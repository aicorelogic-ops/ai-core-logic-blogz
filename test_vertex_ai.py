"""Test Vertex AI Imagen 3 connection and image generation"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variables from .env
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / 'news_bot' / '.env')

# Now test Vertex AI
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel

# Get config
PROJECT_ID = os.getenv("VERTEX_PROJECT_ID")
LOCATION = os.getenv("VERTEX_LOCATION", "us-central1")
KEY_PATH = os.getenv("VERTEX_KEY_PATH")

print(f"Testing Vertex AI Imagen 3...")
print(f"Project ID: {PROJECT_ID}")
print(f"Location: {LOCATION}")
print(f"Key Path: {KEY_PATH}")

# Set credentials
if KEY_PATH and os.path.exists(KEY_PATH):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH
    print(f"✅ Using service account: {KEY_PATH}")

# Initialize Vertex AI
aiplatform.init(project=PROJECT_ID, location=LOCATION)
print(f"✅ Vertex AI initialized")

# Try to load the model
try:
    print(f"\n🎨 Loading Imagen model...")
    model = ImageGenerationModel.from_pretrained("imagegeneration@002")
    print(f"✅ Model loaded successfully!")
    
    # Try to generate an image
    print(f"\n🎨 Generating test image...")
    response = model.generate_images(
        prompt="A futuristic AI brain glowing with data streams, cinematic lighting",
        number_of_images=1,
        aspect_ratio="16:9"
    )
    
    if response.images:
        print(f"✅ Image generated successfully!")
        output_path = Path(__file__).parent / 'temp_images' / 'test_imagen.jpg'
        output_path.parent.mkdir(exist_ok=True)
        response.images[0].save(location=str(output_path))
        print(f"✅ Image saved to: {output_path}")
    else:
        print(f"❌ No images in response")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
