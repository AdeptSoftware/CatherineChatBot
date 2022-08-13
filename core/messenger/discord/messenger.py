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
    def __init__(self, data, configs):
        super().__init__(data, configs)
        self._bot   = commands.Bot(command_prefix=configs["prefix"],
                                   loop=data.updater.loop)
        self._token = configs["token"]
        # Последний присланный объект
        self._obj   = None

        @self._bot.event
        async def on_message(ctx):
            # Пишут нам не боты и не из запрещенных серверов
            if self._ctx.mngr.is_allowed_chat(ctx.guild.id) and not ctx.author.bot:
                self._obj = ctx
                self._ctx.set_message(DiscordMessage(ctx, self._bot.user.id))
                self._ctx.set_answer(DiscordAnswer(ctx.guild.id))
                if self._ctx.mngr.on_message(self._ctx):
                    await self.send(self._ctx.ans.get(), is_async=True)

    @property
    def type_id(self):
        return TYPE_DISCORD

    def create_answer(self, chat_id):
        return DiscordAnswer(chat_id)

    async def run(self):
        await self._bot.start(self._token)
        return True

    def send(self, obj, is_async=False):
        if not is_async:
            run_coroutine(self.send(obj["text"], True))
            return None

        if self._obj.guild.id != obj["chat_id"]:
            return None     # Пока не поддерживается

        embed = None
        if obj["embeds"]:
            embed = obj["embeds"].pop(0)
            for e in obj["embeds"]:
                run_coroutine(self._obj.channel.send("", embed=e))
        if obj["reply"]:
            return self._obj.reply(obj["text"], embed=embed)
        return self._obj.channel.send(obj["text"], embed=embed)

# ========= ========= ========= ========= ========= ========= ========= =========
