import os
from typing import List, Dict, Any

from google import genai
from google.genai import types
from PIL import Image


class MultiModalChatBot:
    """
    Simple multi-modal chatbot using Google's Gemini API via google-genai SDK.

    Capabilities:
      - Text chat
      - Image understanding (captioning / Q&A about an image)
      - Image generation
    """

    def __init__(
        self,
        text_model: str = "gemini-2.5-flash",        # text + vision capable model
        image_model: str = "gemini-2.5-flash-image" # image-generation model
    ):
        # Client auto-uses GEMINI_API_KEY from env if present
        self.client = genai.Client()
        self.text_model = text_model
        self.image_model = image_model

        # Store conversation as a list of "role: text" strings
        self.history: List[str] = []

    # ---------- Internal helpers ----------

    def _build_prompt_from_history(self, new_user_msg: str) -> List[Any]:
        """
        Convert history into a single list of text pieces + append new user msg.

        Gemini accepts a list of strings, Images, etc., as `contents`. :contentReference[oaicite:5]{index=5}
        We'll keep it simple: just text history + the new user message.
        """
        # Very simple formatting: prepend "User:"/"Bot:" so model sees roles.
        all_turns = []
        for i, line in enumerate(self.history):
            all_turns.append(line)

        all_turns.append(f"User: {new_user_msg}")
        all_turns.append("Assistant:")

        return all_turns

    def _append_to_history(self, user_msg: str, bot_msg: str):
        self.history.append(f"User: {user_msg}")
        self.history.append(f"Assistant: {bot_msg}")

    # ---------- Public methods ----------

    def chat_text(self, user_msg: str) -> str:
        """
        Pure text chat with context memory.
        """
        contents = self._build_prompt_from_history(user_msg)

        response = self.client.models.generate_content(
            model=self.text_model,
            contents=contents,
        )

        # Combine all text parts from the response
        bot_text_parts = [p.text for p in response.parts if p.text is not None]
        bot_reply = "\n".join(bot_text_parts).strip()

        # Update history
        self._append_to_history(user_msg, bot_reply)

        return bot_reply

    def chat_with_image(self, image_path: str, user_msg: str) -> str:
        """
        Send an image + text question to Gemini for visual Q&A.
        Example: "What is in this image?"
        """
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        image = Image.open(image_path)

        # History in text + new prompt + image as one multimodal request
        history_prompt = self._build_prompt_from_history(
            f"{user_msg} (I have attached an image.)"
        )
        contents = history_prompt + [image]

        response = self.client.models.generate_content(
            model=self.text_model,   # text+image capable model
            contents=contents,
        )

        bot_text_parts = [p.text for p in response.parts if p.text is not None]
        bot_reply = "\n".join(bot_text_parts).strip()

        # Store a simplified version of what happened in history
        self._append_to_history(f"{user_msg} [image={image_path}]", bot_reply)

        return bot_reply

    def generate_image(self, prompt: str, output_path: str = "generated_image.png") -> str:
        """
        Generate an image from a text prompt using an image model.
        Saves the image and returns the file path.
        """
        response = self.client.models.generate_content(
            model=self.image_model,
            contents=[prompt],
        )

        # The image model returns inline image data inside parts. :contentReference[oaicite:6]{index=6}
        image_saved = False
        for part in response.parts:
            if getattr(part, "inline_data", None) is not None:
                image_obj = part.as_image()  # convert to PIL.Image
                image_obj.save(output_path)
                image_saved = True
                break

        if not image_saved:
            raise RuntimeError("No image data returned from Gemini.")

        return output_path


# ---------- Simple CLI driver ----------

def main():
    # Optional: check key explicitly
    if not os.getenv("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY is not set. The google-genai client will fail.")
        print("Set GEMINI_API_KEY environment variable and try again.")
        return

    bot = MultiModalChatBot()

    print("\n=== Multi-Modal Gemini Chatbot ===")
    print("1) Text chat")
    print("2) Ask a question about an image")
    print("3) Generate an image from text")
    print("4) Exit\n")

    while True:
        choice = input("Choose an option (1/2/3/4): ").strip()

        if choice == "1":
            user_msg = input("\nYou: ")
            if not user_msg:
                continue
            reply = bot.chat_text(user_msg)
            print("\nBot:", reply, "\n")

        elif choice == "2":
            img_path = input("Path to image file: ").strip()
            question = input("Your question about this image: ").strip()
            try:
                reply = bot.chat_with_image(img_path, question)
                print("\nBot:", reply, "\n")
            except Exception as e:
                print(f"Error: {e}\n")

        elif choice == "3":
            prompt = input("Describe the image you want Gemini to create: ").strip()
            out = input("Output filename (default: generated_image.png): ").strip()
            if not out:
                out = "generated_image.png"
            try:
                path = bot.generate_image(prompt, out)
                print(f"\nImage saved to: {path}\n")
            except Exception as e:
                print(f"Error: {e}\n")

        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3 or 4.\n")


if __name__ == "__main__":
    main()
