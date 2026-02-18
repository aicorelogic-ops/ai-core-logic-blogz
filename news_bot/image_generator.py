"""
Multi-Provider Image Generator with Robust Fallbacks
Supports: Pollinations AI (free), DALL-E 3 (paid), PIL text graphics (fallback)
"""

import os
from pathlib import Path
from datetime import datetime
import urllib.parse
import requests
import random

class ImageGenerator:
    def __init__(self):
        """Initialize image generator with multiple providers."""
        # Create temp_images directory
        self.output_dir = Path(__file__).parent.parent / 'temp_images'
        self.output_dir.mkdir(exist_ok=True)
        
        # Check for OpenAI API key (optional)
        from .settings import OPENAI_API_KEY
        self.openai_key = OPENAI_API_KEY if OPENAI_API_KEY else None
        
        print(f"✅ Image Generator initialized")
        print(f"   Primary: Vertex AI Imagen 3.0 (Google Cloud, free tier)")
        print(f"   Fallback: Pollinations AI (free)")
        print(f"   Optional: {'DALL-E 3 (paid)' if self.openai_key else 'DALL-E 3 - add OPENAI_API_KEY'}")
        print(f"   Output: {self.output_dir}")
    
    

    def generate_image(self, prompt, output_filename=None, use_dalle=False, use_vertex=True, title=None):
        """
        Generates an image from a text prompt using available providers.
        Tries Vertex AI first, then DALL-E 3, then Pollinations AI.
        
        Args:
            prompt (str): Text prompt describing the image to generate
            output_filename (str, optional): Custom filename. Auto-generated if not provided.
            use_dalle (bool): If True, try DALL-E 3 (requires API key)
            use_vertex (bool): If True, try Vertex AI Imagen first (default: True)
            title (str, optional): Blog title for text overlay.
        
        Returns:
            str: Absolute path to the saved image file, or None if all providers fail
        """
        # Try Vertex AI Imagen first (Google Cloud - free tier available)
        if use_vertex:
            try:
                return self._generate_with_vertex(prompt, output_filename, title=title)
            except Exception as e:
                print(f"❌ Vertex AI Imagen failed: {e}")
                print(f"🔄 Trying next provider...")
        
        # Try DALL-E 3 second if requested and available
        if use_dalle and self.openai_key:
            try:
                return self._generate_with_dalle(prompt, output_filename, title=title)
            except Exception as e:
                print(f"❌ DALL-E 3 failed: {e}")
                print(f"🔄 Falling back to Pollinations AI...")
        
        # Try Pollinations AI (free but can be unreliable)
        try:
            return self._generate_with_pollinations(prompt, output_filename)
        except Exception as e:
            print(f"❌ Pollinations AI failed: {e}")
            print(f"⚠️ No fallback - returning None (post will be skipped)")
            return None
    
    
    def _generate_with_vertex(self, prompt, output_filename=None, title=None):
        """Generate image using Vertex AI Imagen 3.0 (Google Cloud, free tier available)."""
        print(f"🎨 Generating with Vertex AI Imagen 3.0...")
        print(f"   Prompt: {prompt[:100]}...")
        
        import os
        import vertexai
        from vertexai.preview.vision_models import ImageGenerationModel
        from pathlib import Path
        
        # Get Vertex AI config
        from .settings import VERTEX_PROJECT_ID, VERTEX_LOCATION, VERTEX_KEY_PATH
        
        # Set credentials if provided
        if VERTEX_KEY_PATH:
            key_path = Path(__file__).parent / VERTEX_KEY_PATH
            if key_path.exists():
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(key_path)
                print(f"   Using service account: {VERTEX_KEY_PATH}")
            else:
                raise Exception(f"Service account key not found: {key_path}")
        
        # Initialize Vertex AI
        vertexai.init(project=VERTEX_PROJECT_ID, location=VERTEX_LOCATION)
        
        # Load the model - imagen-3.0-generate-001 is the working model
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        print(f"   ✅ Model loaded")
        
        # Generate image
        print(f"   Generating image...")
        response = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio="1:1",  # Changed to square for better social feed/overlay
            safety_filter_level="block_some",
            person_generation="allow_adult"
        )
        
        if not response.images:
            raise Exception("No images in response")
        
        print(f"   ✅ Image generated!")
        
        # Generate filename
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"vertex_img_{timestamp}.jpg"
        
        # Save to local file
        filepath = self.output_dir / output_filename
        response.images[0].save(location=str(filepath))
        
        print(f"✅ Vertex AI image saved: {filepath}")
        
        # Apply overlay if title provided
        if title:
            self.add_news_overlay(filepath, title)
            
        return str(filepath)
    
    
    def add_news_overlay(self, image_path, title):
        """Adds a news-style text overlay to the image."""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Load image
            img = Image.open(image_path).convert("RGBA")
            width, height = img.size
            
            # Create overlay layer
            overlay = Image.new('RGBA', (width, height), (0,0,0,0))
            draw = ImageDraw.Draw(overlay)
            
            # 1. Dark Gradient at Bottom (40% height)
            gradient_start_y = int(height * 0.6)
            for y in range(gradient_start_y, height):
                alpha = int((y - gradient_start_y) / (height - gradient_start_y) * 220)
                draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
            
            # 2. Text Configuration
            font_size = int(height * 0.06)  # 6% of height
            try:
                font = ImageFont.truetype("arialbd.ttf", font_size)
            except IOError:
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except IOError:
                    font = ImageFont.load_default()
            
            # 3. Text Wrapping
            import textwrap
            chars_per_line = 25 
            lines = textwrap.wrap(title.upper(), width=chars_per_line)
            lines = lines[:3] # Limit lines
            
            # 4. Draw Text
            line_height = int(font_size * 1.3)
            total_text_height = len(lines) * line_height
            
            margin_x = int(width * 0.05)
            margin_bottom = int(height * 0.08)
            current_y = height - margin_bottom - total_text_height
            
            # Draw Tag
            tag_text = "AI.CORELOGIC UPDATE"
            tag_font_size = int(font_size * 0.4)
            try:
                tag_font = ImageFont.truetype("arialbd.ttf", tag_font_size)
            except:
                tag_font = font
            
            # Tag background
            tag_bg_y1 = current_y - int(tag_font_size * 2.0)
            tag_bg_y2 = current_y - int(tag_font_size * 0.5)
            draw.rectangle(
                [margin_x, tag_bg_y1, margin_x + int(width*0.35), tag_bg_y2],
                fill="#FF0050"
            )
            draw.text((margin_x + 5, tag_bg_y1 + int(tag_font_size*0.2)), tag_text, font=tag_font, fill="white")

            # Draw Title Lines
            for line in lines:
                # Shadow
                draw.text((margin_x + 2, current_y + 2), line, font=font, fill=(0,0,0,180))
                # Text
                draw.text((margin_x, current_y), line, font=font, fill="white")
                current_y += line_height
            
            # Composite
            out = Image.alpha_composite(img, overlay)
            out = out.convert("RGB")
            out.save(image_path, quality=95)
            print(f"   ✅ Added News Overlay to {image_path}")
            
        except Exception as e:
            print(f"❌ Failed to add overlay: {e}") 
    
    def _generate_with_dalle(self, prompt, output_filename=None, title=None):
        """Generate image using DALL-E 3 (paid, ~$0.04/image)."""
        print(f"🎨 Generating with DALL-E 3...")
        print(f"   Prompt: {prompt[:100]}...")
        
        import openai
        openai.api_key = self.openai_key
        
        # Generate image
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",  # Square format
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        
        # Download the image
        import requests
        img_response = requests.get(image_url, timeout=30)
        img_response.raise_for_status()
        
        # Generate filename
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"dalle_img_{timestamp}.png"
        
        # Save to local file
        filepath = self.output_dir / output_filename
        with open(filepath, 'wb') as f:
            f.write(img_response.content)
        
        print(f"✅ DALL-E 3 image saved: {filepath}")
        print(f"   Size: {len(img_response.content)} bytes")
        
        # Apply overlay if title provided
        if title:
            self.add_news_overlay(filepath, title)
            
        return str(filepath)
    
    
    def _generate_with_pollinations(self, prompt, output_filename=None):
        """Generate image using Pollinations AI (free, works great, occasional rate limits)."""
        print(f"🎨 Generating with Pollinations AI...")
        print(f"   Prompt: {prompt[:100]}...")
        
        # Use Pollinations AI URL
        safe_prompt = urllib.parse.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1200&height=630&nologo=true"
        
        # Retry logic for occasional rate limiting (HTTP 530)
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    # Exponential backoff: wait 2s, 4s, 8s...
                    import time
                    wait_time = 2 ** attempt
                    print(f"   Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                
                print(f"   Attempt {attempt + 1}/{max_retries}: Downloading...")
                
                # Simple, straightforward request
                response = requests.get(image_url, timeout=60)
                
                # Check status
                if response.status_code != 200:
                    # Rate limit or service issue
                    error_msg = f"HTTP {response.status_code}: {response.text[:100]}"
                    if attempt < max_retries - 1:
                        print(f"   ⚠️ {error_msg}, retrying...")
                        continue
                    else:
                        raise Exception(error_msg)
                
                # Check if we got actual image data
                if len(response.content) < 1000:
                    raise Exception(f"Image too small ({len(response.content)} bytes)")
                
                # Success!
                print(f"   ✅ Downloaded {len(response.content)} bytes")
                break
                
            except requests.Timeout:
                if attempt < max_retries - 1:
                    print(f"   ⏱️ Timeout, retrying...")
                    continue
                else:
                    raise Exception("Pollinations timeout after all retries")
            except Exception as e:
                if attempt < max_retries - 1 and "HTTP" in str(e):
                    # Retry HTTP errors (rate limiting)
                    continue
                else:
                    # Don't retry other errors or last attempt
                    raise
        
        # Generate filename
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"pollinations_img_{timestamp}.jpg"
        
        # Save to local file
        filepath = self.output_dir / output_filename
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Pollinations image saved: {filepath}")
        return str(filepath)
    
    
    def _generate_with_pil(self, prompt, output_filename=None):
        """Generate text-based image using PIL (always works, free)."""
        print(f"🎨 Generating with PIL (text graphic)...")
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            import textwrap
            
            width = 1200
            height = 630
            
            # Dark blue background
            img = Image.new('RGB', (width, height), color=(10, 25, 47))
            d = ImageDraw.Draw(img)
            
            # Try to load a font
            try:
                font_size = 60
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()
                
            # Prepare text (extract main subject from prompt)
            text_content = prompt.replace("Editorial news graphic about ", "")
            text_content = text_content.split(",")[0]
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
                
            # Generate filename
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"pil_img_{timestamp}.jpg"
                
            # Save
            filepath = self.output_dir / output_filename
            img.save(filepath, quality=95)
            print(f"✅ PIL image saved: {filepath}")
            return str(filepath)
            
        except ImportError:
            print("❌ PIL library not found!")
            return None
        except Exception as e:
            print(f"❌ PIL generation failed: {e}")
            return None
    
    
    def create_viral_prompt(self, title):
        """
        Create a viral-style prompt using Direct Response Marketing frameworks.
        Based on "Pattern Interrupt" and "Burning Intrigue" principles.
        
        Args:
            title (str): Article title to base the prompt on
        
        Returns:
            str: Viral-style image prompt optimized for Vertex AI Imagen 3.0
        """
        # Extract the subject/topic from the title
        clean_title = title.replace(":", "").replace("-", "")
        # Get the core subject (first 6-8 words)
        image_hook = " ".join(clean_title.split()[:8])
        
        # New "Content-First" Viral Prompt Strategy
        # We want the image to actually depict the TOPIC, but with a viral/dramatic style.
        # Format: [Subject Action/Scene] + [Viral Visual Style] + [Atmosphere]
        
        viral_style = (
            "Visual Style: Hyper-realistic 8k resolution, cinematic lighting, high contrast, "
            "dramatic shadows, depth of field, detailed texture. "
            "Aesthetic: 'Breaking News' intensity, urgency, modern, slightly gritty but professional."
        )
        
        # Construct the scene description based on the hook
        scene_description = (
            f"A dramatic, high-stakes scene depicting '{image_hook}'. "
            f"Make the subject matter the central focus. "
            f"If technology: show glowing servers, data streams, or futuristic interfaces. "
            f"If business/finance: show intense boardroom discussions, stock crashes, or piles of money. "
            f"If policy/law: show gavels, documents, or government buildings with storm clouds. "
            f"Key elements: A sense of motion, impact, or consequence. "
            f"The image should tell a story about '{image_hook}' without using text."
        )

        selected_prompt = f"{scene_description} {viral_style}"
        
        # Add Negative Prompt constraints (what to avoid)
        negative_constraints = (
            " --negative_prompt: blurry, low quality, cartoon, anime, effortless, "
            "boring, plain white background, distorted faces, bad anatomy, "
            "watermark, text, signature, ugly, deformed"
        )
        
        return selected_prompt + negative_constraints
    
    
    def cleanup_old_images(self, days_old=7):
        """Delete image files older than specified days."""
        import time
        current_time = time.time()
        deleted_count = 0
        
        for filepath in self.output_dir.glob("*.jpg"):
            file_age_days = (current_time - os.path.getmtime(filepath)) / 86400
            if file_age_days > days_old:
                os.remove(filepath)
                deleted_count += 1
        
        if deleted_count > 0:
            print(f"🧹 Cleaned up {deleted_count} old image files")


if __name__ == "__main__":
    # Test the image generator
    generator = ImageGenerator()
    
    test_title = "AI Threatens to Eat Business Software and It Could Happen Fast"
    viral_prompt = generator.create_viral_prompt(test_title)
    
    print(f"\n📝 Generated viral prompt:")
    print(f"   {viral_prompt[:150]}...")
    
    # Test with Pollinations (will fall back to PIL if Pollinations is down)
    image_path = generator.generate_image(viral_prompt, title=test_title)
    
    if image_path:
        print(f"\n✅ Test successful! Image saved to: {image_path}")
    else:
        print(f"\n❌ Test failed!")
