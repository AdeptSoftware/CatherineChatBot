# Класс, обновляющий различные данные
import threading
import asyncio

# ======== ========= ========= ========= ========= ========= ========= =========

# Пример
# x = SafeVariable(0)                       x = SafeVariable([2, 3, 5])
# with x:                                   with x:
#   x += 2                                      x += [7, 11, 13]
# print(x.value)                    или     print(x())

# Не поддерживает итерацию объектов (используйте SafeVariable.value)
class SafeVariable:
    def __init__(self, value):
        self.value = value
        self._lock = threading.RLock()

    # ==== ========= ========= ========= ========= ========= ========= =========
    # Эти функции вызываются всегда, даже при ошибках

    def __enter__(self):
        self._lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()

    # ==== ========= ========= ========= ========= ========= ========= =========

    def __str__(self):
        return str(self.value)

    # ==== ========= ========= ========= ========= ========= ========= =========

    def __call__(self):
        return self.value

    def __getattr__(self, item):
        return self.value.__getattribute__(item)

    # ==== ========= ========= ========= ========= ========= ========= =========

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, value):
        self.value[key] = value

    def __len__(self):
        return len(self.value)

    # ==== ========= ========= ========= ========= ========= ========= =========

    def __add__(self, other):
        self.value += other
        return self

    def __radd__(self, other):
        self.value = other + self.value
        return self

    # Другие операции добавлю по мере необходимости...

# ======== ========= ========= ========= ========= ========= ========= =========

async def sleep(sec):
    await asyncio.sleep(sec)

def _default_on_error_handler(data=None): print("Error: " + str(data))

# Глобальные обработчики событий:
G_ON_ERROR = _default_on_error_handler

# ======== ========= ========= ========= ========= ========= ========= =========

class Updater:
    def __init__(self, delay=1):
        self._tasks     = SafeVariable([])
        self._delay     = delay
        self._loop      = asyncio.new_event_loop()
        self._exit      = True

    # Запуск будет осуществлен в текущем потоке
    def run(self):
        if self._exit:
            self._exit = False
            self._loop.run_until_complete(self._updater())

    async def _updater(self):
        while True:
            deleted = []
            with self._tasks:
                for task in self._tasks:
                    if self._exit:
                        return
                    if task[1]:     # isn't working?
                        task[1] = None
                        asyncio.create_task(self._caller(task))
                    elif task[1] is not None:
                        deleted += [task]
                for task in deleted:
                    self._tasks.remove(task)
            await asyncio.sleep(self._delay)

    async def _caller(self, task):
        try:
            task[1] = await task[0]()
        except Exception as err:
            task[1] = await self.on_error(err)

    @staticmethod
    async def on_error(data=None):
        G_ON_ERROR(data)
        await asyncio.sleep(1)
        return False

    def stop(self):
        self._exit = True
        # Завершится поток немного позже

    @property
    def loop(self):
        return self._loop

    # callback должен быть async функцией и возвращать True/False
    # True - использовать повторно. False - удалить из списка
    def append(self, callback):
        with self._tasks:
            self._tasks += [[callback, True]]

# ======== ========= ========= ========= ========= ========= ========= =========
