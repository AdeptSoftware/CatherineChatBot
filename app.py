# 28.05.2022
from core.storage.yadisk_storage    import YandexStorageManager
from core.messenger.discоrd         import DiscordMessenger
from core.messenger.vk              import VkMessenger
from core.event                     import EventManager

from appx.application               import Application        # Пример приложения
import core.debug

import appx.events
import json

# ========= ========= ========= ========= ========= ========= ========= =========

def preset(filename):
    with open(filename, 'r') as f:
        data = json.loads(f.read())
    # Настроим поведение бота
    cso = app.storage.create_storage_object
    app.use_storage_manager(YandexStorageManager(data["token"], data["dst"]))   #
    auth = cso("auth.json").get()
    with auth:
        # инициализация класса для отладки
        core.debug.init(cso(data["out"], False), auth["timezone"])              #
        # Оповещение о запуске
        core.debug.get().log(app.lang("INIT"), True)
        # Инициализация мессенджеров
        app.add_messenger(DiscordMessenger(auth["discord"]))
        app.add_messenger(VkMessenger(auth["vk"]))
    # Загрузим события/оповещения
    app.use_event_manager(EventManager("events"))
    events = cso("events.json").get()
    with events:
        for event in events.value:
            appx.events.loader(app, event)

# ========= ========= ========= ========= ========= ========= ========= =========
# Все папки и файлы в хранилище должны существовать!

app = Application()
preset("data.json")                                                             #
app.run()

# ========= ========= ========= ========= ========= ========= ========= =========
