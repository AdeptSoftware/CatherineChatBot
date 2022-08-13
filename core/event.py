# Классы для работы с событиями
import core.updater as _upd
import time

# ======== ========= ========= ========= ========= ========= ========= =========

# Выполняет различные задачи в заданное время с определенным интервалом
# В вызываемой функции возможна корректировка значений (кроме "next", т.к. оно рассчитывается позже)
class EventManager:
    def __init__(self, updater, delay=15):
        self._events = _upd.SafeVariable({})
        self._delay  = delay
        updater.append(self._update)

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
            self._events[name] = _upd.SafeVariable({
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

    async def _update(self):
        while True:
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
            await _upd.sleep(self._delay)

# ======== ========= ========= ========= ========= ========= ========= =========
