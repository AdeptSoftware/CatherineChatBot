#
from core.messenger.messenger           import AbstractMessenger, TYPE_VK
from core.event				            import TaskManager

from core.messenger.vk.message          import VkMessage
from core.messenger.vk.answer           import VkAnswer

from vk_api.bot_longpoll		        import VkBotLongPoll, VkBotEventType
import vk_api

# ======== ========= ========= ========= ========= ========= ========= =========

class _VkMethodCaller(TaskManager):
    def __init__(self, name, time_update=0.5):
        super().__init__(name, time_update)
        self._api = None

    def set_api(self, api):
        self._api = api

    # вызов функции прямо сейчас, вклинившись в поток
    # не встаёт в очередь, но позволяет обращаться, например, к API последовательно из разных потоков
    # К тому же позволяет получать возвращаемые значения от функций
    def call(self, method, params):
        with self._queue:
            return self._call(method, params)

    def _call(self, method, params):
        return self._api.method(method, params)

# ======== ========= ========= ========= ========= ========= ========= =========

class VkMessenger(AbstractMessenger):
    def __init__(self, configs):
        super().__init__(configs)
        self._caller = _VkMethodCaller("vk", configs["delay"])

    @property
    def type_id(self):
        return TYPE_VK

    def create_answer(self, chat_id):
        return VkAnswer(chat_id)

    def run(self):
        _api = vk_api.VkApi(token=self._configs["token"])
        _api.api_version = "5.131"
        longpoll = VkBotLongPoll(_api, -self._configs["id"], self._configs["wait"])
        self._caller.set_api(_api)
        self._caller.run()

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_chat:
                    self._on_message(event.obj.message)

    def _on_message(self, item):
        # Если сообщение не из разрешенного чата
        if str(item["peer_id"]) not in self._configs["targets"]:
            return
        # Если сообщение не от сообщества/бота/нас
        if item["from_id"] < 0:
            return
        # Собственно поиск команды/фразы-ответа
        self._context.set(VkMessage(item, -self._configs["id"]),
                          VkAnswer(item["peer_id"], item["conversation_message_id"]))
        if self._mngr.on_message(self._context):
            self.send(self._context.ans.get())

    def send(self, obj):
        self._caller.call("messages.send", params=obj)

# ========= ========= ========= ========= ========= ========= ========= =========
