# 03.06.2022
import datetime
from core.xtime import timezone

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

def loader(app, filename="events.json"):
	data = app.storage.create_storage_object(filename).get()
	with data:
		for event in data.value:
			if event["type"] == TYPE_TIMETABLE:
				event["data"]["msgr"] = app.messengers[event["msgr_id"]]
				app.events.new(timetable, event)

# ======== ========= ========= ========= ========= ========= ========= =========
