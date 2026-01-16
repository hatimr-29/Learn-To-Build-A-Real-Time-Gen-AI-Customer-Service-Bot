from googletrans import Translator

class TextTranslator:
    def __init__(self):
        self.translator = Translator()

    def translate(self, text, dest_language):
        try:
            translated = self.translator.translate(text, dest=dest_language)
            return translated.text
        except:
            return text
