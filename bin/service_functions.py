

import re


def multiple_replace(dic, text) -> str:
    pattern = "|".join(map(re.escape, dic.keys()))
    return re.sub(pattern, lambda m: dic[m.group()], text)


def apply_genders(base_text: str, my_sex: int, partner_sex: int) -> str:
    my = {'[q]': ['к', 'ца'], '[w]': ['ку', 'це'], '[e]': ['ком', 'цей'], '[r]': ['', 'а'], '[t]': ['ся', 'ась'],
          '[y]': ['й', 'я'], '[u]': ['го', 'ё'], '[i]': ['му', 'й'], '[o]': ['ёл', 'ла'], '[p]': ['ый', 'ая'],
          '[a]': ['его', 'ю'], '[b]': ['ка', 'цу'], '[s]': ['им', 'ей'], '[d]': ['го', 'ей'], '[f]': ['ка', 'цы']}
    partner = {'[qq]': ['к', 'ца'], '[ww]': ['ку', 'це'], '[ee]': ['ком', 'цей'], '[rr]': ['', 'а'],
               '[tt]': ['ся', 'ась'], '[yy]': ['й', 'я'], '[uu]': ['го', 'ё'], '[ii]': ['му', 'й'], '[oo]': ['ёл', 'ла'],
               '[pp]': ['ый', 'ая'], '[aa]': ['его', 'ю'], '[bb]': ['ка', 'цу'], '[ss]': ['им', 'ей'], '[dd]': ['го', 'ей'],
               '[ff]': ['ка', 'цы']}

    for i in my:
        my[i] = my[i][my_sex]
    for i in partner:
        partner[i] = partner[i][partner_sex]
    my.update(partner)
    return multiple_replace(my, base_text)
