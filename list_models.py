
import google.generativeai as genai
from news_bot.settings import GOOGLE_API_KEY
import os

genai.configure(api_key=GOOGLE_API_KEY)

print("Listing available models...")
try:
    with open("all_models.txt", "w") as f:
        for m in genai.list_models():
            f.write(f"{m.name}\n")
    print("All models written to all_models.txt")
except Exception as e:
    print(f"Error listing models: {e}")
