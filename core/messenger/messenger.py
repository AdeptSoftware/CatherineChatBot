# Производные классы предназначены для организации цикла сообщений
from core.commands.manager import CommandManager, Context

# ======== ========= ========= ========= ========= ========= ========= =========

# Message Types:
TYPE_VK					= 0
TYPE_DISCORD			= 1

# ======== ========= ========= ========= ========= ========= ========= =========

class AbstractMessenger:
    def __init__(self, configs):
        self._mngr      = CommandManager(configs)
        self._configs   = configs
        self._context   = None

    def type_id(self):
        pass

    def run(self):  # Аргументы не добавлять
        pass

    def create_answer(self, chat_id):
        pass

    def set_appdata(self, appdata):
        if self._context is None:
            self._context = Context(appdata, self)

    def send(self, obj):
        pass

# ========= ========= ========= ========= ========= ========= ========= =========
