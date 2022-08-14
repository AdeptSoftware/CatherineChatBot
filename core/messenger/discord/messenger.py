#
from core.messenger.messenger           import AbstractMessenger, TYPE_DISCORD
from core.messenger.discord.message     import DiscordMessage
from core.messenger.discord.answer      import DiscordAnswer

from discord.ext				        import commands

# ======== ========= ========= ========= ========= ========= ========= =========

class DiscordMessenger(AbstractMessenger):
    def __init__(self, data, configs):
        super().__init__(data, configs)
        self._bot   = commands.Bot(command_prefix=configs["prefix"],
                                   loop=data.updater.loop)
        self._token = configs["token"]

        @self._bot.event
        async def on_message(ctx):
            # Пишут нам не боты и не из запрещенных серверов
            if self._ctx.mngr.is_allowed_chat(ctx.guild.id) and not ctx.author.bot:
                self._ctx.set_message(DiscordMessage(ctx, self._bot.user.id))
                self._ctx.set_answer(DiscordAnswer(ctx.guild.id))
                if self._ctx.mngr.on_message(self._ctx):
                    await self.send(self._ctx.ans.get(), ctx)

    @property
    def type_id(self):
        return TYPE_DISCORD

    def create_answer(self, chat_id):
        return DiscordAnswer(chat_id)

    async def run(self):
        await self._bot.start(self._token)
        return True

    def send(self, obj, ctx=None):
        if ctx and ctx.guild.id == obj["chat_id"]:
            if obj["reply"]:  # Пересылать можно только в текущий чат
                return ctx.reply(obj["text"], embed=obj["embed"], files=obj["files"])
            channel = ctx.channel
        else:
            channel = self._bot.get_channel(obj["chat_id"])
        return channel.send(obj["text"], embed=obj["embed"], files=obj["files"])

# ========= ========= ========= ========= ========= ========= ========= =========
