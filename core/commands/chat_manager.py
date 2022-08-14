# Управляет беседой и выдает информацию о ней
from core.commands.command import SVCommand, get_commands

# ========= ========= ========= ========= ========= ========= ========= =========

class ChatManager:
    def __init__(self, configs):
        self._commands      = None
        self._ignored       = None
        self._admins        = configs["admins"]
        self._blacklist     = configs["blacklist"]
        self._moderators    = configs["moderators"]

        self._init_commands(configs["!cmd"])

    def _init_commands(self, ignored):
        _list = []
        _cmds = get_commands()
        if ignored is not None:                     # Иначе игнорируем всё!
            for cmd in _cmds:
                flag = cmd.name in ignored          # Не игнорируем ничего!
                if ignored is None or not flag:
                    _list += [SVCommand(cmd)]
                if flag:
                    ignored.remove(cmd.name)
        else:
            ignored = []
        self._commands = tuple(_list)
        self._ignored  = tuple(ignored)

    def is_ignored_cmd(self, name):
        return name in self._ignored

    def is_blacklist_user(self, user_id):
        return user_id in self._blacklist

    def get(self):
        return {
            "admins":       self._admins.copy(),
            "blacklist":    self._blacklist.copy(),
            "moderators":   self._moderators.copy()
        }

    # Можно только установить, но не снять
    def admin(self, user_id):
        if user_id not in self._admins:
            self._admins += [user_id]

    def moderator(self, user_id, delete=False):
        if delete:
            if user_id in self._moderators:
                self._moderators.remove(user_id)
        else:
            if user_id not in self._moderators:
                self._moderators += [user_id]

    #
    def blacklist(self, user_id, cause=None):
        """ Добавление/Удаление пользователя из черного списка

        :param user_id: ID пользователя
        :param cause: строка, если не задана, то удаление пользователя из черного списка
        """
        if cause is None:
            if user_id in self._blacklist and \
               self._moderators[user_id] is not None:
                self._moderators.pop(user_id)
            # Если self._moderators[user_id] is None - то это вечный блок
            # Можно добавить/удалить только через редактирование файла
        else:
            if user_id not in self._blacklist:
                self._moderators[user_id] = cause

    @property
    def commands(self):
        return self._commands

# ========= ========= ========= ========= ========= ========= ========= =========