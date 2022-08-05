# 03.06.2022
import datetime
from core.time import timezone

# ======== ========= ========= ========= ========= ========= ========= =========
# Типы событий

TYPE_TIMETABLE = 0					# Вывод текста по расписанию

# ======== ========= ========= ========= ========= ========= ========= =========

def timetable(event):
	data = event["data"]
	if "current" in event:
		ans = data["msgr"].create_answer(data["pid"])
		ans.set_text(event["current"])
		data["msgr"].send(ans.get())
		event["current"] = None
	# Определение времени отправки следующего сообщения (z)
	days = 0
	now = datetime.datetime.now() + datetime.timedelta(hours=data["timezone"]-timezone())
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

def loader(appdata, filename="events.json"):
	data = appdata.storage.create_storage_object(filename).get()
	with data:
		appdata.events.set_update_time(data["update"])
		for event in data["events"]:
			if event["type"] == TYPE_TIMETABLE:
				event["data"]["msgr"] = appdata.messenger(event["msgr_id"])
				appdata.events.new(timetable, event)

# ======== ========= ========= ========= ========= ========= ========= =========
