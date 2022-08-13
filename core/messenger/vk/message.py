#
from core.messenger.message import AbstractMessage

# ========= ========= ========= ========= ========= ========= ========= =========

class VkMessage(AbstractMessage):
    def __init__(self, item, group_id, fwd=True):
        super().__init__()
        self._group_id  = group_id
        self._item      = item
        self._fwd       = []

        if fwd:
            if "reply_message" in item:
                self._fwd += [VkMessage(item["reply_message"], group_id, False)]
            elif "fwd_messages" in item:
                for msg in item["fwd_messages"]:
                    self._fwd += [VkMessage(msg, group_id, False)]
            self._fwd  = tuple(self._fwd)

    def is_me(self):
        return self._group_id == self._item["from_id"]

    @property
    def msg_id(self):
        return self._item["conversation_message_id"]

    @property
    def chat_id(self):
        return self._item["peer_id"]	# лучше передать peer_id

    @property
    def from_id(self):
        return self._item["from_id"]

    @property
    def text(self):
        return self._item["text"]

    @property
    def fwd(self):  # Пересланные сообщения
        return self._fwd

# ========= ========= ========= ========= ========= ========= ========= =========
