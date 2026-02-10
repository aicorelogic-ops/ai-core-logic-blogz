"""
Enhanced Reel Generator with Hyper-Dopamine Framework
Creates viral-style reels using AI-generated scripts
"""

from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
import textwrap
import numpy as np
from .reel_script_generator import ReelScriptGenerator

class ViralReelGenerator:
    def __init__(self):
        self.width = 1080
        self.height = 1920
        self.fps = 30
        self.script_gen = ReelScriptGenerator()
    
    def create_viral_reel(self, article, blog_html, image_url):
        """Generate viral reel using AI-generated script"""
        
        try:
            print("🎬 Generating viral reel...")
            
            # Generate AI script
            print("🤖 Generating viral script with AI...")
            script = self.script_gen.generate_viral_script(article['title'], blog_html)
            
            if not script:
                print("❌ Failed to generate script")
                return None
            
            # Download viral image
            viral_image_path = self._download_image(image_url) if image_url else None
            
            # Create slides based on viral script
            slides = []
            
            # Hook slide (3 seconds) - STOP SCROLLING style
            slides.append(self._create_urgent_slide(
                text=script['hook']['script'],
                overlay_text=script['hook']['text_overlay'],
                image_path=viral_image_path,
                duration=3,
                style='hook'  # Red, urgent
            ))
            
            # Body slides (3-4 slides, ~10s each)
            for i, point in enumerate(script['body']):
                slides.append(self._create_urgent_slide(
                    text=point['script'],
                    overlay_text=point['text_overlay'],
                    image_path=viral_image_path,
                    duration=10,
                    style='body'  # Orange/yellow
                ))
            
            # CTA slide (3 seconds) - Link in bio
            slides.append(self._create_urgent_slide(
                text=script['cta']['script'],
                overlay_text=script['cta']['text_overlay'],
                image_path=viral_image_path,
                duration=3,
                style='cta'  # Green/white
            ))
            
            # Concatenate
            final_video = concatenate_videoclips(slides, method="compose")
            
            # Export
            output_path = os.path.join("blog", "reels", f"{article['title'][:30].replace(' ', '_').replace('/', '_')}_VIRAL.mp4")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio=False,
                preset='medium'
            )
            
            print(f"✅ Viral reel created: {output_path}")
            
            # Cleanup
            if viral_image_path and os.path.exists(viral_image_path):
                os.remove(viral_image_path)
            
            return output_path
            
        except Exception as e:
            import traceback
            print(f"❌ Viral reel generation error: {e}")
            traceback.print_exc()
            return None
    
    def _create_urgent_slide(self, text, overlay_text, image_path, duration, style='body'):
        """Create slide with viral urgent styling"""
        
        # Load/create background
        if image_path and os.path.exists(image_path):
            img = self._load_and_crop_image(image_path)
            # Darken for text readability
            overlay = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            img = Image.blend(img, overlay, 0.7)  # Very dark for urgency
        else:
            img = self._create_urgent_gradient(style)
        
        draw = ImageDraw.Draw(img)
        
        # Style colors based on type
        if style == 'hook':
            text_color = (255, 50, 50)  # Urgent red
            overlay_color = (255, 255, 255)  # White overlay text
        elif style == 'cta':
            text_color = (100, 255, 150)  # Action green
            overlay_color = (255, 255, 255)  # White overlay text
        else:  # body
            text_color = (255, 220, 100)  # Warning orange
            overlay_color = (255, 255, 255)  # White
        
        # Large overlay text at top (TikTok style - ALL CAPS)
        try:
            overlay_font = ImageFont.truetype("arialbd.ttf", 90)
        except:
            overlay_font = ImageFont.truetype("arial.ttf", 90)
        
        # Wrap overlay text
        wrapped_overlay = textwrap.fill(overlay_text, width=15)
        
        # Draw overlay text at top with heavy outline
        bbox = draw.textbbox((0, 0), wrapped_overlay, font=overlay_font)
        overlay_width = bbox[2] - bbox[0]
        overlay_height = bbox[3] - bbox[1]
        
        overlay_x = (self.width - overlay_width) // 2
        overlay_y = 150  # Top third
        
        # Thick black outline (viral style)
        for adj_x in range(-8, 9):
            for adj_y in range(-8, 9):
                draw.text((overlay_x+adj_x, overlay_y+adj_y), wrapped_overlay, fill=(0, 0, 0), font=overlay_font, align="center")
        
        # Main overlay text
        draw.text((overlay_x, overlay_y), wrapped_overlay, fill=overlay_color, font=overlay_font, align="center")
        
        # Script text in middle (readable, conversational)
        try:
            script_font = ImageFont.truetype("arial.ttf", 65)
        except:
            script_font = ImageFont.load_default()
        
        wrapped_script = textwrap.fill(text, width=25)
        
        bbox = draw.textbbox((0, 0), wrapped_script, font=script_font)
        script_width = bbox[2] - bbox[0]
        script_height = bbox[3] - bbox[1]
        
        script_x = (self.width - script_width) // 2
        script_y = (self.height - script_height) // 2
        
        # Outline for script
        for adj_x in range(-6, 7):
            for adj_y in range(-6, 7):
                draw.text((script_x+adj_x, script_y+adj_y), wrapped_script, fill=(0, 0, 0), font=script_font, align="center")
        
        # Script text
        draw.text((script_x, script_y), wrapped_script, fill=text_color, font=script_font, align="center")
        
        # Convert to clip
        img_array = np.array(img)
        clip = ImageClip(img_array).set_duration(duration)
        
        return clip
    
    def _load_and_crop_image(self, image_path):
        """Load and crop image to 9:16 vertical"""
        img = Image.open(image_path).convert('RGB')
        
        img_width, img_height = img.size
        target_ratio = self.width / self.height
        img_ratio = img_width / img_height
        
        if img_ratio > target_ratio:
            new_width = int(img_height * target_ratio)
            left = (img_width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img_height))
        else:
            new_height = int(img_width / target_ratio)
            top = (img_height - new_height) // 2
            img = img.crop((0, top, img_width, top + new_height))
        
        img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
        return img
    
    def _create_urgent_gradient(self, style):
        """Create urgent gradient background"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        
        if style == 'hook':
            # Dark red to black (urgent)
            for y in range(self.height):
                progress = y / self.height
                r = int(50 + (10 - 50) * progress)
                g = int(10 + (10 - 10) * progress)
                b = int(10 + (10 - 10) * progress)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        elif style == 'cta':
            # Dark green to black (action)
            for y in range(self.height):
                progress = y / self.height
                r = int(10 + (10 - 10) * progress)
                g = int(50 + (10 - 50) * progress)
                b = int(10 + (10 - 10) * progress)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        else:
            # Dark orange to black (warning)
            for y in range(self.height):
                progress = y / self.height
                r = int(60 + (10 - 60) * progress)
                g = int(40 + (10 - 40) * progress)
                b = int(10 + (10 - 10) * progress)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        return img
    
    def _download_image(self, url):
        """Download image for background"""
        try:
            import uuid
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                temp_path = f"temp_viral_bg_{uuid.uuid4().hex[:8]}.jpg"
                with open(temp_path, 'wb') as f:
                    f.write(response.content)
                return temp_path
        except Exception as e:
            print(f"⚠️ Image download failed: {e}")
        return None
