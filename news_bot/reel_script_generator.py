"""
AI-Powered Viral Reel Script Generator
Uses Hyper-Dopamine Framework to convert articles into viral video scripts
"""

import google.generativeai as genai
from .settings import GOOGLE_API_KEY

class ReelScriptGenerator:
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_viral_script(self, article_title, blog_html):
        """
        Convert article into viral reel script using Hyper-Dopamine framework.
        
        Returns:
        {
            'hook': {'visual': str, 'text_overlay': str, 'script': str},
            'body': [{'visual': str, 'text_overlay': str, 'script': str}, ...],
            'cta': {'visual': str, 'text_overlay': str, 'script': str}
        }
        """
        
        prompt = f"""Role: You are a Viral Video Strategist and Direct Response Copywriter.

Task: Convert this article into a 30-60 second viral Facebook Reel script using the Hyper-Dopamine Framework.

CRITICAL RULES:
1. Extract SPECIFIC NUMBERS from the article (percentages, dollar amounts, statistics)
2. Use URGENT language ("STOP," "EXPOSED," "LEAKED," "WARNING")
3. Make it feel like USER-GENERATED CONTENT, not a commercial
4. Each line must use the "Slippery Slope" - make them want to hear the next line
5. Sell the CLICK, not the product

Article Title: {article_title}

Article Content:
{blog_html}

Output a JSON object with this EXACT structure:
{{
  "hook": {{
    "visual": "Description of opening visual",
    "text_overlay": "Large grabber text in ALL CAPS with emoji",
    "script": "Opening line (3-5 words max, urgent)"
  }},
  "body": [
    {{
      "visual": "Visual for this point",
      "text_overlay": "Key number or finding in CAPS",
      "script": "Specific finding with exact number"
    }},
    {{
      "visual": "Visual for next point",
      "text_overlay": "Another key stat in CAPS", 
      "script": "Another specific finding"
    }},
    {{
      "visual": "Visual for solution",
      "text_overlay": "Solution stat in CAPS",
      "script": "What was discovered"
    }}
  ],
  "cta": {{
    "visual": "Urgent CTA visual",
    "text_overlay": "TAP LINK BELOW",
    "script": "Urgency-based CTA"
  }}
}}

Return ONLY the JSON object, no markdown formatting."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.9,
                    response_mime_type="application/json"
                )
            )
            
            import json
            
            # Get response text
            response_text = response.text.strip()
            print(f"Raw response: {response_text[:200]}...")
            
            # Parse JSON
            script = json.loads(response_text)
            
            print("✅ Viral script generated successfully!")
            return script
            
        except Exception as e:
            print(f"❌ Script generation error: {e}")
            import traceback
            traceback.print_exc()
            
            # Fallback to simpler script
            print("⚠️ Using fallback script...")
            return self._create_fallback_script(article_title, blog_html)
    
    def _create_fallback_script(self, article_title, blog_html):
        """Create a basic script if AI generation fails"""
        return {
            "hook": {
                "visual": "Screenshot with red circle on key number",
                "text_overlay": "STOP SCROLLING ⚠️",
                "script": "Stop if you run a small business"
            },
            "body": [
                {
                    "visual": "Zoom into £50K number",
                    "text_overlay": "£50,000 WASTED YEARLY 💸",
                    "script": "Your gut feeling is costing you £50K a year"
                },
                {
                    "visual": "Flash effect on 40%",
                    "text_overlay": "40% FASTER WITH AI ⚡",
                    "script": "Businesses using AI move 40% faster"
                },
                {
                    "visual": "Green checkmark appearing",
                    "text_overlay": "FREE SOLUTION RELEASED ✅",
                    "script": "Square AI just dropped - completely free"
                }
            ],
            "cta": {
                "visual": "Pulsing LINK IN BIO banner",
                "text_overlay": "TAP LINK BELOW ⬇️",
                "script": "Full breakdown in bio before it's removed"
            }
        }
    
    def format_script_for_display(self, script):
        """Format script as readable table for review"""
        if not script:
            return "No script generated"
        
        output = "## Viral Reel Script\n\n"
        output += "| Time | Visual/Action | Audio/Script | Text Overlay |\n"
        output += "|------|---------------|--------------|---------------|\n"
        
        # Hook (0-3s)
        output += f"| 0-3s | {script['hook']['visual']} | {script['hook']['script']} | {script['hook']['text_overlay']} |\n"
        
        # Body (3-45s)
        time_start = 3
        for i, point in enumerate(script['body']):
            time_end = time_start + 12  # ~12s per point
            output += f"| {time_start}-{time_end}s | {point['visual']} | {point['script']} | {point['text_overlay']} |\n"
            time_start = time_end
        
        # CTA (45-60s)
        output += f"| {time_start}-60s | {script['cta']['visual']} | {script['cta']['script']} | {script['cta']['text_overlay']} |\n"
        
        return output
