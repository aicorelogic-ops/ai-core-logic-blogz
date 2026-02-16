from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def create_text_image(text, output_path, bg_color=(20, 20, 30), text_color=(255, 255, 255)):
    """Create a simple news graphic with text."""
    width = 1200
    height = 630
    img = Image.new('RGB', (width, height), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()
        
    # Wrap text
    lines = textwrap.wrap(text, width=30)
    
    # Calculate text height
    # Using basic spacing for default font
    line_height = 80 
    total_text_height = len(lines) * line_height
    
    y_text = (height - total_text_height) / 2
    
    for line in lines:
        try:
            # bbox is more accurate for newer Pillow
            bbox = d.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
        except AttributeError:
             # Fallback for older Pillow
             line_width = d.textlength(line, font=font)
             
        x_text = (width - line_width) / 2
        d.text((x_text, y_text), line, font=font, fill=text_color)
        y_text += line_height
        
    img.save(output_path)
    return output_path

if __name__ == "__main__":
    create_text_image("Blackstone Invests $600M in AI Infrastructure", "test_graphic.jpg")
