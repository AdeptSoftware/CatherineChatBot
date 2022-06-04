# 27.05.2022-28.05.2022
from core.messenger.discord		import DiscordMessenger
from core.thread				import run_thread
import core.lang				as _lang
import time

# ======== ========= ========= ========= ========= ========= ========= =========

class Application:
	def __init__(self, lang="ru"):
		_lang.set_locale(lang)
		print(self.lang("INIT"))
		
		self._is_running	= False
		self._threads		= []
		
		self._events		= None				# Event Manager
		self._storage		= None				# Storage Manager
		self._msgr			= {}				# Messengers
		
	# ==== ========= ========= ========= ========= ========= ========= =========

	def use_storage_manager(self, mngr):
		self._storage = mngr
		return mngr.create()
		
	# На данный момент может быть запущен может быть только 1 DiscordMessenger
	# И несколько VkMessenger
	def add_messenger(self, msgr, codename=None):
		if codename is None:
			codename = len(self._msgr)
		self._msgr[codename] = msgr

	def use_event_manager(self, mngr):
		self._events = mngr

	# ==== ========= ========= ========= ========= ========= ========= =========

	@property
	def storage(self):
		return self._storage

	@property
	def events(self):
		return self._events

	def messenger(self, codename=None, cls=None):
		if cls is not None:
			for key in self._msgr:
				if type(self._msgr[key]) is cls:
					return self._msgr[key]
		return self._msgr[codename]

	# ==== ========= ========= ========= ========= ========= ========= =========

	def run_thread(self, fn, name):
		self._threads += [run_thread(fn, name)]

	# Должно быть вызвано после create, use_storage_manager и use_messenger!
	# Если sleep <= 0, то Вы обязаны заняться циклом программы сами
	def run(self, sleep=5):
		if not self._is_running:
			if self._events is not None:
				self.run_thread(self._events.run, self._events.__name__)
			discord = None
			for codename in self._msgr:
				if type(self._msgr[codename]) is not DiscordMessenger:
					self.run_thread(self._msgr[codename].run, codename)
				else:
					discord = self._msgr[codename]
			self._is_running = True
			print(self.lang("RUN"))
			# Ожидаем событий...
			if discord:
				discord.run()
			else:
				time.sleep(sleep)
				while self.is_running():
					time.sleep(sleep)
			# Если достигли конца функции, то все потоки завершатся!

	def is_running(self):
		for codename in self._msgr:
			if not self._msgr[codename].is_running():
				return False
		return self._is_running
	
	# ==== ========= ========= ========= ========= ========= ========= =========

	@staticmethod
	def lang(key):
		return _lang.get(key)

# ======== ========= ========= ========= ========= ========= ========= =========
		