

quests = {
    0: {
        "quest_type": "quest",
        "enter_text": """Ты медленно приходил в себя. Снег острыми иглами впивался в щёку, а голова невыносимо болела, отказываясь вспоминать события последних дней. С трудом заставив себя подняться и открыть глаза, ты огляделся. Рядом с тобой приходил в себя твой спутник, а вокруг стояла толпа полуголых лучников. Стоило тебе приглядеться к ним получше, как сразу пришлось пожалеть об этом решении. Красные опухшие лица, пивные животы, и какие-то белые тряпки, едва прикривывшие все интимные места, стоявших пред тобой людей. Вдобавок, у каждого за спиной почему-то были ободранные крылья, не то вороны, не то голубя. Сознание не выдержало этой картины и в глазах потемнело...""",
        "answers": {
            "Дальше": {
                "new_id": 1,
                "wait_companion": True,
                "result": {
                    # "gain": {
                    #     "1": 1
                    # },
                    "set_progress": 1
                }
            }
        }
    },
    1: {
        "quest_type": "quest",
        "enter_text": """Неприятный запах перегара заставил тебя снова очнуться. Один из тех мужиков стоял на тобой и хлопал по щекам.
– Отвали, придурок! — твой удар был неожиданностью, и мужик упал на снег. Поднявшись, он обратился к тебе и твоему спутнику:
– Пьянчуги вы проклятые, - эти слова прозвучали невероятно иронично, учитывая вид говорившего, - наконец мы вас нашли! Ворвались к нам пару дней назад и все волшебные стрелы украли. А без них, в мире не будет любви! Вот теперь идите в ту пещеру, где вы их про... оставили, и верните. - к вам пришло осознание, что эти мужики это купидоны, а грзный вид пары десятков луков помог принять верное решение. Так вы с компаньоном отправились в путь.""",
        "answers": {
            "Отправиться в пещеру": {
                "new_id": 2,
                "wait_companion": True,
            }
        }
    },
    2: {
        "quest_type": "quest",
        "enter_text": """Вы вошли в пещеру, оставляя яркий и светлый мир за своей спиной. Но не успела ваша команда пройти и нескольких шагов, как в глубине пещеры раздалось злобное шипение. Тихо шагая, оттуда вышла пушистая рысь. Вы только посмотрите, какая она милая! А эти глазки, а кисточки на ушах! Но рысь почему-то выпустила когти. О нет, она собирается напасть!
дальше идёт бой (пока без него)""",
        "answers": {
            "В бой!": {
                "battle": {
                    "enemies": {
                        "Child Lynx": {
                            "lvl": 2,
                            "hp": 15,
                            "max_hp": 15,
                            "attack": 2,

                        }
                    }
                },
                "new_id": 3,
                "wait_companion": False,
            }
        }
    },
    3: {
        "quest_type": "quest",
        "enter_text": """Вы убили маленькую рысь! Как вы могли! Уму не постижимо, что вы действительно сделали это! Тем не менее, перед вами самый первый зал пещеры. Впереди тонель, ведущий куда-то вглубь, на стенах видны какие-то надписи, а в центре лежит убитая вами, негодяями, пушистая рысь. Внезапно из угла зала раздался тихий писк.""",
        "answers": {
            "Идти дальше": {
                "new_id": 4,
                "wait_companion": True,
            },
            "Осмотреть стены": {
                "new_id": 3,
                "wait_companion": False,
                "path": "wall",
                "progress": 0,
                "first_text": """Ты подходишь к стене и видишь надпись кровью - <em>Герой, помни, чтобы сбежать из боя, достаточно лишь произнести /cancel</em>
                Чтобы это ни значило, ты решил запомнить эти слова.""",
                "second_text": """Твой спутник встал у стены, на которой вы заметили странные надписи. Сейчас он водит по ней пальцем и бубнит какую-то фразу, но ты не смог расслышать, что именно он говорит.""",
            },
            "Прочесть ещё раз": {
                "new_id": 3,
                "wait_companion": False,
                "path": "wall",
                "progress": 1,
                "add_progress": 0,
                "first_text": """Ты подходишь к стене и видишь надпись кровью - <em>Герой, помни, чтобы сбежать из боя, достаточно лишь произнести /cancel</em>
Чтобы это ни значило, ты решил запомнить эти слова.""",
                "second_text": """Твой спутник встал у стены, на которой вы заметили странные надписи. Сейчас он водит по ней пальцем и бубнит какую-то фразу, но ты не смог расслышать, что именно он говорит.""",
            },
            "Выпотрошить рысь": {
                ""
                "new_id": 3,
                "wait_companion": False,
                "path": "Lynx",
                "progress": 0,
            },
            "Продолжать потрошить рысь": {
                ""
                "new_id": 3,
                "wait_companion": False,
                "path": "Lynx",
                "progress": 1,
                "first_text": """Что с тобой не так? Эта рысь и так уже мертва. И всё же ты разрываешь её на части. Ничего полезного внутри нет. Только кровь и органы... А что там могло быть? Это не рпг, где волки бегают с золотыми мечами внутри!""",
                "second_text": """Ты услышал, как твой спутник идёт к рыси. Обервнушись ты увидел жуткую картину. Твой спутник просто так принялся разделывать убитую вами рысь. Тёплая кровь струилась по холодному камню. Но твоего компаньона это не останавливало..."""

            },
            "Потрошить дальше": {
                ""
                "new_id": 3,
                "wait_companion": False,
                "path": "Lynx",
                "progress": 2,
                "add_progress": 0,
                "first_text": """Ты решил продолжить уничтожение останков рыси. Не похоже, чтобы в этом был хоть какой-то смысл, но тебя это не волновало.""",
                "second_text": """Ты замечаешь, как твой спутник склонился над телом рыси. Словно безумный, он режет и режет останки рыси. От неё и так осталось немного... Ты не выдержал и тебя стошнило.""",
            },

            "Идти на писк": {
                "new_id": 3,
                "wait_companion": False,
                "path": "Kittens",
                "progress": 0,
                "first_text": """Прийдя на звук, тебе встретились маленькие котята. Теперь они сироты, а всё из-за тебя и твоего спутника! Но хотя бы остались эти милые малыши.""",
                "second_text": """Твой спутник решил узнать, откуда шёл писк и отправился в угол зала.""",
            },
            "Поиграть с котятами": {
                "new_id": 3,
                "wait_companion": False,
                "path": "Kittens",
                "progress": 1,
                "first_text": """Они такие милые! Пушистые малыши со сверкающими глазками. Пусть из-за тебя и твоего спутника им и грозит неминуемая гибель, сейчас они счастливы поиграть с тобой.""",
                "second_text": """Твой компаньон нашёл маленьких рысят и решил с ними поиграть. Он так счастлив, ведь малыши невероятно милые. Тебе захотелось подойти к ним...""",
            },
            "Убить котят": {
                "new_id": 3,
                "wait_companion": False,
                "path": "Kittens",
                "progress": 1,
                "add_progress": 9,
                "first_text": """Господи! Зачем было так делать! Твои руки полностью в крови. Нет тебе прощенья. Как в мире мог появиться такой человек, как ты! Господи, за что...""",
                "second_text": """Нет! Ты пытаешься закрыть голову руками, ты не хочещь слышать эти звуки, не хочешь смотреть на эту кровь! Ты готов сделать что угодно, лишь бы не слышать, как твой спутник расправляется с маленькими рысятами. За что он так поступает с ними...""",
            },
            "Осмотреть останки котят": {
                "new_id": 3,
                "wait_companion": False,
                "path": "Kittens",
                "progress": 10,
                "add_progress": 1,
                "first_text": """Перед тобой лежат маленькие тела рысят. Они все мертвы из-за вас двоих. И даже пробудившееся чувство совести не сможет сделать тебя вновь хорошим человеком. """,
                "second_text": """Твой спутник вернулся к котятам. Неужели он хочет снова издеваться над телами несчастных детей? Единственное, что обнадёживает - боли они уже не почувствуют...""",
            },
            "Оплакивать котят": {
                "new_id": 3,
                "wait_companion": False,
                "path": "Kittens",
                "progress": 11,
                "add_progress": 1,
                "first_text": """Раскаявшись, ты упал на колени и залился горестными слезами. Солёные капли падали на камни и мягкую шерсть. Но котятам уже ничто не могло помочь. Этот грех тебе не забыть никогда...""",
                "second_text": """Твой спутник заплакал, стоя перед котятами. Но ты знал, что это уже ничего не исправит...""",
            },
            "Продолжить оплакивать котят": {
                "new_id": 3,
                "wait_companion": False,
                "path": "Kittens",
                "progress": 12,
                "add_progress": 0,
                "first_text": """Раскаявшись, ты упал на колени и залился горестными слезами. Солёные капли падали на камни и мягкую шерсть. Но котятам уже ничто не могло помочь. Этот грех тебе не забыть никогда...""",
                "second_text": """Твой спутник заплакал, стоя перед котятами. Но ты знал, что это уже ничего не исправит...""",
            },

            "Поиграть ещё котятами": {
                "new_id": 3,
                "wait_companion": False,
                "path": "Kittens",
                "progress": 2,
                "add_progress": 0,
                "first_text": """Они такие милые! Пушистые малыши со сверкающими глазками. Пусть из-за тебя и твоего спутника им и грозит неминуемая гибель, сейчас они счастливы поиграть с тобой.""",
                "second_text": """Твой компаньон нашёл маленьких рысят и решил с ними поиграть. Он так счастлив, ведь малыши невероятно милые. Тебе захотелось подойти к ним...""",
            },
        }

    },
    4: {
        "quest_type": "quest",
        "enter_text": """Конец первого зала.""",
        "answers": {
            "Заглушка. Не тыкай, сломаешь.": {}
        }
    }
}
