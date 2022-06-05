# 25.05.2022
from core.storage.cls import *
import os

# ======== ========= ========= ========= ========= ========= ========= =========

def _write(path, string):
	with open(path, 'w', encoding=FILE_ENCODING) as f:
		f.write(string)
		return True

# ======== ========= ========= ========= ========= ========= ========= =========

class LocalStorageObject(AbstractStorageObject):
	def _read(self, path):
		with open(self._path, 'r', encoding=FILE_ENCODING) as f:
			return f.read()

	def _write(self, path, string):
		return _write(path, string)

# ======== ========= ========= ========= ========= ========= ========= =========

# path - относительный путь (по отношению к root)
class LocalStorageManager(IStorageManager):
	def __init__(self, root):
		self.cso = self.create_storage_object
		self._root = root

	def create(self):
		return True

	def create_file(self, path, string=""):
		return _write(self._root+path, string)

	def mkdir(self, path):
		os.mkdir(self._root+path)

	def exists(self, path):
		return os.path.exists(self._root+path)

	# На основе существующего файла
	def create_storage_object(self, path, is_json=True):
		if is_json:
			return LocalStorageObject(self._root+path, {})
		else:
			return LocalStorageObject(self._root+path, "")

# ======== ========= ========= ========= ========= ========= ========= =========
