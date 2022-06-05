# 24.05.2022 Базовые классы для работы с мессенджером

# ======== ========= ========= ========= ========= ========= ========= =========

# для аргумента ref функции IMessenger.set_mode()
REF_NONE				= 0			# Без упоминаний
REF_NAME				= 1			# Добавить имя
REF_FULLNAME			= 2			# Полное имя
REF_NICKNAME			= 4
REF_LINK				= 8			# Добавить упоминание

# для IMessenger.type()
TYPE_VK					= 0
TYPE_DISCORD			= 1

# для внутреннего использования в IMessage.attach():
ATT_TEXT				= "txt"			# str
ATT_IMAGES				= "img"			# list: [(url, description), ...]
ATT_AUDIOS				= "snd"			# list								# !!! Для Discord нет смысла реализовывать
ATT_DOCS				= "doc"			# list								# !!! Не реализовано для Discord'а
ATT_FORWARDS			= "fwd"			# list								# !!! Для Discord невозможно реализовать

IMAGE_URL				= 0
IMAGE_DESC				= 1

GENDER_NOT_SPECIFIED	= 0
GENDER_MAN				= 0
GENDER_WOMAN			= 1

# ======== ========= ========= ========= ========= ========= ========= =========

class IMessenger:
	def __init__(self):
		pass

	def msg(self, target):
		# создает объект для отправки сообщений
		pass

	def is_running(self):
		pass

	def run(self):										# Аргументы не добавлять
		pass
	
# ======== ========= ========= ========= ========= ========= ========= =========

class IMessage:
	def is_me(self, obj):
		pass

	def type(self):
		# Должен вернуть ID используемого мессенджера (см. начало файла)
		pass

	# @property
	def id(self):
		pass

	# @property
	def chat_id(self):
		pass

	# @property
	def text(self):
		pass

# ======== ========= ========= ========= ========= ========= ========= =========

class Answer:
	def __init__(self, user, msg):
		self.stats	= None
		self.user	= user
		self.msg	= msg
		self._att	= {}				# Список attachments
		self._ref	= REF_NONE
		self._reply = False

	def is_ready(self):
		return len(self._att) != 0

	# Mode - добавлять упоминания (см. начало файла)
	def set_reference_mode(self, mode):
		self._ref = mode

	def set_reply(self, flag=True):
		self._reply = flag

	def attach(self, **kwargs):
		for key in kwargs:
			if key not in self._att:
				if len(kwargs[key]) != 0:
					self._att[key] = kwargs[key]
			elif kwargs[key] not in self._att[key]:
				self._att[key] += kwargs[key]

# ======== ========= ========= ========= ========= ========= ========= =========

class IUserProfile:
	# @property
	def id(self):
		pass

	def ref(self, ref_type):
		pass

	# @property
	def gender(self):
		pass

# ======== ========= ========= ========= ========= ========= ========= =========
