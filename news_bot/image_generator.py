"""
Image Generator using Google Gemini Imagen 3 API.
Generates viral-style images for Facebook posts and saves them locally.
"""

import google.generativeai as genai
from .settings import GOOGLE_API_KEY
import os
from pathlib import Path
from datetime import datetime
import uuid

class ImageGenerator:
    def __init__(self):
        """Initialize Imagen 3 model and output directory."""
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('imagen-3.0-generate-001')
        
        # Create temp_images directory if it doesn't exist
        self.output_dir = Path(__file__).parent.parent / 'temp_images'
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"ImageGenerator initialized. Output directory: {self.output_dir}")
    
    
    def generate_viral_image(self, prompt, output_filename=None):
        """
        Generate a viral-style image using Pollinations AI (Reliable Fallback) and save locally.
        
        Args:
            prompt (str): Text prompt describing the image to generate
            output_filename (str, optional): Custom filename. Auto-generated if not provided.
        
        Returns:
            str: Absolute path to the saved image file
        """
        import requests
        import time
        import urllib.parse
        import re

        try:
            print(f"🎨 Generating image with Pollinations AI...")
            print(f"   Prompt: {prompt[:100]}...")
            
            # Clean prompt for URL
            clean_prompt = re.sub(r'[^a-zA-Z0-9, ]', '', prompt)
            encoded_prompt = urllib.parse.quote(clean_prompt.strip())
            
            # Use specific parameters for better reliability
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630&nologo=true&seed={uuid.uuid4().int % 100000}"
            
            print(f"   URL: {url}")
            
            # Download with retries
            max_retries = 3
            image_content = None
            
            for attempt in range(max_retries):
                try:
                    print(f"   Attempt {attempt + 1}/{max_retries}...")
                    response = requests.get(url, timeout=30)
                    
                    if response.status_code == 200 and len(response.content) > 1000:
                        image_content = response.content
                        print(f"✅ Downloaded ({len(image_content):,} bytes)")
                        # Ensure content header is image
                        if 'image' not in response.headers.get('content-type', '').lower():
                             print("⚠️ Warning: Content-Type is not image.")
                        break
                    else:
                        print(f"⚠️ Failed or too small. Status: {response.status_code}. Retrying...")
                        time.sleep(2)
                except Exception as e:
                    print(f"❌ Error: {e}")
                    time.sleep(2)
            
            if not image_content:
                print("❌ Failed to download valid image from Pollinations.")
                
                # FALLBACK: Use local text generator
                print("🔄 Attempting local text graphic fallback...")
                try:
                    from PIL import Image, ImageDraw, ImageFont
                    import textwrap
                    
                    width = 1200
                    height = 630
                    # Dark blue background for tech/business news
                    img = Image.new('RGB', (width, height), color=(10, 25, 47))
                    d = ImageDraw.Draw(img)
                    
                    # Try to load a font
                    try:
                        # Try system fonts or default
                        font_size = 60
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except IOError:
                        font = ImageFont.load_default()
                        
                    # Prepare text (use prompt's main subject or generic title)
                    # Extract "Editorial news graphic about X" -> "X"
                    text_content = prompt.replace("Editorial news graphic about ", "").split(",")[0]
                    if len(text_content) > 50:
                        text_content = text_content[:50] + "..."
                        
                    # Wrap text
                    lines = textwrap.wrap(text_content, width=25)
                    
                    # Calculate vertical center
                    line_height = 80
                    total_text_height = len(lines) * line_height
                    y_text = (height - total_text_height) / 2
                    
                    # Draw text
                    for line in lines:
                        # Get text width for centering
                        try:
                            bbox = d.textbbox((0, 0), line, font=font)
                            line_width = bbox[2] - bbox[0]
                        except AttributeError:
                             line_width = d.textlength(line, font=font)
                             
                        x_text = (width - line_width) / 2
                        d.text((x_text, y_text), line, font=font, fill=(255, 255, 255))
                        y_text += line_height
                        
                    # Save fallback image
                    if not output_filename:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_filename = f"fallback_img_{timestamp}.jpg"
                        
                    filepath = self.output_dir / output_filename
                    img.save(filepath, quality=95)
                    print(f"✅ Fallback image generated: {filepath}")
                    return str(filepath)
                    
                except ImportError:
                    print("❌ PIL library not found. Cannot generate fallback.")
                    return None
                except Exception as e:
                    print(f"❌ Fallback generation failed: {e}")
                    return None
            
            # Save to local file (Pollinations success path)
            filepath = self.output_dir / output_filename
            with open(filepath, 'wb') as f:
                f.write(image_content)
            
            print(f"✅ Image saved locally: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def cleanup_old_images(self, days_old=7):
        """
        Delete image files older than specified days.
        
        Args:
            days_old (int): Delete files older than this many days
        """
        import time
        current_time = time.time()
        deleted_count = 0
        
        for filepath in self.output_dir.glob("viral_img_*.jpg"):
            file_age_days = (current_time - os.path.getmtime(filepath)) / 86400
            if file_age_days > days_old:
                os.remove(filepath)
                deleted_count += 1
        
        if deleted_count > 0:
            print(f"🧹 Cleaned up {deleted_count} old image files")


if __name__ == "__main__":
    # Test the image generator
    generator = ImageGenerator()
    
    test_prompt = "Viral news graphic about AI investment, cinematic lighting, high contrast, modern tech aesthetic, 8k quality"
    
    image_path = generator.generate_viral_image(test_prompt)
    
    if image_path:
        print(f"\n✅ Test successful! Image saved to: {image_path}")
    else:
        print(f"\n❌ Test failed!")
