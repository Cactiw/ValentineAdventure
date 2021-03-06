from telegram import Bot
from telegram.utils.request import Request
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)


import multiprocessing
import queue
import threading
import time
import logging
import traceback
import re

MESSAGE_PER_SECOND_LIMIT = 29
MESSAGE_PER_CHAT_LIMIT = 3
MESSAGE_PER_CHAT_MINUTE_LIMIT = 19

UNAUTHORIZED_ERROR_CODE = 2
BADREQUEST_ERROR_CODE = 3

MAX_MESSAGE_LENGTH = 4096


class AsyncBot(Bot):

    def __init__(self, token, workers=4, request_kwargs=None):
        counter_rlock = threading.RLock()
        self.counter_lock = threading.Condition(counter_rlock)
        self.message_queue = multiprocessing.Queue()
        self.waiting_chats_message_queue = multiprocessing.Queue()
        self.dispatcher = None
        self.processing = True
        self.num_workers = workers
        self.messages_per_second = 0
        self.messages_per_chat = {}
        self.messages_per_chat_per_minute = {}
        self.spam_chats_count = {}

        self.second_reset_queue = multiprocessing.Queue()
        self.minute_reset_queue = multiprocessing.Queue()

        self.workers = []
        self.resending_workers = []
        self.group_workers = []
        if request_kwargs is None:
            request_kwargs = {}
        con_pool_size = workers + 4
        if 'con_pool_size' not in request_kwargs:
            request_kwargs['con_pool_size'] = con_pool_size
        self._request = Request(**request_kwargs)
        super(AsyncBot, self).__init__(token=token, request=self._request)

        self.types_to_methods = {0: self.send_message, 1: self.send_video, 2: self.send_audio, 3: self.send_photo,
                                 4: self.send_document, 5: self.send_sticker, 6: self.send_voice, 7: self.sendVideoNote}
        self.methods_ty_types = {v: k for k, v in list(self.types_to_methods.items())}
        self.types_to_original_methods = {
            0: super(AsyncBot, self).send_message, 1: super(AsyncBot, self).send_video,
            2: super(AsyncBot, self).send_audio, 3: super(AsyncBot, self).send_photo,
            4: super(AsyncBot, self).send_document, 5: super(AsyncBot, self).send_sticker,
            6: super(AsyncBot, self).send_voice, 7: super(AsyncBot, self).sendVideoNote,
            8: super(AsyncBot, self).answerCallbackQuery
        }

    def send_message(self, *args, **kwargs):
        message = MessageInQueue(*args, **kwargs)
        self.message_queue.put(message)
        return 0

    # # Функция отправки сообщения в конкретную группу,
    # # используйте group_send_message для автоматического получения этой группы
    # def send_message_in_user_group(self, group, *args, **kwargs):
    #     message = MessageInQueue(*args, **kwargs)
    #     if isinstance(group, int):
    #         group = message_groups.get(group)
    #     if group is None:
    #         raise TypeError
    #     group.add_message(message)
    #
    # # Отправка в группу для chat_id, которая передаётся вместе с сообщением
    # def group_send_message(self, *args, **kwargs):
    #     chat_id = kwargs.get('chat_id')
    #     if chat_id is None:
    #         chat_id = args[0]
    #     self.send_message_in_user_group(self.get_message_group(chat_id), *args, **kwargs)
    #
    # # Отправка всех сообщений из группы
    # def send_message_group(self, chat_id):
    #     self.get_message_group(chat_id).send_group()
    #
    # # Метод для получения группы заданного пользователя, или создания таковой при её отстутствии
    # # Необходим заданный атрибут dispatcher у bot
    # def get_message_group(self, player_id):
    #     user_data = self.dispatcher.user_data.get(player_id)
    #     id = user_data.get("message_group")
    #     if id is None:
    #         group = MessageGroup(player_id)
    #         user_data.update({"message_group": group.id})
    #     else:
    #         group = message_groups.get(id)
    #     if group is None or group.created_id != player_id:
    #         # Запись в user data устарела, группа уже не существует
    #         user_data.pop("message_group")
    #         return self.get_message_group(player_id)
    #     return group

    def send_video(self, *args, **kwargs):
        kwargs.update({"message_type": 1})
        message = MessageInQueue(*args, **kwargs)
        self.message_queue.put(message)
        return 0

    def send_audio(self, *args, **kwargs):
        kwargs.update({"message_type": 2})
        message = MessageInQueue(*args, **kwargs)
        self.message_queue.put(message)
        return 0

    def send_photo(self, *args, **kwargs):
        kwargs.update({"message_type": 3})
        message = MessageInQueue(*args, **kwargs)
        self.message_queue.put(message)
        return 0

    def send_document(self, *args, **kwargs):
        kwargs.update({"message_type": 4})
        message = MessageInQueue(*args, **kwargs)
        self.message_queue.put(message)
        return 0

    def send_sticker(self, *args, **kwargs):
        kwargs.update({"message_type": 5})
        message = MessageInQueue(*args, **kwargs)
        self.message_queue.put(message)
        return 0

    def send_voice(self, *args, **kwargs):
        kwargs.update({"message_type": 6})
        message = MessageInQueue(*args, **kwargs)
        self.message_queue.put(message)
        return 0

    def sendVideoNote(self, *args, **kwargs):
        kwargs.update({"message_type": 7})
        message = MessageInQueue(*args, **kwargs)
        self.message_queue.put(message)
        return 0

    def answerCallbackQuery(self, *args, **kwargs):
        kwargs.update({"message_type": 8})
        message = MessageInQueue(*args, **kwargs)
        self.message_queue.put(message)
        return 0

    def check_and_translate(self, *args, **kwargs):
        chat_id = kwargs.get('chat_id')
        if chat_id is None:
            try:
                chat_id = args[0]
            except IndexError:
                chat_id = 0
        mes_text: str = kwargs.get('text')
        return args, kwargs

    def editMessageText(self, *args, **kwargs):
        args, kwargs = self.check_and_translate(*args, **kwargs)
        return super(AsyncBot, self).editMessageText(*args, **kwargs)

    def sync_send_message(self, *args, **kwargs):
        return super(AsyncBot, self).send_message(*args, **kwargs)

    def actually_send_message(self, *args, **kwargs):
        chat_id = kwargs.get('chat_id')
        if chat_id is None:
            try:
                chat_id = args[0]
            except IndexError:
                chat_id = 0
        message_type = kwargs.get('message_type')
        if message_type is None:
            message_type = 0

        if message_type in frozenset([0]):
            args, kwargs = self.check_and_translate(*args, **kwargs)

        lock = self.counter_lock
        lock.acquire()
        try:
            while True:
                lock.acquire()
                if chat_id in self.spam_chats_count and not kwargs.get("resending"):
                    spam_was = self.spam_chats_count.get(chat_id)
                    if time.time() - spam_was > 30 * 60:
                        self.spam_chats_count.pop(chat_id)
                    else:
                        self.spam_chats_count.update({chat_id: time.time()})
                        self.waiting_chats_message_queue.put(MessageInQueue(*args, **kwargs))
                        lock.release()
                        return None
                messages_per_current_chat = self.messages_per_chat.get(chat_id)
                messages_per_current_chat_per_minute = self.messages_per_chat_per_minute.get(chat_id)
                if messages_per_current_chat is None:
                    messages_per_current_chat = 0
                if messages_per_current_chat_per_minute is None:
                    messages_per_current_chat_per_minute = 0
                if self.messages_per_second < MESSAGE_PER_SECOND_LIMIT and messages_per_current_chat < \
                        MESSAGE_PER_CHAT_LIMIT and messages_per_current_chat_per_minute < MESSAGE_PER_CHAT_MINUTE_LIMIT:
                    self.messages_per_second += 1
                    self.messages_per_chat.update({chat_id: messages_per_current_chat + 1})
                    self.messages_per_chat_per_minute.update({chat_id: messages_per_current_chat_per_minute + 1})
                    lock.release()
                    break
                else:
                    if self.messages_per_second < MESSAGE_PER_SECOND_LIMIT and \
                            (not kwargs.get("resending") or chat_id > 0):
                        # Сообщения в эту секунду ещё можно отправлять
                        if chat_id > 0:
                            # Личка, маленькие чаты -- отправляем любое число сообщений в минуту
                            if messages_per_current_chat < MESSAGE_PER_CHAT_LIMIT:
                                self.messages_per_second += 1
                                self.messages_per_chat.update({chat_id: messages_per_current_chat + 1})
                                self.messages_per_chat_per_minute.update(
                                    {chat_id: messages_per_current_chat_per_minute + 1})
                                lock.release()
                                break
                        if messages_per_current_chat_per_minute >= MESSAGE_PER_CHAT_MINUTE_LIMIT:
                            self.spam_chats_count.update({chat_id: time.time()})
                        if not kwargs.get("message_in_group"):
                            # Кладём в другую очередь, если сообщение не в группе сообщений
                            self.waiting_chats_message_queue.put(MessageInQueue(*args, **kwargs))
                            lock.release()
                            return None
                lock.release()
                lock.wait()
        finally:
            try:
                lock.release()
            except RuntimeError:
                pass
        message = None
        try:
            try:
                method = self.types_to_original_methods.get(message_type)
                if method is None:
                    method = super(AsyncBot, self).send_message
            except Exception:
                logging.error(traceback.format_exc())
                method = super(AsyncBot, self).send_message
            message = method(*args, **kwargs)
        except Unauthorized:
            return UNAUTHORIZED_ERROR_CODE
        except BadRequest:
            logging.error(traceback.format_exc())
            logging.error(kwargs)
            return BADREQUEST_ERROR_CODE
        except (TimedOut, NetworkError):
            logging.error(traceback.format_exc())
            # return None

            # Временно отключена повторная попытка отправить -- уже нет
            # Сообщение отправляется ещё раз, иначе -- отправляется в другую очередь
            retry = kwargs.get('retry')
            if retry is None:
                retry = 0
            if retry >= 1:
                # Кладём в другую очередь
                self.waiting_chats_message_queue.put(MessageInQueue(*args, **kwargs))
                return
            retry += 1
            kwargs.update({"retry": retry})
            time.sleep(0.1)
            try:
                method = self.types_to_original_methods.get(message_type)
                if method is None:
                    method = super(AsyncBot, self).send_message
            except Exception:
                logging.error(traceback.format_exc())
                method = super(AsyncBot, self).send_message
            message = method(*args, **kwargs)
        finally:
            body = {"chat_id": chat_id, "time": time.time()}
            self.second_reset_queue.put(body)
            self.minute_reset_queue.put(body)
        return message

    def start(self):
        for i in range(0, self.num_workers):
            worker = threading.Thread(target=self.__work, args=())
            worker.start()
            self.workers.append(worker)
            resending_worker = threading.Thread(target=self.__resend_work, args=())
            resending_worker.start()
            self.resending_workers.append(worker)
            # group_worker = threading.Thread(target=self.__group_work, args=())
            # group_worker.start()
            # self.group_workers.append(group_worker)
        threading.Thread(target=self.__release_monitor, args=(self.second_reset_queue, 1)).start()
        threading.Thread(target=self.__release_monitor, args=(self.minute_reset_queue, 60)).start()

    def set_dispatcher(self, dispatcher):
        self.dispatcher = dispatcher

    def stop(self):
        self.processing = False
        self.second_reset_queue.put(None)
        self.minute_reset_queue.put(None)
        for i in range(0, self.num_workers):
            self.message_queue.put(None)
            self.waiting_chats_message_queue.put(None)
            # groups_need_to_be_sent.put(None)  Groups
        for i in self.workers:
            i.join()
        for i in self.resending_workers:
            i.join()
        time.sleep(1)
        try:
            while True:
                self.message_queue.get_nowait()
        except queue.Empty:
            pass
        try:
            while True:
                self.waiting_chats_message_queue.get_nowait()
        except queue.Empty:
            pass
        self.message_queue.close()
        self.waiting_chats_message_queue.close()
        self.second_reset_queue.close()
        self.minute_reset_queue.close()

    def __del__(self):
        self.processing = False
        for i in range(0, self.num_workers):
            #self.message_queue.put(None)
            pass
        self.message_queue.close()
        try:
            super(AsyncBot, self).__del__()
        except AttributeError:
            pass


    def __releasing_resourse(self, chat_id):
        with self.counter_lock:
            self.messages_per_second -= 1
            mes_per_chat = self.messages_per_chat.get(chat_id)
            if mes_per_chat is None:
                self.counter_lock.notify_all()
                return
            if mes_per_chat == 1:
                self.messages_per_chat.pop(chat_id)
                self.counter_lock.notify_all()
                return
            mes_per_chat -= 1
            self.messages_per_chat.update({chat_id: mes_per_chat})
            self.counter_lock.notify_all()

    def __release_monitor(self, release_queue, interval):
        data = release_queue.get()
        while self.processing and data is not None:
            chat_id = data.get("chat_id")
            set_time = data.get("time")
            if chat_id is None or time is None:
                data = release_queue.get()
                continue
            remaining_time = interval - (time.time() - set_time)
            if remaining_time > 0:
                while remaining_time > 5:
                    time.sleep(5)
                    remaining_time -= 5
                    if not self.processing:
                        return
                time.sleep(remaining_time)
            if interval == 60:
                self.__releasing_minute_resourse(chat_id)
            else:
                self.__releasing_resourse(chat_id)
            try:
                data = release_queue.get()
            except Exception:
                return

    def __releasing_minute_resourse(self, chat_id):
        with self.counter_lock:
            mes_per_chat = self.messages_per_chat_per_minute.get(chat_id)
            if mes_per_chat is None:
                self.counter_lock.notify_all()
                return
            if mes_per_chat == 1:
                self.messages_per_chat_per_minute.pop(chat_id)
                self.counter_lock.notify_all()
                return
            mes_per_chat -= 1
            self.messages_per_chat_per_minute.update({chat_id: mes_per_chat})
            self.counter_lock.notify_all()

    def __work(self):
        message_in_queue = self.message_queue.get()
        while self.processing and message_in_queue is not None:
            args = message_in_queue.args
            kwargs = message_in_queue.kwargs
            self.actually_send_message(*args, **kwargs)
            message_in_queue = self.message_queue.get()
            if message_in_queue is None:
                return 0
        return 0

    def __resend_work(self):
        message_in_queue = self.waiting_chats_message_queue.get()
        while self.processing and message_in_queue is not None:
            args = message_in_queue.args
            kwargs = message_in_queue.kwargs
            kwargs.update({"resending": True})
            mes = self.actually_send_message(*args, **kwargs)
            if mes is None:
                time.sleep(0.1)
            message_in_queue = self.waiting_chats_message_queue.get()
            if message_in_queue is None:
                return 0
        return 0

    # def __group_work(self):
    #     group = groups_need_to_be_sent.get()
    #     while self.processing and group is not None:
    #         while True:
    #             message = group.get_message()
    #             if message is 1:
    #                 group.busy = False
    #                 break
    #             if message is None:
    #                 group = None
    #                 break
    #             message.kwargs.update({"resending": True, "message_in_group": True})
    #             self.actually_send_message(*message.args, **message.kwargs)
    #         if group is not None:
    #             group.busy = False
    #         group = groups_need_to_be_sent.get()
    #

class MessageInQueue:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
