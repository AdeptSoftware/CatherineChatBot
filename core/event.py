# Классы для работы с событиями
import core.thread
import core.safe
import time

# ======== ========= ========= ========= ========= ========= ========= =========

# Выполняет различные задачи (отправку сообщений и тд) сразу по возможности
# Необходим, если задачи нужно выполнять с некоторой задержкой между ними
class TaskManager(core.thread.BaseThread):
    def __init__(self, name, time_update=0.5):
        super().__init__(name, time_update)
        self._queue = core.safe.SafeVariable([])
        self._last = None

    def stop(self):
        with self._queue:
            self._queue.clear()
        super().stop()

    def append(self, fn, obj):
        with self._queue:
            self._queue += [(fn, obj)]

    def on_update(self):
        with self._queue:
            if len(self._queue) > 0:
                self._last = self._queue.pop(0)
                self._call(self._last[0], self._last[1])

    def _call(self, fn, obj):
        self._last[0](self._last[1])

# ======== ========= ========= ========= ========= ========= ========= =========

# Выполняет различные задачи в заданное время с определенным интервалом
# В вызываемой функции возможна корректировка значений (кроме "next", т.к. оно рассчитывается позже)
class EventManager(core.thread.BaseThread):
    def __init__(self, name, time_update=1):
        super().__init__(name, time_update)
        self._events = core.safe.SafeVariable({})

    def stop(self):
        with self._events:
            self._events.clear()
        super().stop()

    def set_update_time(self, sec):
        if sec > 0:
            self._time_update = sec

    # name - уникальное имя события (если такое есть - перезапишется)
    # cooldown - время между событиями (sec)
    # delay - когда следующий вызов события (через сколько sec)
    # fn - функция-обработчик (Если вернет False - событие будет удалено)
    # fn принимает в качестве аргумента словарь с ключами:
    # "fn", "data", "cooldown", "next"
    # data - дополнительные данные
    def new_ex(self, name, fn, delay, cooldown, data=None):
        if delay < 0 or cooldown <= 0:
            return False

        with self._events:
            # Оборачиваем в SafeVariable, чтобы безопасно использовать get()
            self._events[name] = core.safe.SafeVariable({
                "fn":       fn,
                "data":     data,
                "cooldown": cooldown,
                "next":     time.time() + delay
            })
        return True

    def new(self, fn, obj):
        return self.new_ex(obj["name"], fn, obj["delay"], obj["cooldown"], obj["data"])

    def delete(self, name):
        with self._events:
            if name in self._events.value:
                self._events.pop(name)
                return True
        return False

    # Пример использования полученного события:
    # with event: event["fn"](event.value)
    def get(self, name):
        with self._events:
            if name in self._events.value:
                return self._events[name]
        return None

    # будет применено после следующего вызова события
    def set_cooldown(self, name, cooldown):
        if cooldown <= 0:
            return False

        with self._events:
            if name in self._events.value:
                event = self._events[name]
                with event:
                    event.value["cooldown"] = cooldown
                    return True
        return False

    def keys(self):
        with self._events:
            return self._events.keys()

    def on_update(self):
        deleted = []
        now = time.time()
        with self._events:
            for name in self._events.value:
                event = self._events[name]
                with event:
                    if now >= event["next"]:
                        if not event["fn"](event.value):
                            # Удаляем события, которые вернули False
                            deleted += [name]
                        else:
                            event["next"] = now + event["cooldown"]
            if deleted:
                for name in deleted:
                    self._events.pop(name)

# ======== ========= ========= ========= ========= ========= ========= =========
