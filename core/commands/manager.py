# 24.05.2022
from core.messenger.cls		import *
from core.thread			import G_ON_ERROR

# ======== ========= ========= ========= ========= ========= ========= =========

class CommandManager:
	def __init__(self, cmd_list):
		pass

	def on_message(self, answer : Answer):
		try:
			answer.user.stats = None
			# Приступим к анализу сообщения
			# answer.attach(txt=answer.msg.text)
			return answer.is_ready()
		except Exception as err:
			G_ON_ERROR(err)
			return False

# ======== ========= ========= ========= ========= ========= ========= =========
