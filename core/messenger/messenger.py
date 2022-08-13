# Производные классы предназначены для организации цикла сообщений
from core.commands.manager import CommandManager
from core.commands.context import ContextEx

# ======== ========= ========= ========= ========= ========= ========= =========

# Message Types:
TYPE_VK					= 0
TYPE_DISCORD			= 1

# ======== ========= ========= ========= ========= ========= ========= =========

class AbstractMessenger:
    def __init__(self, data, configs):
        self._ctx = ContextEx(
            CommandManager(data.updater, configs),
            self,
            data
        )

    # Уникальный идентификатор (см. выше: Message Types)
    def type_id(self):
        pass

    # Аргументы не добавлять!
    async def run(self):
        return False

    def create_answer(self, chat_id):
        pass

    def send(self, obj):
        pass

# ========= ========= ========= ========= ========= ========= ========= =========
