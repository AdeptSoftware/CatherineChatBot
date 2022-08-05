# Этот класс включает в себя все основные объекты, обеспечивающие его работу

class Context:
    def __init__(self, appdata, msgr):
        self._app   = appdata
        self._msgr  = msgr
        self._msg   = None
        self._ans   = None

    def set(self, msg, ans):
        self._msg   = msg
        self._ans   = ans

    @property
    def app(self):
        return self._app

    @property
    def msg(self):
        return self._msg

    @property
    def ans(self):
        return self._ans

    @property
    def messenger(self):
        return self._msgr

# ========= ========= ========= ========= ========= ========= ========= =========
