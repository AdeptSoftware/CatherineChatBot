# 28.05.2022 Загружает локальные файлы на Яндекс.Диск
import yadisk
import json
import os

# ========= ========= ========= ========= ========= ========= ========= =========

api  = None
data = None

# ========= ========= ========= ========= ========= ========= ========= =========

def upload_dir(srcpath, dstpath):
	if not api.exists(dstpath):
		api.mkdir(dstpath)
	for name in os.listdir(srcpath):
		if os.path.isdir(srcpath+name):
			upload_dir(srcpath+name+'/', dstpath+name+'/')
		else:
			api.upload(srcpath+name, dstpath+name, overwrite=True)
			print("READY: " + dstpath+name)


# ========= ========= ========= ========= ========= ========= ========= =========

# Загрузка данных
data = None
with open("data.json", 'r') as f:
	data = json.loads(f.read())
# Инициализация
api = yadisk.YaDisk(token=data["token"])
if not api.check_token():
	raise BaseException("Token isn't correct!")
# Загружаем все содержимое папки на Яндекс.Диск
upload_dir(data["src"], data["dst"])


