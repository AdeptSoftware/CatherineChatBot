#
from core.messenger.answer import IAnswer

# ========= ========= ========= ========= ========= ========= ========= =========

class DiscordAnswer(IAnswer):
    def __init__(self, chat_id):
        self._text      = ""
        self._embeds    = []
        self._reply     = False
        self._chat_id   = chat_id

    def get(self):
        if not self._text and \
           not self._embeds:
            return None

        return {
            "embeds":   self._embeds,
            "text":     self._text,
            "reply":    self._reply,
            "chat_id":  self._chat_id
        }

    def set_text(self, text):
        self._text += text
        return None

    # Не поддерживается
    def set_sticker(self, sticker_id):
        return None

    def set_image(self, image):
        return None

    # Не поддерживается
    def set_document(self, doc):
        return None

    # Не поддерживается
    def set_audio(self, audio):
        return None

    # Не поддерживается
    def set_video(self, video):
        return None

    def reply(self):
        self._reply = True
        return None

# ========= ========= ========= ========= ========= ========= ========= =========
