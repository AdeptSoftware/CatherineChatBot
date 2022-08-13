#
from core.messenger.message import AbstractMessage

# ========= ========= ========= ========= ========= ========= ========= =========

class DiscordMessage(AbstractMessage):
    def __init__(self, ctx, bot_id):
        super().__init__()
        self._me   = bot_id
        self._ctx  = ctx
        self._fwd  = []                  # Не поддерживается

    def is_me(self):
        return self._me == self._ctx.author.id

    @property
    def msg_id(self):
        return self._ctx.id

    @property
    def chat_id(self):
        return self._ctx.channel.id

    @property
    def from_id(self):
        return self._ctx.author.id

    @property
    def text(self):
        return self._ctx.content

    @property
    def fwd(self):
        return self._fwd

# ========= ========= ========= ========= ========= ========= ========= =========
