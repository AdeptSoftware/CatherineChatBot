# Управление текущим временем
import datetime

# ======== ========= ========= ========= ========= ========= ========= =========

_G_TIMEZONE = 0

# ======== ========= ========= ========= ========= ========= ========= =========

def set_timezone(tz):
    global _G_TIMEZONE
    _G_TIMEZONE = tz

# ======== ========= ========= ========= ========= ========= ========= =========

def time():
    return datetime.datetime.now() + datetime.timedelta(hours=_G_TIMEZONE)

def timezone():
    return _G_TIMEZONE

# ======== ========= ========= ========= ========= ========= ========= =========
