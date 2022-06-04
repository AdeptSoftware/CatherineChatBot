# 25.05.2022
from core.storage.cls import *
import yadisk
import io

# ======== ========= ========= ========= ========= ========= ========= =========

def _write(api, path, string):
	bytes_io = io.BytesIO(string.encode())
	api.upload(bytes_io, path, overwrite=True)
	bytes_io.close()
	return True

# ======== ========= ========= ========= ========= ========= ========= =========

# Все файлы, привязанные к таким объектам должны существовать на момент создания
class YandexStorageObject(AbstractStorageObject):
	def __init__(self, api, path, default):
		self._api = api
		super().__init__(path, default)

	def _read(self, path):
		bytes_io = io.BytesIO(b"")
		self._api.download(path, bytes_io)
		string = bytes_io.getvalue().decode(FILE_ENCODING, 'backslashreplace')
		bytes_io.close()
		return string

	def _write(self, path, string):
		return _write(self._api, path, string)

# ======== ========= ========= ========= ========= ========= ========= =========

# path - относительный путь (по отношению к root)
class YandexStorageManager():
	def __init__(self, token, root):
		self.cso = self.create_storage_object
		self._token = token
		self._root = root
		self._api = None

	def create(self):
		if self._api is None:
			self._api = yadisk.YaDisk(token=self._token)
		return self._api.check_token()

	def create_file(self, path, string=""):
		return _write(self._api, self._root+path, string)

	def mkdir(self, path):
		self._api.mkdir(self._root+path)

	def exists(self, path):
		return self._api.exists(self._root+path)

	# На основе существующего файла
	def create_storage_object(self, path, is_json=True):
		if is_json:
			return YandexStorageObject(self._api, self._root+path, {})
		else:
			return YandexStorageObject(self._api, self._root+path, "")
			
# ======== ========= ========= ========= ========= ========= ========= =========
