"""Test Vertex AI Imagen with different models"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variables from .env
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / 'news_bot' / '.env')

# Get config
PROJECT_ID = os.getenv("VERTEX_PROJECT_ID")
LOCATION = os.getenv("VERTEX_LOCATION", "us-central1")
KEY_PATH = Path(__file__).parent / 'news_bot' / os.getenv("VERTEX_KEY_PATH")

print(f"=== Vertex AI Imagen Test ===")
print(f"Project ID: {PROJECT_ID}")
print(f"Location: {LOCATION}")
print(f"Key Path: {KEY_PATH}")
print(f"Key exists: {KEY_PATH.exists()}")

# Set credentials
if KEY_PATH.exists():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(KEY_PATH)
    print(f"✅ Using service account: {KEY_PATH}")
else:
    print(f"❌ Service account key not found at {KEY_PATH}")
    sys.exit(1)

# Test different methods
print(f"\n=== Testing Method 1: vertexai.preview.vision_models ===")
try:
    from google.cloud import aiplatform
    from vertexai.preview.vision_models import ImageGenerationModel
    import vertexai
    
    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    print(f"✅ Vertex AI initialized")
    
    # Try different models
    models_to_try = [
        "imagegeneration@006",
        "imagegeneration@002", 
        "imagen-3.0-generate-001",
        "imagen-3.0-fast-generate-001"
    ]
    
    for model_name in models_to_try:
        try:
            print(f"\n🎨 Testing model: {model_name}")
            model = ImageGenerationModel.from_pretrained(model_name)
            print(f"   ✅ Model loaded!")
            
            # Try to generate
            response = model.generate_images(
                prompt="A professional news graphic about AI, modern design",
                number_of_images=1,
            )
            
            if response.images:
                print(f"   ✅ Image generated successfully!")
                output_path = Path(__file__).parent / 'temp_images' / f'vertex_{model_name.replace("/", "_")}.jpg'
                output_path.parent.mkdir(exist_ok=True)
                response.images[0].save(location=str(output_path))
                print(f"   ✅ Saved to: {output_path}")
                print(f"\n✅✅✅ SUCCESS WITH {model_name}! ✅✅✅")
                break
            else:
                print(f"   ❌ No images in response")
                
        except Exception as e:
            print(f"   ❌ Error: {type(e).__name__}: {str(e)[:100]}")
            
except Exception as e:
    print(f"❌ Method 1 failed: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print(f"\n=== Testing Method 2: Gemini Image Generation API ===")
try:
    import google.generativeai as genai
    
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Try imagen-3.0 models
    imagen_models = [
        "imagen-3.0-generate-001",
        "imagen-3.0-fast-generate-001",
        "imagen-4.0-fast-generate-001"
    ]
    
    for model_name in imagen_models:
        try:
            print(f"\n🎨 Testing Gemini model: {model_name}")
            model = genai.GenerativeModel(model_name)
            
            response = model.generate_content("A professional news graphic about AI")
            print(f"   Response: {response}")
            
            if hasattr(response, 'images') and response.images:
                print(f"   ✅ Image generated!")
                print(f"\n✅✅✅ SUCCESS WITH GEMINI {model_name}! ✅✅✅")
                break
            else:
                print(f"   ❌ No images attribute or empty")
                
        except Exception as e:
            print(f"   ❌ Error: {type(e).__name__}: {str(e)[:100]}")
            
except Exception as e:
    print(f"❌ Method 2 failed: {type(e).__name__}: {e}")

print(f"\n=== Test Complete ===")
