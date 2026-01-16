from langdetect import detect

class LanguageDetector:
    def detect_language(self, text):
        try:
            return detect(text)
        except:
            return "en"  # default English
