# 28.05.2022
from core.storage.yadisk_storage	import YandexStorageManager
from core.messenger.discord			import DiscordMessenger
from core.messenger.vk				import VkMessenger
from core.event						import EventManager

from appx.application				import Application		# Пример приложения
import core.debug	
			
import appx.events
import json

# ========= ========= ========= ========= ========= ========= ========= =========

def preset(filename):
	with open(filename, 'r') as f:
		data = json.loads(f.read())
	# Настроим поведение бота
	app.use_storage_manager(YandexStorageManager(data["token"], data["dst"]))
	auth = app.storage.create_storage_object("auth.json").get()
	with auth:
		# инициализация класса для отладки
		core.debug.init(app.storage.cso(data["out"], False), auth.value["timezone"])
		# Оповещение о запуске
		core.debug.get().log(app.lang("INIT"), True)
		# Инициализация мессенджеров
		app.add_messenger(DiscordMessenger(auth.value["discord"]))
		app.add_messenger(VkMessenger(auth.value["vk"]))
	# Загрузим события/оповещения
	app.use_event_manager(EventManager("events"))
	events = app.storage.create_storage_object("events.json").get()
	with events:
		for event in events.value:
			appx.events.loader(app, event)

# ========= ========= ========= ========= ========= ========= ========= =========
# Все папки и файлы в хранилище должны существовать!

app = Application()
preset("data.json")
app.run()

# ========= ========= ========= ========= ========= ========= ========= =========
