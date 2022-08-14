# Производные классы предназначены для приведения данных сообщения
# к общему виду для всей программы
import re

# ========= ========= ========= ========= ========= ========= ========= =========

# Регулярное выражение для разбивки сообщения на части
_parts = re.compile(r"[\w\d][-\w\d]+|[_\w\d]+|\[id\d+\|.+?]|@[_\w\d]+")

# ======== ========= ========= ========= ========= ========= ========= =========

_NAMES = ()

def set_catherine_names(names):
    _list = []
    for name in names:
        _list += [name.lower()]
    global _NAMES
    _NAMES = tuple(_list)

# ======== ========= ========= ========= ========= ========= ========= =========

class IMessage:
    def is_me(self):
        pass

    def msg_id(self):
        pass

    def from_id(self):
        pass

    def chat_id(self):
        pass

    @property                  # уж, не знаю насколько такое правильно в python
    def text(self):
        return ""

    @property
    def fwd(self):                                      # Пересланные сообщения
        return []

# ======== ========= ========= ========= ========= ========= ========= =========

class AbstractMessage(IMessage):
    def __init__(self):
        self._words         = None
        self._lower         = None
        self._prefix        = None
        self._appeal        = None
        self._sentences     = None

    # ==== ========= ========= ========= ========= ========= ========= =========

    @property
    def appeal(self):
        """ Вернет строку, как обращаются к нам """
        self._check()
        return self._appeal

    @property
    def words(self):
        """ Вернёт разбитое на слова сообщение """
        self._check()
        return self._words

    @property
    def prefix(self):
        """ Вернёт символы перед сообщением """
        self._check()
        return self._prefix

    # Подготавливает сообщение к дальнейшему использованию
    def __prepare(self):
        self._words  = []
        self._appeal = []
        self._prefix = ""
        # Разбивание текста на слова
        last = 0
        text = self.text
        for obj in _parts.finditer(text.lower().replace('ё', 'е')):
            span = obj.span()
            if span[0] - last > 0:
                self._words += self._punctuation(text, last, span[0])
            self._words += [text[span[0]:span[1]]]
            last = span[1]
        if last < len(text):
            self._words += self._punctuation(text, last, len(text))
        # Поиск префикса
        if self._words and not self._words[0].isalnum():
            if not self._words[0][0].isalnum():          # искл.: точь-в-точь
                self._prefix = self._words.pop(0)
        # Поиск обращения
        if self._words:
            if not self._is_appeal(0) and not self._is_appeal(-1):
                for msg in self.fwd:
                    if msg.is_me():
                        self._appeal += [_NAMES[0]]
                        break
        self._appeal = tuple(self._appeal)
        self._words  = tuple(self._words)

    @property
    def lower(self):
        """ Вернёт разбитое на слова сообщение в lowercase формате """
        return self.__lower()

    # создание lowercase версии self._words
    def __lower(self):
        if self._lower is None:
            self._check()
            self._lower = []
            for part in self._words:
                self._lower += [part.lower()]
            self._lower = tuple(self._lower)
        return self._lower

    @property
    def sentences(self):
        """ Определение конца каждого предложения """
        return self.__sentences()

    # Определение границ предложений
    def __sentences(self):
        if self._sentences is None:
            self._check()
            pos = 0
            self._sentences = []
            for part in self._words:
                if not part.isalnum():
                    for char in part:
                        if char in ".?!()":
                            self._sentences += [pos + 1]
                            break
                pos += 1
            self._sentences = tuple(self._sentences)
        return self._sentences

    # ==== ========= ========= ========= ========= ========= ========= =========

    # Проверяет промежутки между результатами _parts (RegEx)
    # На наличие знаков препинания и т.д.
    @staticmethod
    def _punctuation(text, span0, span1):
        data = text[span0:span1]
        data = ''.join(data.split(' '))
        if data:
            return [data]
        return []

    # Проверяет есть ли обращение к нам
    # Так же убирает лишние символы, мешающие распознаванию текста
    def _is_appeal(self, index):
        if self._words[index].lower() in _NAMES:
            self._appeal = [self._words.pop(index)]
            if not self._words[index].isalnum():
                self._appeal += [self._words.pop(index)]
            return True
        return False

    def _check(self):
        if self._words is None:
            self.__prepare()

    # ==== ========= ========= ========= ========= ========= ========= =========

    def get_sentences(self, as_string=False):
        if len(self.__sentences()) == 0:
            return []
        pos = 0
        _list = []
        for i in range(len(self._sentences)):
            _sublist = self._words[pos:self._sentences[i]]
            if _sublist:
                if not as_string:
                    _list += [_sublist]
                else:
                    string = ""
                    for j in range(len(_sublist)):
                        if string and _sublist[j].isalnum():
                            string += ' '
                        string += _sublist[j]
                    _list += [string]
            pos = self._sentences[i]
        return _list

    def contain(self, words):
        """ Проверка содержит ли сообщение определенные слова

        :param words: список слов в lowercase формате
        :return: True/False
        """
        self.__lower()
        for word in words:
            if word in self._lower:
                return True
        return False

    # phrases - должен содержать lowercase фразы
    def contain_phrase(self, phrases):
        """ Проверка содержит ли сообщение определенные фразы

        :param phrases: список фраз в lowercase формате.
            phrase состоит из списка слов
        :return: True/False
        """
        _list = self.__lower()
        _lenL = len(_list)
        for i in range(0, _lenL):
            for phrase in phrases:
                _lenP  = len(phrase)
                if i+_lenP <= _lenL:
                    offset = 0
                    for part in phrase:
                        if part != _list[i+offset]:
                            break
                        offset += 1
                    if offset == _lenP:
                        return True
        return False

# ========= ========= ========= ========= ========= ========= ========= =========
