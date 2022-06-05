# 17.01.2022-27.05.2022
import random
import json

# ======== ========= ========= ========= ========= ========= ========= =========

_lang = []

# ======== ========= ========= ========= ========= ========= ========= =========

# Доступные: "ru"
def set_locale(lang, encoding="utf-8"):
    global _lang
    path = None
    if lang == "ru":
        path = "core/lang/ru.json"

    if path:
        with open(path, 'r', encoding=encoding) as f:
            _lang = json.loads(f.read().encode(encoding))
            return
    raise FileNotFoundError(f"Unknown lang: {lang}")

# ======== ========= ========= ========= ========= ========= ========= =========

# случайный элемент из списка
def rndx(lst):
    return lst[random.randint(0, len(lst) - 1)]

def rnd(key):
    return rndx(_lang[key])

def get(key):
    return _lang[key]

# ======== ========= ========= ========= ========= ========= ========= =========
