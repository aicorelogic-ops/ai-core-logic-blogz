import requests
import os
import json
from news_bot.settings import GOOGLE_API_KEY

def test_imagen_rest():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={GOOGLE_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "instances": [
            {
                "prompt": "A futuristic city with flying cars, cinematic lighting, 8k resolution"
            }
        ],
        "parameters": {
            "sampleCount": 1
        }
    }
    
    print(f"Testing Imagen 3 REST API...")
    try:
        response = requests.post(url, headers=headers, json=data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            # print(json.dumps(result, indent=2))
            
            # Check for image data
            predictions = result.get('predictions', [])
            if predictions:
                print(f"✅ Success! Received {len(predictions)} images.")
                # Save first image to decode and verify
                import base64
                b64_data = predictions[0]['bytesBase64Encoded']
                with open("test_rest_image.png", "wb") as f:
                    f.write(base64.b64decode(b64_data))
                print("Saved to test_rest_image.png")
            else:
                print("❌ No predictions found in response")
                print(response.text)
        else:
            print(f"❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_imagen_rest()
