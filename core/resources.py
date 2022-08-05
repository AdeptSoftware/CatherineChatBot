# Классы для работы с ресурсами (json-файлами) приложения
import core.messenger.message as _msg
import random
import json

# ======== ========= ========= ========= ========= ========= ========= =========

class ProtectedDictionary:
    def __init__(self, _dict):
        self._data = _dict

    def __getitem__(self, key):
        return self._data[key]

# ======== ========= ========= ========= ========= ========= ========= =========

class Resource(ProtectedDictionary):
    def __init__(self, filename, encoding="utf-8"):
        with open(filename, 'r', encoding=encoding) as f:
            super().__init__(json.loads(f.read().encode(encoding)))

# ======== ========= ========= ========= ========= ========= ========= =========

class LanguageResource(Resource):
    def __init__(self, filename, encoding="utf-8"):
        super().__init__(filename, encoding)
        _msg.set_catherine_names(self._data["CATHERINE"])

    # Вернёт одну из строк в списке
    def rnd(self, key):
        index = random.randint(0, len(self._data[key])-1)
        return self._data[key][index]

# ======== ========= ========= ========= ========= ========= ========= =========
