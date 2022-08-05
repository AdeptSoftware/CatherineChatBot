# 27.05.2022-28.05.2022
from core.messenger.messenger			import TYPE_DISCORD
from core.thread						import run_thread
from core.commands.appdata 				import AppData
import time

# ======== ========= ========= ========= ========= ========= ========= =========

class Application:
	def __init__(self, data: AppData):
		print(data.lang["INIT"])
		self._is_running	= False
		self._threads		= []
		self._data			= data

	# ==== ========= ========= ========= ========= ========= ========= =========

	def _run(self, fn, name):
		self._threads += [run_thread(fn, name)]

	# Должно быть вызвано после create, use_storage_manager и use_messenger!
	# Если sleep <= 0, то Вы обязаны заняться циклом программы сами
	def run(self, sleep=60):
		if not self._is_running:
			if self._data.events is not None:
				self._run(self._data.events.run, self._data.events.__name__)
			pos = 0
			discord = None
			for msgr in self._data.messengers:
				msgr.set_appdata(self._data)
				if msgr.type_id != TYPE_DISCORD:
					self._run(msgr.run, "{0}:{1}".format(type(msgr), pos))
				else:
					discord = msgr
				pos += 1
			self._is_running = True
			print(self._data.lang["RUN"])
			# Ожидаем событий...
			if discord:
				discord.run()
			else:
				while True:
					time.sleep(sleep)
		# Если ошибка/достигли конца функции, то все потоки завершатся!

# ======== ========= ========= ========= ========= ========= ========= =========
		