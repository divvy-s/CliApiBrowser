import os
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv()

class GeminiBrowser:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("API key not set")
            exit(1)
        self.model = "gemini-1.5-flash"  
    def set_model(self, model_name):
        supported_models = ['gemini-1.5-flash', 'gemini-1.5-pro']
        if model_name in supported_models:
            self.model = model_name
            print(f"Switched to model: {model_name}")
        else:
            print("Unsupported model. Available models:", ', '.join(supported_models))
    def gemini_query(self, prompt):
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 200:
            output = response.json()
            try:
                return output["candidates"][0]["content"]["parts"][0]["text"].strip()
            except (KeyError, IndexError):
                return "No response from Gemini."
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

def type_out(text, delay=0.02):
    """Simulate typing animation in terminal."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print() 

def main():
    bot = GeminiBrowser()
    print("Welcome to the CLI browser")
    print("Type exit to exit the browser")
    print("You can change model typing /model followed by the model name")
    print("You can save the last reply using: /save filename.txt")

    last_reply = None 

    while True:
        user_input = input(">>> ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        elif user_input.startswith('/model'):
            parts = user_input.split(maxsplit=1)
            if len(parts) == 2:
                model_name = parts[1].strip()
                bot.set_model(model_name)
            else:
                print("Usage: /model MODEL_NAME")
        elif user_input.startswith('/save'):
            parts = user_input.split(maxsplit=1)
            if len(parts) == 2:
                filename = parts[1].strip()
                if last_reply:
                    try:
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(last_reply)
                        print(f"Reply saved to {filename}")
                    except Exception as e:
                        print(f"Error saving file: {e}")
                else:
                    print("No reply to save yet.")
            else:
                print("Usage: /save filename.txt")
        else:
            reply = bot.gemini_query(user_input)
            if reply:
                type_out(reply, delay=0.02)
                print("--------\n")
                last_reply = reply 
if __name__ == "__main__":
    main()