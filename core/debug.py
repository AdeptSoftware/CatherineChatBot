# 26.05.2022 Объект-singleton. Для вывода логов и ошибок
import core.updater
import traceback
import sys

from core.xtime import time

# ======== ========= ========= ========= ========= ========= ========= =========

_G_OUTPUT_CONSOLE = True  # Дополнительно выводить логи в консоль
_G_DEBUG          = None  # None - не инициализировано/без debug-режима

# ======== ========= ========= ========= ========= ========= ========= =========

class _Debug:
    def __init__(self, storage_object):
        self._so    = storage_object
        self._last  = None

    # Выводит текст в логи
    def log(self, text, ignore_console=False):
        text = time().strftime("[%Y-%m-%d %H:%M:%S]: ") + text
        try:
            out = self._so.get()
            with out:
                out += text + '\n'
            self._so.backup()
            if not _G_OUTPUT_CONSOLE or ignore_console:
                return
        except Exception as exc:
            text += "\n" + str(exc)
        print(text)

    # Собираем всю доступную информацию и сохраняет в логах
    # Если ошибка повторилась, то повторной отправки не будет
    def err(self, data=None):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        string = str(exc_value) + "\n"
        for frame in traceback.extract_tb(exc_traceback):
            index = frame.filename.rfind('\\')
            string += "=> {0}.{1}():{2} ".format(frame.filename[index + 1:-3], frame.name, frame.lineno)
        if self._last == string:
            return
        self._last = string
        if data:
            data = str(data)
            if data not in string:
                string += str(data)
        self.log(string + '\n')

# ======== ========= ========= ========= ========= ========= ========= =========

def init(storage_object):
    global _G_DEBUG
    if _G_DEBUG is None:
        _G_DEBUG = _Debug(storage_object)
        # установка обработчиков ошибок
        core.updater.G_ON_ERROR = _G_DEBUG.err


def get():
    return _G_DEBUG

# ======== ========= ========= ========= ========= ========= ========= =========
