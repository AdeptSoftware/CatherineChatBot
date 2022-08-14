# Классы для работы с ресурсами (json-файлами) приложения
import core.messenger.message as _msg
import random
import json

# ======== ========= ========= ========= ========= ========= ========= =========

class LanguageResource:
    def __init__(self, filename, encoding="utf-8"):
        with open(filename, 'r', encoding=encoding) as f:
            self._data = json.loads(f.read().encode(encoding))
        # Корректировка значений
        _msg.set_catherine_names(self._data["CATHERINE"])
        self._split()

    def __getitem__(self, key):
        return self._data[key]

    # Вернёт одну из строк в списке
    def rnd(self, key):
        index = random.randint(0, len(self._data[key])-1)
        return self._data[key][index]

    def _split(self):
        for key in self._data:
            if key[0] == '#':
                _list = []
                _list += [value.lower().split(' ') for value in self._data[key]]
                self._data[key] = _list

# ======== ========= ========= ========= ========= ========= ========= =========
