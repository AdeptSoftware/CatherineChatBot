#
from core.messenger.messenger           import AbstractMessenger, TYPE_VK
from core.messenger.vk.message          import VkMessage
from core.messenger.vk.answer           import VkAnswer

from core.wrappers.vk_async_longpoll    import AsyncVkLongPoll, VkBotEventType
from core.updater                       import SafeVariable
from vk_api                             import VkApi

# ======== ========= ========= ========= ========= ========= ========= =========

class _VkMethodCaller:
    def __init__(self, updater, token, group_id, wait, version="5.131"):
        updater.append(self._update)
        self._queue     = SafeVariable([])
        self._api       = VkApi(token=token, api_version=version)
        self._longpoll  = AsyncVkLongPoll(self._api, group_id, wait)

    def longpoll(self):
        return self._longpoll

    def send(self, obj):
        with self._queue:
            self._queue += [("messages.send", obj)]

    async def _update(self):
        with self._queue:
            if len(self._queue) > 0:
                _last = self._queue.pop(0)
                self._method(_last[0], _last[1])
        return True

    # вызов функции прямо сейчас, вклинившись в поток
    # не встаёт в очередь, но позволяет обращаться, например, к API последовательно из разных потоков
    # К тому же позволяет получать возвращаемые значения от функций
    def call(self, method, params):
        with self._queue:
            return self._method(method, params)

    def _method(self, method, params):
        return self._api.method(method, params)

# ======== ========= ========= ========= ========= ========= ========= =========

class VkMessenger(AbstractMessenger):
    def __init__(self, data, configs):
        super().__init__(data, configs)
        self._group_id  = -configs["id"]
        self._api       = _VkMethodCaller(data.updater,   configs["token"],
                                          -configs["id"], configs["wait"])

    @property
    def type_id(self):
        return TYPE_VK

    def create_answer(self, chat_id):
        return VkAnswer(chat_id)

    async def run(self):
        longpoll = self._api.longpoll()
        async for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_chat:
                    self._on_message(event.obj.message)
        return True

    def _on_message(self, item):
        # Если сообщение не из разрешенного чата и не от сообщества/бота/нас
        if not self._ctx.mngr.is_allowed_chat(item["peer_id"]) or item["from_id"] < 0:
            return
        # Собственно поиск команды/фразы-ответа
        self._ctx.set_message(VkMessage(item, self._group_id))
        self._ctx.set_answer(VkAnswer(item["peer_id"], item["conversation_message_id"]))
        if self._ctx.mngr.on_message(self._ctx):
            self.send(self._ctx.ans.get())

    def send(self, obj):
        self._api.send(obj)

# ========= ========= ========= ========= ========= ========= ========= =========
