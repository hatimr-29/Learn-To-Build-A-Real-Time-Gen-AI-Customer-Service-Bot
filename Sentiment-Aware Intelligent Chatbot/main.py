from chatbot import SentimentChatbot

def main():
    bot = SentimentChatbot()
    print("\n🤖 Sentiment Chatbot Started! Type 'exit' to quit.\n")

    while True:
        user_msg = input("You: ")

        if user_msg.lower() == "exit":
            print("Bot: Goodbye! 👋")
            break

        sentiment, reply = bot.respond(user_msg)

        print(f"(Detected Sentiment: {sentiment})")
        print(f"Bot: {reply}\n")

if __name__ == "__main__":
    main()
