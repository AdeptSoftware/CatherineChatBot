# Базовый класс для хранения важных объектов приложения

class AppData:  # Не придумал название лучше...
    def __init__(self, storage, messengers, events, lang, constants):
        self._storage		= storage
        self._messengers	= tuple(messengers)
        self._events		= events
        self._lang          = lang
        self._constants		= constants

    @property
    def events(self):
        return self._events

    @property
    def storage(self):
        return self._storage

    @property
    def lang(self):
        return self._lang

    @property
    def const(self):
        return self._constants

    @property
    def messengers(self):
        return self._messengers

    def messenger(self, key):
        return self._messengers[key]

# ========= ========= ========= ========= ========= ========= ========= =========
