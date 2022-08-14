# Используемые команды приложением
import core.commands.command as _cmd

# ======== ========= ========= ========= ========= ========= ========= =========

def hello(ctx: _cmd.Context):
    return ctx.msg.contain(ctx.lang["$HELLO"])

def goodbye(ctx: _cmd.Context):
    return ctx.msg.contain_phrase(ctx.lang["#GOODBYE"])

# ======== ========= ========= ========= ========= ========= ========= =========
# Answer_key - ключи в json-файле, хранящем строки локализации
# Если перед именем стоит символ:
#   $ - Содержит список строк (слов), не требующих разбивание на слова
#   # - . . . . . . . . . . . . . . . . .требует разбить на слова
#   = - Категория ответов. Содержит список строк-ответов
# P.S.: Если идёт сразу текст, то это значит, что он не относится к командам

def attach():
    #        condition  answer_key  cd  lim      access_type        name
    _cmd.new(hello,     "=HELLO",   300, 1, _cmd.ACCESS_PERSONAL, "Hello")
    _cmd.new(goodbye,   "=GOODBYE", 300, 1, _cmd.ACCESS_PERSONAL, "Goodbye")

# ======== ========= ========= ========= ========= ========= ========= =========
