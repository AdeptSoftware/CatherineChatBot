#
from core.storage.cls                   import IStorageManager
from core.resources                     import LanguageResource
from core.updater                       import Updater
from core.event                         import EventManager
from core.messenger.answer              import IAnswer
from core.messenger.message             import AbstractMessage

# Применяется для хранения важных классов приложения и доступа к ним
class CommonData:
    def __init__(self):
        self.storage        = None
        self.updater        = None
        self.messengers     = []
        self.events         = None
        self.lang           = None

# ======== ========= ========= ========= ========= ========= ========= =========

# Передается в CommandManager. Для каждого мессенджера свой
class Context:
    def __init__(self, data: CommonData):
        # Общие поля
        self._storage       = data.storage              # IStorageManager
        self._updater       = data.updater              # Updater
        self._messengers    = tuple(data.messengers)    # AbstractMessengers
        self._events        = data.events               # EventManager
        self._lang          = data.lang                 # LanguageResource
        # Поля связанные с мессенджером
        self._messenger     = None                      # AbstractMessenger
        self._commands      = None                      # CommandManager
        self._message       = None                      # AbstractMessage
        self._answer        = None                      # IAnswer

    @property
    def storage(self) -> IStorageManager:
        return self._storage

    @property
    def updater(self) -> Updater:
        return self._updater

    @property
    def messengers(self):
        return self._messengers

    @property
    def events(self) -> EventManager:
        return self._events

    @property
    def lang(self) -> LanguageResource:
        return self._lang

    @property
    def msgr(self):
        return self._messenger

    @property
    def mngr(self):
        return self._commands

    @property
    def msg(self) -> AbstractMessage:
        return self._message

    @property
    def ans(self) -> IAnswer:
        return self._answer

# ======== ========= ========= ========= ========= ========= ========= =========

# Должен быть свой у каждого AbstractMessenger'а
class ContextEx(Context):
    def __init__(self, mngr, msgr, data):
        super().__init__(data)
        self._messenger = msgr
        self._commands  = mngr

    def set_answer(self, ans):
        self._answer = ans

    def set_message(self, msg):
        self._message = msg

# ======== ========= ========= ========= ========= ========= ========= =========
