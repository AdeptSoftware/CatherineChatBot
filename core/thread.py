# 13.11.2018
import threading
import time

# ======== ========= ========= ========= ========= ========= ========= =========

# заглушки
def _default_on_exit_handler(): pass
def _default_on_error_handler(data=None): print("Error: " + str(data))

# Глобальные обработчики событий:
G_ON_THREAD_EXIT = _default_on_exit_handler
G_ON_ERROR = _default_on_error_handler

# ======== ========= ========= ========= ========= ========= ========= =========

def run_thread(fn, name=None):
    thread = threading.Thread(target=fn, name=name, daemon=True)
    thread.start()
    return thread

# ======== ========= ========= ========= ========= ========= ========= =========

# Своего рода абстрактный базовый класс потоков
class BaseThread:
    # time_update - задержка (sec) между вызовами on_update и выхода из потока при вызове stop()
    def __init__(self, name, time_update=1):
        self._time_update   = time_update
        self.__name__       = name
        self._thread        = None
        self._exit          = False

    def on_update(self):
        pass

    @staticmethod
    def on_exit():
        G_ON_THREAD_EXIT()

    @staticmethod
    def on_error(data=None):
        G_ON_ERROR(data)

    def run(self):
        try:
            # Запустим поток, если он не существует
            if self._thread and self._thread.is_alive():
                return True
            self._exit = False
            if self._thread is None or not self._thread.is_alive():
                self._thread = run_thread(self._run, self.__name__)
                return True
        except Exception as err:
            self.on_error(err)
        self._exit = True
        return False

    def stop(self):
        self._exit = True

    def _run(self):
        while not self._exit:
            try:
                self.on_update()
            except Exception as err:
                self.on_error(err)
            time.sleep(self._time_update)
        self.on_exit()

# ======== ========= ========= ========= ========= ========= ========= =========
