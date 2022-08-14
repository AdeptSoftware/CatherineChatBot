# Заготовка под центр управлением командами
from core.commands.context        import Context

# ======== ========= ========= ========= ========= ========= ========= =========

class CommandManager:
    def __init__(self, updater, configs):
        self._chats      = {}
        for key in configs["targets"]:
            self._chats[int(key)] = None

        updater.append(self._update)

    async def _update(self):
        return True

    def is_allowed_chat(self, chat_id):
        return chat_id in self._chats

    def on_message(self, ctx: Context):
        ctx.ans.set_text(ctx.msg.text)
        return True
