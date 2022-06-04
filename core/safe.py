# 25.05.2022 Потокобезопасная переменная
import threading

# ======== ========= ========= ========= ========= ========= ========= =========

# Пример
# x = SafeVariable(0)
# with x:
#   x.value += 2

# acquire и release - вызываются всегда, даже при ошибках (но их все равно лучше обрабатывать)
class SafeVariable:
    def __init__(self, value):
        self.value = value
        self._lock = threading.RLock()

    def __enter__(self):
        self._lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()

    def __call__(self):
        return self.value

# ======== ========= ========= ========= ========= ========= ========= =========
