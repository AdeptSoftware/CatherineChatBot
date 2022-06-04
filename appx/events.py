# 03.06.2022
from core.messenger.vk			import VkMessenger
import datetime

# ======== ========= ========= ========= ========= ========= ========= =========
# Типы событий

TYPE_VK_TIMETABLE = 0					# Вывод текста по расписанию

# ======== ========= ========= ========= ========= ========= ========= =========

def vk_timetable(event):
	data = event["data"]
	if "current" in event:
		data.msgr.msg(data["pid"]).send(event["current"])
		event["current"] = None
	# Определение времени отправки следующего сообщения (z)
	days = 0
	now = datetime.datetime.now() + datetime.timedelta(hours=data["timezone"])
	while days < 8:			# Неделя+1
		for msg in data["lst"]:
			z = datetime.datetime(now.year, now.month, now.day, msg["hour"], msg["minute"])
			z += datetime.timedelta(days=days)
			if msg["isoweekday"] is None or z.isoweekday() in msg["isoweekday"]:
				if now > z:
					continue
				event["current"] = msg["params"]
				cooldown = (z-now).total_seconds()
				if cooldown < 0:
					cooldown = 5
				event["cooldown"] = cooldown
				return True
		days += 1
	return True

# ======== ========= ========= ========= ========= ========= ========= =========

class Dictionary(dict): pass

# ======== ========= ========= ========= ========= ========= ========= =========

def loader(app, event):
	event["data"] = Dictionary(event["data"])
	if event["type"] == TYPE_VK_TIMETABLE:
		event["data"].msgr = app.messenger(cls=VkMessenger)
		app.events.new(vk_timetable, event)


# ======== ========= ========= ========= ========= ========= ========= =========