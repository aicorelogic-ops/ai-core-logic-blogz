"""
Test Gemini Imagen 4.0 Fast Generation
"""
import google.generativeai as genai
from news_bot.settings import GOOGLE_API_KEY
import os

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

print("Testing Gemini Imagen 4.0...")

try:
    # Try using the imagen model directly
    model = genai.GenerativeModel('imagen-4.0-fast-generate-001')
    print(f"✅ Model loaded: {model.model_name}")
    
    # Try to generate an image
    prompt = "A professional news graphic about AI technology, modern design, high contrast"
    print(f"Generating image with prompt: {prompt}")
    
    response = model.generate_content(prompt)
    print(f"Response type: {type(response)}")
    print(f"Response: {response}")
    
    # Try to save if successful
    if hasattr(response, 'images') and response.images:
        with open('test_gemini_imagen.jpg', 'wb') as f:
            f.write(response.images[0].data)
        print("✅ Image saved to test_gemini_imagen.jpg")
    else:
        print(f"❌ No images in response")
        print(f"Response attributes: {dir(response)}")
        
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
