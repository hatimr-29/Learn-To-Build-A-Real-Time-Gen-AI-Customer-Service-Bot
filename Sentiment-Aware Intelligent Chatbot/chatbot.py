from sentiment_analyzer import SentimentAnalyzer
from model import ChatbotModel

class SentimentChatbot:
    def __init__(self):
        self.sentiment_model = SentimentAnalyzer()
        self.chat_model = ChatbotModel()

    def respond(self, user_input):
        sentiment = self.sentiment_model.get_sentiment(user_input)
        response = self.chat_model.generate_response(user_input, sentiment)
        return sentiment, response
