class ChatbotModel:
    def generate_response(self, user_message, sentiment):

        if sentiment == "positive":
            return "I'm glad to hear that! 😊 How else can I assist you today?"

        elif sentiment == "negative":
            return "I'm really sorry you feel this way. 😟 Let me try my best to help you. Tell me more."

        else:  # neutral
            return "I understand. How can I help you further?"
