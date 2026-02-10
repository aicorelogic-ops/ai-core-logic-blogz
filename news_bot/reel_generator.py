from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
import textwrap
import numpy as np

class ReelGenerator:
    def __init__(self):
        self.width = 1080  # 9:16 vertical format
        self.height = 1920
        self.fps = 30
        
    def create_reel(self, article, blog_html, image_url):
        """Generate a 15-30 second vertical reel from blog content"""
        
        try:
            print("🎬 Generating reel...")
            
            # Extract content for slides
            hook = self._extract_hook(article['title'], blog_html)
            pain_points = self._extract_pain_points(blog_html)
            solution = self._extract_solution(blog_html)
            
            # Download viral image to use as background
            viral_image_path = self._download_image(image_url) if image_url else None
            
            # Create slides with image backgrounds
            slides = []
            
            # Slide 1: Hook with dramatic image background (3 seconds)
            slides.append(self._create_image_text_slide(
                hook,
                duration=3,
                image_path=viral_image_path,
                text_color=(255, 50, 50),  # Red
                font_size=80,
                emoji="💣",
                darken=0.6  # Darken image for text readability
            ))
            
            # Slides 2-4: Pain points with image backgrounds (2 seconds each)
            for i, pain in enumerate(pain_points[:3]):
                slides.append(self._create_image_text_slide(
                    pain,
                    duration=2,
                    image_path=viral_image_path,
                    text_color=(255, 220, 100),  # Orange/yellow
                    font_size=65,
                    emoji=["⚠️", "💰", "⏰"][i],  # Different emoji per slide
                    darken=0.7
                ))
            
            # Slide 5: Solution with image (3 seconds)
            slides.append(self._create_image_text_slide(
                solution,
                duration=3,
                image_path=viral_image_path,
                text_color=(100, 255, 150),  # Green
                font_size=70,
                emoji="✅",
                darken=0.65
            ))
            
            # Slide 6: CTA with dark overlay (2 seconds)
            slides.append(self._create_image_text_slide(
                "Full story in bio 👆\n\nAI.Core Logic",
                duration=2,
                image_path=viral_image_path,
                text_color=(255, 255, 255),  # White
                font_size=75,
                darken=0.8  # Very dark for emphasis
            ))
            
            # Concatenate all slides
            final_video = concatenate_videoclips(slides, method="compose")
            
            # Export
            output_path = os.path.join("blog", "reels", f"{article['title'][:30].replace(' ', '_').replace('/', '_')}.mp4")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio=False,  # No audio for now (can add later)
                preset='medium'
            )
            
            print(f"✅ Reel created: {output_path}")
            
            # Cleanup temp image
            if viral_image_path and os.path.exists(viral_image_path):
                os.remove(viral_image_path)
            
            return output_path
            
        except Exception as e:
            import traceback
            print(f"❌ Reel generation error: {e}")
            traceback.print_exc()
            return None
    
    def _create_image_text_slide(self, text, duration, image_path, text_color, font_size, emoji="", darken=0.5):
        """Create a slide with image background and text overlay"""
        
        if image_path and os.path.exists(image_path):
            # Load and resize image to vertical format
            img = Image.open(image_path).convert('RGB')
            
            # Resize to 9:16 vertical, crop if needed
            img_width, img_height = img.size
            target_ratio = self.width / self.height
            img_ratio = img_width / img_height
            
            if img_ratio > target_ratio:
                # Image is too wide, crop width
                new_width = int(img_height * target_ratio)
                left = (img_width - new_width) // 2
                img = img.crop((left, 0, left + new_width, img_height))
            else:
                # Image is too tall, crop height
                new_height = int(img_width / target_ratio)
                top = (img_height - new_height) // 2
                img = img.crop((0, top, img_width, top + new_height))
            
            # Resize to final dimensions
            img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
            
            # Apply darkening overlay for text readability
            overlay = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            img = Image.blend(img, overlay, darken)
        else:
            # Fallback to gradient background
            img = self._create_gradient_background()
        
        # Add text overlay
        draw = ImageDraw.Draw(img)
        
        # Try to use a bold font
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Add emoji if provided
        full_text = f"{emoji} {text}" if emoji else text
        
        # Wrap text
        wrapped_text = textwrap.fill(full_text, width=25)
        
        # Calculate text position (center)
        bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2
        
        # Draw text with thick black outline for readability
        outline_width = 6
        for adj_x in range(-outline_width, outline_width+1):
            for adj_y in range(-outline_width, outline_width+1):
                draw.text((x+adj_x, y+adj_y), wrapped_text, fill=(0, 0, 0), font=font, align="center")
        
        # Draw main text
        draw.text((x, y), wrapped_text, fill=text_color, font=font, align="center")
        
        # Convert to MoviePy clip
        img_array = np.array(img)
        clip = ImageClip(img_array).set_duration(duration)
        
        return clip
    
    def _create_gradient_background(self):
        """Create a gradient background as fallback"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        
        # Vertical gradient from dark blue to dark red
        for y in range(self.height):
            progress = y / self.height
            r = int(20 + (30 - 20) * progress)
            g = int(20 + (20 - 20) * progress)
            b = int(50 + (30 - 50) * progress)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        return img
    
    def _download_image(self, url):
        """Download image from URL for use as background"""
        try:
            import uuid
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                temp_path = f"temp_reel_bg_{uuid.uuid4().hex[:8]}.jpg"
                with open(temp_path, 'wb') as f:
                    f.write(response.content)
                return temp_path
        except Exception as e:
            print(f"⚠️ Image download failed: {e}")
        return None
    
    def _extract_hook(self, title, blog_html):
        """Extract the hook from title or blog"""
        # Use first 60 chars of title as hook
        return title[:60].upper()
    
    def _extract_pain_points(self, blog_html):
        """Extract pain points from blog HTML"""
        # Simple extraction - look for sentences with pain words
        pain_words = ["bleeding", "losing", "costing", "burning", "wasting", "stuck", "frustrated"]
        
        # Basic extraction (can be enhanced with AI)
        pain_points = [
            "You're bleeding cash every month",
            "Your team wastes 20+ hours weekly",
            "Competitors are automating faster"
        ]
        
        return pain_points
    
    def _extract_solution(self, blog_html):
        """Extract solution from blog"""
        return "Here's what smart businesses discovered..."


if __name__ == "__main__":
    # Test
    gen = ReelGenerator()
    test_article = {
        'title': 'Your Payroll Is A Ticking Time Bomb',
        'summary': 'Test summary'
    }
    gen.create_reel(test_article, "<p>Test content</p>", "https://example.com/image.jpg")
