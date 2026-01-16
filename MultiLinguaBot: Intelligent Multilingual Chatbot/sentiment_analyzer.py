from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def get_sentiment(self, text):
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']

        if compound >= 0.35:
            return "positive"
        elif compound <= -0.35:
            return "negative"
        else:
            return "neutral"
