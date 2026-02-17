"""Test Gemini image generation"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variables from .env
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / 'news_bot' / '.env')

# Test Gemini image generation
import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY")

print(f"Testing Gemini Image Generation...")
print(f"API Key: {API_KEY[:20]}...")

# Configure Gemini
genai.configure(api_key=API_KEY)

try:
    print(f"\n🎨 Loading Gemini Imagen 4.0 Fast model...")
    model = genai.GenerativeModel('imagen-4.0-fast-generate-001')
    print(f"✅ Model loaded successfully!")
    
    # Try to generate an image
    print(f"\n🎨 Generating test image...")
    prompt = "A futuristic AI brain glowing with data streams, cinematic lighting, high contrast"
    
    response = model.generate_content(prompt)
    
    if response.parts:
        print(f"✅ Image generated successfully!")
        
        # Save the image
        image_data = response.parts[0].inline_data.data
        output_path = Path(__file__).parent / 'temp_images' / 'test_gemini.jpg'
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(image_data)
        
        print(f"✅ Image saved to: {output_path}")
    else:
        print(f"❌ No image data in response")
        print(f"Response: {response}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
