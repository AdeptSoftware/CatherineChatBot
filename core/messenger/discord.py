# 24.05.2022-27.05.2022
import core.commands.manager	as _mgr
from core.messenger.cls			import *
from core.thread				import run_thread
from discord.ext				import tasks, commands
import discord
import asyncio

# ======== ========= ========= ========= ========= ========= ========= =========

def run_coroutine(coro):
	loop = asyncio.get_event_loop()
	return asyncio.run_coroutine_threadsafe(coro, loop)

# ======== ========= ========= ========= ========= ========= ========= =========

class DiscordUserProfile(IUserProfile):
	def __init__(self, ctx):
		self._ctx	= ctx
		self._data	= None

	@property
	def id(self):
		return self._ctx.author.id

	def ref(self, ref_type):
		result = ""
		if ref_type != REF_NONE:
			if ref_type == REF_NAME or ref_type == REF_FULLNAME:
				result = self._ctx.author.display_name
			elif ref_type == REF_NICK:
				result = self._ctx.author.nick or "?"
			if result and ref_type == REF_LINK:
				return '@' + self._ctx.author.display_name
		return result

	@property
	def gender(self):
		return GENDER_NOT_SPECIFIED

# ======== ========= ========= ========= ========= ========= ========= =========

# Хранит данные о текущем сообщении
class DiscordMessage(IMessage):
	def __init__(self, bot, ctx):
		self._bot = bot
		self._ctx = ctx

	@property
	def text(self):
		return self._ctx.content

	@property
	def chat_id(self):
		return self._ctx.channel.id

	@property
	def id(self):
		return self._ctx.id

	def is_me(self, user_id):
		return self._bot.user.id == user_id

	def type(self):
		return TYPE_DISCORD

# ======== ========= ========= ========= ========= ========= ========= =========

class DiscordAnswer(Answer):
	def __init__(self, bot, ctx):
		super().__init__(DiscordUserProfile(ctx), DiscordMessage(bot, ctx))
		self._ctx = ctx

	def send(self, text="", is_async=False):
		if not is_async:
			run_coroutine(self.send(text, True))
			return None

		if ATT_TEXT in self._att:
			text = self._att[ATT_TEXT] + text
		# Подготовка изображений
		embeds = []
		if ATT_IMAGES in self._att:
			for img in self._att[ATT_IMAGES]:
				embed = discord.Embed(color = 0xFF9900, title = img[IMAGE_DESC])
				embed.set_image(url = img[IMAGE_URL])
				embeds += [embed]
		self._att.clear()
		# Отправка сообщений
		embed = None
		if embeds:
			embed = embeds.pop(0)
			for e in embeds:
				run_coroutine(self._ctx.channel.send("", embed = e))
		if self._reply:
			return self._ctx.reply(text, embed = embed)
		return self._ctx.channel.send(text, embed = embed)

# ======== ========= ========= ========= ========= ========= ========= =========

class _FakeContext:
	def __init__(self, channel):
		self.context = ""
		self.channel = channel

class DiscordMessenger(IMessenger):
	def __init__(self, cfg):
		self._mgr		= _mgr.CommandManager(cfg["servers"])
		self._bot		= commands.Bot(command_prefix=cfg["prefix"])
		self._cfg		= cfg

		@self._bot.event
		async def on_message(ctx):
			# Пишут нам не боты и из разрешенных серверов
			if str(ctx.guild.id) in self._cfg["servers"] and not ctx.author.bot:
				ans = DiscordAnswer(self._bot, ctx)
				if self._mgr.on_message(ans):
					await ans.send(is_async=True)

	def msg(self, channel_id):
		ctx = _FakeContext(self._bot.get_channel(channel_id))
		return DiscordAnswer(self._bot, ctx)

	def run(self):
		self._on = True
		try:
			self._bot.run(self._cfg["token"])
			# Не работает на heroku. Выдаёт ошибку:
			# "ValueError: set_wakeup_fd only works in main thread"
		except Exception as err:
			self._on = False
			raise err

	def is_running(self):
		return self._on

# ======== ========= ========= ========= ========= ========= ========= =========
