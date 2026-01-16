class ChatbotModel:

    responses = {
        "en": {
            "positive": "I'm glad to hear that! 😊 How can I assist you more?",
            "negative": "I'm sorry you're feeling this way. I'm here to help. 🙏",
            "neutral": "Alright, tell me how I can support you."
        },
        "hi": {
            "positive": "यह सुनकर बहुत अच्छा लगा! 😊 मैं आपकी और कैसे मदद कर सकता हूँ?",
            "negative": "मुझे अफसोस है कि आप ऐसा महसूस कर रहे हैं। मैं आपकी सहायता करने के लिए यहाँ हूँ। 🙏",
            "neutral": "ठीक है, बताइए मैं आपकी कैसे मदद कर सकता हूँ?"
        },
        "es": {
            "positive": "¡Me alegra escuchar eso! 😊 ¿Cómo puedo ayudarte más?",
            "negative": "Lamento que te sientas así. Estoy aquí para ayudarte. 🙏",
            "neutral": "Bien, dime cómo puedo ayudarte."
        },
        "fr": {
            "positive": "Je suis heureux de l'entendre ! 😊 Comment puis-je vous aider davantage ?",
            "negative": "Je suis désolé que vous vous sentiez ainsi. Je suis là pour vous aider. 🙏",
            "neutral": "D'accord, dites-moi comment puis-je vous aider."
        }
    }

    def get_response(self, sentiment, lang="en"):
        lang_responses = self.responses.get(lang, self.responses["en"])
        return lang_responses[sentiment]
