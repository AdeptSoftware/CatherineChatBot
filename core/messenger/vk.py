# 24.05.2022-27.05.2022
import core.commands.manager	as _mgr
import core.event				as _e
from core.messenger.cls			import *
from vk_api.bot_longpoll		import VkBotLongPoll, VkBotEventType
import vk_api

# ======== ========= ========= ========= ========= ========= ========= =========

MIN_CHAT_ID	 = 2000000000
MAX_MSG_SIZE = 4000		# 4096	# Больше этого значения сообщения просто не выводятся и не вызывают ошибку
MAX_ATT_SIZE = 10

# ======== ========= ========= ========= ========= ========= ========= =========

class VkUserProfile(IUserProfile):
	def __init__(self, caller, user_id):
		self._caller	= caller
		self._id		= user_id
		self._data		= None

	@property
	def id(self):
		return self._id

	def ref(self, ref_type):
		result = ""
		if ref_type != REF_NONE:
			self._update()
			if ref_type == REF_NAME:
				result = self._data["first_name"]
			elif ref_type == REF_FULLNAME:
				result = self._data["first_name"]+' '+self._data["last_name"]
			elif ref_type == REF_NICKNAME:
				result = "?"
			if result and ref_type == REF_LINK:
				return "[{0}|{1}]".format(self._id, result)
		return result

	@property
	def gender(self):
		self._update()
		return self._data["sex"]
		
	# загрузка данных, если их нет
	def _update(self):
		if not self._data:
			params = {
				"user_ids":		self._id,
                "fields":		"domain,sex,online,can_write_private_message,city",
                "name_case":	"nom"
			}
			self._data = self._caller.call("users.get", params)[0]


# ======== ========= ========= ========= ========= ========= ========= =========

# Хранит данные о текущем сообщении
class VkMessage(IMessage):
	def __init__(self, item, group_id):
		self._group_id = group_id
		self._item = item

	@property
	def text(self):
		return self._item["text"]

	@property
	def id(self):
		return self._item["conversation_message_id"]

	@property
	def chat_id(self):
		return self._item["peer_id"]	# лучше передать peer_id

	def is_me(self, user_id):
		return self._group_id == user_id

	def type(self):
		return TYPE_VK

# ======== ========= ========= ========= ========= ========= ========= =========

class VkAnswer(Answer):
	def __init__(self, caller, item, group_id):
		self._caller = caller
		super().__init__(VkUserProfile(self._caller, item["from_id"]), 
						 VkMessage(item, group_id))

	def send(self, text=""):
		params = {"random_id": 0, "peer_id": self.msg.chat_id, "dont_parse_links": True,
				  "attachment": []}
		# Подготовка текста
		if ATT_TEXT in self._att:
			text = self._att[ATT_TEXT] + text
		params["message"] = text
		if len(text) > MAX_MSG_SIZE:
			params["message"] = params["message"][:MAX_MSG_SIZE] + "..."
		# Подготовка прикрепленного контента
		# <type><owner_id>_<media_id>_<access_key>
		# Приоретет: документы > аудио > изображения
		if ATT_DOCS in self._att:
			params["attachment"] += self._att[ATT_DOCS]
		_max = MAX_ATT_SIZE-len(params["attachment"])
		if _max > 0:
			images = audios = 0
			if ATT_AUDIOS in self._att:
				audios = len(self._att[ATT_AUDIOS])
			if ATT_IMAGES in self._att:
				images = len(self._att[ATT_IMAGES])
				if audios+images <= _max:	# Добавление всех изображений или музыки
					params["attachment"] += self._att[ATT_IMAGES]
				elif audios >= _max:		# Много аудио, то хотя бы 1 изображение
					params["attachment"] += [self._att[ATT_IMAGES][0]]
				else:						# Заполним изображениями до краёв
					params["attachment"] += self._att[ATT_IMAGES][:_max-audios]
			if audios:
				params["attachment"] += self._att[ATT_AUDIOS]
			if len(params["attachment"]) > MAX_ATT_SIZE:
				params["attachment"] = params["attachment"][:_max]
		params["attachment"] = ','.join(params["attachment"])
		# Прикрепленные сообщения
		fwd = ""
		if ATT_FORWARDS in self._att:
			fwd += ','.join(self._att[ATT_FORWARDS])
		if self._reply and (not fwd or self._mid not in self._att[ATT_FORWARDS]):
			if fwd:
				fwd += ','
			fwd += str(self.msg.id)
		if fwd:
			obj = {
				"peer_id":					self.msg.chat_id,
				"conversation_message_ids": fwd
			}
			params["forward"] = json.dumps(obj)
		# Отправка в очередь
		self._caller.append("messages.send", params)

# ======== ========= ========= ========= ========= ========= ========= =========

class VkMethodCaller(_e.TaskManager):
	def set_api(self, api):
		self._api = api

	# вызов функции прямо сейчас, вклинившись в поток
	# не встаёт в очередь, но позволяет обращаться, например, к API последовательно из разных потоков
	# К тому же позволяет получать возвращаемые значения от функций
	def call(self, method, params):
		with self._queue:
			return self._call(method, params)
		return None

	def _call(self, method, params):
		return self._api.method(method, params)


class VkMessenger(IMessenger):
	def __init__(self, cfg):
		super().__init__()
		self._caller	= VkMethodCaller("vk", cfg["delay"])
		self._mgr		= _mgr.CommandManager(cfg["dialogs"])
		self._on		= False
		self._cfg		= cfg

	def msg(self, peer_id):
		item = {
			"conversation_message_id":	0,
			"from_id":					0,
			"peer_id":					peer_id,
			"text":						""
		}
		return VkAnswer(self._caller, item, self._cfg["id"])

	def on_message(self, item):
		# Если сообщение не из разрешенного чата
		if str(item["peer_id"]) not in self._cfg["dialogs"]:
			return
		# Если сообщение не от сообщества/бота/нас
		if item["from_id"] < 0:
			return
		# Собственно поиск команды/фразы-ответа
		ans = VkAnswer(self._caller, item, self._cfg["id"])
		if self._mgr.on_message(ans):
			ans.send()

	def run(self):
		if self._on:
			return
		try:
			_api = vk_api.VkApi(token=self._cfg["token"])
			_api.api_version = "5.131"
			longpoll = VkBotLongPoll(_api, -self._cfg["id"], self._cfg["wait"])
			self._on = True
			self._caller.set_api(_api)
			self._caller.run()
		except Exception as err:
			self._on = False
			raise err
		while self._on:
			for event in longpoll.listen():
				if event.type == VkBotEventType.MESSAGE_NEW:
					if event.from_chat:
						self.on_message(event.obj.message)

	def is_running(self):
		return self._on

# ======== ========= ========= ========= ========= ========= ========= =========
