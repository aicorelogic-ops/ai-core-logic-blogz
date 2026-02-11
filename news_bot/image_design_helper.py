"""
Helper module to analyze news articles and generate 
design specifications for Facebook post images.

Inspired by professional news network graphics:
- ABC News (photo + bold headline overlay)
- Variety / Bloomberg (entertainment/business news aesthetic)
- Professional photojournalism style
"""

import google.generativeai as genai
from .settings import GOOGLE_API_KEY


def analyze_article_visual_context(article):
    """
    Analyzes article and returns visual design specifications
    inspired by news network graphics (ABC, Bloomberg, Variety style).
    
    Args:
        article (dict): Article with 'title' and 'summary' keys
        
    Returns:
        dict: {
            'scene': str,           # Background photo description
            'emotion_trigger': str, # Visual mood (urgent/professional/exciting)
            'category_badge': str,  # Badge text (BREAKING NEWS, TECH UPDATE, etc.)
            'headline_position': str, # 'bottom' (default for news overlay style)
            'color_scheme': str     # Primary color scheme
        }
    """
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-flash-latest')  # Same model as processor.py
        
        prompt = f"""Analyze this news article and provide visual design specifications for a Facebook post image.

Article Title: {article['title']}
Summary: {article.get('summary', '')[:300]}

Create specifications for a NEWS OVERLAY GRAPHIC (ABC News / Variety / Bloomberg style):

Return ONLY a JSON object with these exact keys (no markdown, no explanation):
{{
    "scene": "Detailed description of background photo/scene that visually represents the story",
    "emotion_trigger": "Choose ONE: urgent | professional | exciting | concerning | inspiring",
    "category_badge": "Choose appropriate badge: BREAKING NEWS | TECH UPDATE | BUSINESS | AI NEWS | INDUSTRY ALERT",
    "headline_position": "bottom",
    "color_scheme": "Primary color for accents (e.g., 'vibrant red', 'tech blue', 'gold')"
}}

Examples:
- For breaking AI news: {{"scene": "Modern AI datacenter with servers and blue lighting", "emotion_trigger": "urgent", "category_badge": "BREAKING NEWS", "headline_position": "bottom", "color_scheme": "electric blue"}}
- For business update: {{"scene": "Professional business meeting with charts on screen", "emotion_trigger": "professional", "category_badge": "BUSINESS", "headline_position": "bottom", "color_scheme": "corporate navy blue"}}"""

        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Parse JSON response
        import json
        import re
        
        # Remove markdown code blocks if present
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        
        design_specs = json.loads(text)
        
        # Validate and provide defaults
        return {
            'scene': design_specs.get('scene', 'modern office with technology'),
            'emotion_trigger': design_specs.get('emotion_trigger', 'professional'),
            'category_badge': design_specs.get('category_badge', 'NEWS'),
            'headline_position': 'bottom',  # Always bottom for news overlay style
            'color_scheme': design_specs.get('color_scheme', 'vibrant blue')
        }
        
    except Exception as e:
        print(f"Warning: Design analysis failed: {e}, using defaults")
        # Fallback defaults
        return {
            'scene': 'modern technology workspace with computers',
            'emotion_trigger': 'professional',
            'category_badge': 'NEWS',
            'headline_position': 'bottom',
            'color_scheme': 'vibrant blue'
        }


def create_news_overlay_prompt(article, design_specs, image_idea=None):
    """
    Creates Pollinations AI prompt for news-style overlay graphic.
    
    Inspired by designs in:
    - ABC News graphics (photo + bold headline overlay)
    - Variety entertainment news style
    - Bloomberg business news aesthetic
    
    Args:
        article (dict): Article with 'title' key
        design_specs (dict): Output from analyze_article_visual_context()
        image_idea (str, optional): AI-suggested image idea from processor
        
    Returns:
        str: Optimized prompt for Pollinations AI
    """
    # Extract headline (truncate if too long for visual display)
    headline = article['title'][:80] if len(article['title']) > 80 else article['title']
    
    # Build scene description
    if image_idea:
        # If processor provided specific idea, incorporate it
        scene_desc = f"{image_idea}, {design_specs['scene']}"
    else:
        scene_desc = design_specs['scene']
    
    # Mood descriptors based on emotion trigger
    mood_map = {
        'urgent': 'dramatic lighting, high contrast, tense atmosphere',
        'professional': 'clean lighting, corporate aesthetic, polished',
        'exciting': 'dynamic composition, vibrant colors, energetic',
        'concerning': 'somber tones, serious mood, documentary style',
        'inspiring': 'warm lighting, uplifting composition, aspirational'
    }
    mood = mood_map.get(design_specs['emotion_trigger'], 'professional lighting')
    
    # Create comprehensive prompt
    prompt = f"""Professional news network graphic in the style of ABC News or Bloomberg television:

PHOTO BACKGROUND: {scene_desc}, photojournalism quality, {mood}

TEXT OVERLAY ELEMENTS:
- Large bold white sans-serif headline at BOTTOM with dark gradient backdrop: "{headline}"
- Small category badge in TOP-LEFT corner: "{design_specs['category_badge']}" in {design_specs['color_scheme']} color
- Subtle dark gradient overlay (50% opacity) across bottom third for text readability
- Clean professional typography similar to ABC News or Variety magazine graphics

STYLE SPECIFICATIONS:
- High-quality photojournalistic image, not amateur or casual
- Corporate news network aesthetic
- Text must be clearly readable and prominent
- {design_specs['emotion_trigger']} visual mood
- Composition suitable for social media thumbnail
- No watermarks or logos except subtle "NEWS" badge

TECHNICAL: 1200x630 aspect ratio, optimized for Facebook feed"""

    return prompt


if __name__ == "__main__":
    # Test the helper functions
    sample_article = {
        'title': 'New AI Tool Automates 95% of Logistics Paperwork, Saves Companies $40K Monthly',
        'summary': 'A revolutionary AI platform is transforming the logistics industry by automating invoice processing.'
    }
    
    print("Analyzing article for visual design...")
    specs = analyze_article_visual_context(sample_article)
    print(f"\nDesign Specs: {specs}")
    
    print("\n" + "="*80)
    print("Generated Image Prompt:")
    print("="*80)
    prompt = create_news_overlay_prompt(sample_article, specs)
    print(prompt)
