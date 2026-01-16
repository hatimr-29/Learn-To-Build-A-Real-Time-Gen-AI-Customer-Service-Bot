from language_detector import LanguageDetector
from sentiment_analyzer import SentimentAnalyzer
from translator import TextTranslator
from model import ChatbotModel

class MultilingualChatbot:

    def __init__(self):
        self.lang_detector = LanguageDetector()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.translator = TextTranslator()
        self.chat_model = ChatbotModel()

    def respond(self, user_text):

        # 1. Detect language
        lang = self.lang_detector.detect_language(user_text)

        # 2. Translate to English for sentiment model
        text_in_english = self.translator.translate(user_text, "en")

        # 3. Sentiment detection
        sentiment = self.sentiment_analyzer.get_sentiment(text_in_english)

        # 4. Generate culturally appropriate response in original language
        reply = self.chat_model.get_response(sentiment, lang)

        return lang, sentiment, reply
