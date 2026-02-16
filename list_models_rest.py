import requests
import os
import json
from news_bot.settings import GOOGLE_API_KEY

def list_models_rest():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GOOGLE_API_KEY}"
    
    print(f"Listing models via REST API...")
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            models = result.get('models', [])
            print(f"Found {len(models)} models:")
            for m in models:
                print(f"- {m['name']} ({m.get('displayName', '')})")
                if 'image' in m['name'] or 'imagen' in m['name']:
                    print(f"  *** FOUND IMAGE MODEL: {m['name']} ***")
        else:
            print(f"❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_models_rest()
