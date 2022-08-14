#
from core.updater           import SafeVariable
from core.commands.context  import Context
import time

# ======== ========= ========= ========= ========= ========= ========= =========

# Типы доступа пользователей к команде
ACCESS_PERSONAL             = 0             # Отвечает каждому по отдельности
ACCESS_ALL_AT_ONCE          = 1             # Отвечает всем сразу
ACCESS_OCCUPIED             = 2             # Отвечает только одному
ACCESS_MODERATOR            = 3             # Отвечает только модерам
ACCESS_ADMIN                = 4             # Отвечает только админам

# Типы готовности команды
COMMAND_ACCESS_DENIED       = -1            # Команда не доступна (исп. и тд)
COMMAND_COOLDOWN            = 0             # Команда на откате
COMMAND_LIMIT               = 1             # Достигнут лимит по использованию
COMMAND_READY               = 2             # Команда доступна
COMMAND_READY_AND_USED      = 3             # ... и была использована ранее

# ======== ========= ========= ========= ========= ========= ========= =========

_COMMANDS = []  # Общий список команд, доступный всем мессенджерам

# регистрирует команду
def add(cmd):
    global _COMMANDS
    _COMMANDS += [SafeVariable(cmd)]

# создает новую командую
def new(condition, answer, cooldown=0, limit=0, access_type=0, remember_time=60, name="", nodes=None):
    root = CommandNode(condition, answer, cooldown, limit, nodes)
    add(Command(root, access_type, remember_time, name))

# Возвращает список команд
def get_commands():
    return _COMMANDS

# ======== ========= ========= ========= ========= ========= ========= =========

class CommandNode:
    # condition - функция вида: fn(ctx)->boolean
    # answer - имя строки в базе строк или функция обработчик вида: fn(ctx)->boolean
    def __init__(self, condition, answer, cooldown=0, limit=0, nodes=None):
        self._cooldown              = cooldown
        self._limit                 = limit
        self._condition             = condition
        self._answer                = answer
        self._nodes                 = nodes or [self]

        self._has_string_key_answer = type(answer) is str

    @property
    def cooldown(self):
        return self._cooldown

    @property
    def limit(self):
        return self._limit

    def check(self, ctx):
        return self._condition(ctx)

    def find(self, ctx):
        """ Поиск CommandNode, который даст ответ на сообщение

        :param ctx: :class: `core.commands.context.Context`
        :return: None or CommandNode object
        """
        for node in self._nodes:
            if node.check(ctx):
                return node
        if self.check(ctx):
            return self
        return None

    def get(self, ctx):
        """
        :param ctx: :class: `core.commands.context.Context`
        :return: Возвращает строку-ответ
        """
        if self._has_string_key_answer:
            ctx.ans.set_text(ctx.app.lang.rnd(self._answer))
            return True
        return self._answer(ctx)

# ======== ========= ========= ========= ========= ========= ========= =========

class Command:
    def __init__(self, node, access_type=0, remember_time=60, name=""):
        """
        :param node: :class: `core.commands.command.CommandNode`
        :param access_type: тип доступа пользователя к команде
        :param remember_time: сколько секунд команда будет запомненной
        :param name: имя команды
        """
        self._access_type   = access_type       # см. в начале файла
        self.__name__       = name
        self._remember_time = remember_time
        self._node          = node

    @property
    def access_type(self):
        return self._access_type

    @property
    def remember_time(self):
        return self._remember_time

    @property
    def name(self):
        return self.__name__

    def find(self, ctx):
        return self._node.find(ctx)

# Безопасно управляет командами, отслеживает действия пользователей
class SVCommand:
    def __init__(self, cmd: SafeVariable):
        self._user_list     = SafeVariable({})
        self._cmd           = cmd

    def has_access(self, user_access_type):
        """ Проверка уровня доступа пользователя к команде """
        with self._cmd:
            if self._cmd.access_type == ACCESS_ADMIN:
                return user_access_type >= ACCESS_MODERATOR
            if self._cmd.access_type == ACCESS_MODERATOR:
                return user_access_type == ACCESS_MODERATOR
            flag = self._cmd.access_type == ACCESS_OCCUPIED
        if flag:
            with self._user_list:
                return len(self._user_list) == 0
        return True

    def update(self, now):
        deleted = []
        with self._cmd:
            rt = self._cmd.remember_time
        with self._user_list:
            for user_id in self._user_list:
                if now >= self._user_list[user_id][1]+rt:
                    deleted += [user_id]
            for user_id in deleted:
                self._user_list.pop(user_id)

    def status(self, now, user_id):
        """ Проверка статуса команды для текущего пользователя

        :param now: текущее время (timestamp)
        :param user_id: ID пользователя
        :return: Код-статус, обозначающий готовность команды
        """
        with self._cmd:
            flag1 = self._cmd.access_type == ACCESS_OCCUPIED
            if self._cmd.access_type == ACCESS_ALL_AT_ONCE:
                user_id = 0
        with self._user_list:
            if user_id in self._user_list:
                node, t, count = self._user_list[user_id]
                if node.limit and count > node.limit:
                    return COMMAND_LIMIT
                if node.cooldown and now < t+node.cooldown:
                    return COMMAND_COOLDOWN
                return COMMAND_READY_AND_USED
            elif flag1 and len(self._user_list) > 0:
                return COMMAND_ACCESS_DENIED
            return COMMAND_READY

    def check(self, ctx: Context):
        """ Поиск ответа среди команд """
        count = 0
        from_id = 0
        with self._cmd:
            if self._cmd.access_type != ACCESS_ALL_AT_ONCE:
                from_id = ctx.msg.from_id()
        with self._user_list:
            flag2 = from_id not in self._user_list
            if not flag2:
                node  = self._user_list[from_id][0].find(ctx)
                count = self._user_list[from_id][1]
        if flag2:
            with self._cmd:
                node = self._cmd.find(ctx)
        if node and node.get(ctx):
            with self._user_list:         # [0]       [1]        [2]
                self._user_list[from_id] = (node, time.time(), count+1)        #
            return True
        return False

""" # В более привычном виде. Переделал, чтобы исключить возможность блокировки
        from_id = 0
        with self._cmd:
            access_type = self._cmd.access_type
        if access_type != ACCESS_ALL_AT_ONCE:
            from_id = ctx.msg.from_id()
        with self._user_list:
            if from_id not in self._user_list:
                with self._cmd:                                         # здесь
                    node = self._cmd.find(ctx)
                    count = 0
            else:
                node  = self._user_list[from_id][0].find(ctx)
                count = self._user_list[from_id][1]
            if node and node.get(ctx):    # [0]       [1]        [2]
                self._user_list[from_id] = (node, time.time(), count+1)        #
        return None
"""

# ======== ========= ========= ========= ========= ========= ========= =========
