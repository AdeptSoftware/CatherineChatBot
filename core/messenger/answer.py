# Производные классы предназначены для формирования ответа на сообщения

class IAnswer:
    def get(self):
        pass

    def set_text(self, text):
        pass

    def set_sticker(self, sticker_id):
        pass

    def set_image(self, image):
        pass

    def set_document(self, doc):
        pass

    def set_audio(self, audio):
        pass

    def set_video(self, video):
        pass

    def reply(self):
        pass

# ========= ========= ========= ========= ========= ========= ========= =========
