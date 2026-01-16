from chatbot import MultilingualChatbot

def main():
    bot = MultilingualChatbot()
    print("\n🤖 Multilingual Chatbot Started! (Supports English, Hindi, Spanish, French)")
    print("Type 'exit' to stop.\n")

    while True:
        msg = input("You: ")

        if msg.lower() == "exit":
            print("Bot: Goodbye! 👋")
            break

        lang, sentiment, reply = bot.respond(msg)

        print(f"(Language Detected: {lang}, Sentiment: {sentiment})")
        print("Bot:", reply, "\n")

if __name__ == "__main__":
    main()
