# Заготовка под центр управлением командами
from core.commands.context import Context

class CommandManager:
    def __init__(self, configs):
        pass

    def on_message(self, ctx: Context):
        ctx.ans.set_text(ctx.msg.text)
        return True
