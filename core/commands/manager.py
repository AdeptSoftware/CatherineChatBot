# Заготовка под центр управлением командами
from core.commands.chat_manager   import ChatManager
from core.commands.resentment     import ResentmentController
from core.commands.context        import Context
import time

# ======== ========= ========= ========= ========= ========= ========= =========

class CommandManager:
    def __init__(self, updater, configs):
        self._resentment = ResentmentController(configs["resentment"])
        self._chats      = {}
        for key in configs["targets"]:
            self._chats[int(key)] = ChatManager(configs["targets"][key])

        updater.append(self._update)

    async def _update(self):
        now = time.time()
        self._resentment.update(now)
        for key in self._chats:
            for cmd in self._chats[key].commands:
                with cmd:
                    cmd.update(now)
        return True

    def is_allowed_chat(self, chat_id):
        return chat_id in self._chats

    def on_message(self, ctx: Context):
        # for cmd in self._chats[ctx.msg.chat_id]: return cmd.check(ctx)
        ctx.ans.set_text(ctx.msg.text)
        return True
