# 14.06.2022
from core.storage.yadisk_storage        import YandexStorageManager
from core.storage.local_storage         import LocalStorageManager
from core.messenger.discord.messenger   import DiscordMessenger
from core.messenger.vk.messenger        import VkMessenger, TYPE_VK
from core.event                         import EventManager
from core.commands.appdata 		        import AppData
from core.resources                     import Resource, LanguageResource
from core.time                          import set_timezone

import appx.application
import appx.events

import core.debug
import json

# ========= ========= ========= ========= ========= ========= ========= =========

class AppBuilder:
    # data, lang - пути до файлов
    def __init__(self, data, lang):
        self._data              = self.load(data)
        self._auth              = None
        # Обработчики
        self._on_events_load    = None
        # AppData variables
        self._storage           = None
        self._messengers        = []
        self._events            = None
        self._lang              = LanguageResource(lang)
        self._const             = Resource("constants.json")

    def get(self):
        data = AppData(
            self._storage,
            self._messengers,
            self._events,
            self._lang,
            self._const
        )
        if self._on_events_load:
            self._on_events_load(data)
        return appx.application.Application(data)

    @property
    def auth(self):
        return self._auth

    @staticmethod
    def load(filename):
        with open(filename, 'r') as f:
            return json.loads(f.read())

    def use_local_storage(self):
        self.use_storage(LocalStorageManager(self._data["src"]))

    def use_yandex_storage(self):
        token = self._data["token"]
        self.use_storage(YandexStorageManager(self._data["dst"], token))

    def use_storage(self, storage):
        self._storage = storage
        if not self._storage.create():
            raise Exception(self._lang["INIT_FAILED"])
        self._auth = storage.create_storage_object("auth.json").get()
        with self._auth:
            set_timezone(self._auth["timezone"])
            # инициализация мессенджеров
            for data in self._auth["messengers"]:
                if data["type"] == TYPE_VK:
                    self._messengers += [VkMessenger(data)]
                else:
                    self._messengers += [DiscordMessenger(data)]

    def use_debug(self):
        # инициализация класса для отладки
        out = self._storage.create_storage_object(self._data["log"], False)
        with self._auth:
            core.debug.init(out)
        # Оповещение о запуске
        core.debug.get().log(self._lang["INIT"], True)

    def use_events(self):
        self._on_events_load = appx.events.loader
        self._events = EventManager("events")

# ========= ========= ========= ========= ========= ========= ========= =========
