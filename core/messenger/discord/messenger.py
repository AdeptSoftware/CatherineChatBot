#
from core.messenger.messenger           import AbstractMessenger, TYPE_DISCORD

from core.messenger.discord.message     import DiscordMessage
from core.messenger.discord.answer      import DiscordAnswer

from discord.ext				        import commands
import asyncio

# ======== ========= ========= ========= ========= ========= ========= =========

def run_coroutine(coro):
    loop = asyncio.get_event_loop()
    return asyncio.run_coroutine_threadsafe(coro, loop)

# ======== ========= ========= ========= ========= ========= ========= =========

class DiscordMessenger(AbstractMessenger):
    def __init__(self, configs):
        super().__init__(configs)
        self._bot = commands.Bot(command_prefix=configs["prefix"])
        self._ctx = None

        @self._bot.event
        async def on_message(ctx):
            # Пишут нам не боты и из разрешенных серверов
            if self._check_guild_id(ctx.guild.id) and not ctx.author.bot:
                self._ctx = ctx
                self._context.set(DiscordMessage(ctx, self._bot.user.id),
                                  DiscordAnswer(ctx.guild.id))
                if self._mngr.on_message(self._context):
                    await self.send(self._context.ans.get(), is_async=True)

    def _check_guild_id(self, gid):
        return str(gid) in self._configs["targets"]

    @property
    def type_id(self):
        return TYPE_DISCORD

    def create_answer(self, chat_id):
        return DiscordAnswer(chat_id)

    def run(self):
        self._bot.run(self._configs["token"])

    def send(self, obj, is_async=False):
        if not is_async:
            run_coroutine(self.send(obj["text"], True))
            return None

        if self._ctx.guild.id != obj["chat_id"]:
            return None     # Пока не поддерживается

        embed = None
        if obj["embeds"]:
            embed = obj["embeds"].pop(0)
            for e in obj["embeds"]:
                run_coroutine(self._ctx.channel.send("", embed=e))
        if obj["reply"]:
            return self._ctx.reply(obj["text"], embed=embed)
        return self._ctx.channel.send(obj["text"], embed=embed)

# ========= ========= ========= ========= ========= ========= ========= =========
