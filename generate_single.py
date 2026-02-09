import os
import google.generativeai as genai
from dotenv import load_dotenv
from news_bot.blog_generator import BlogGenerator

# Load Environment Variables
load_dotenv(os.path.join("news_bot", ".env"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use gemini-2.0-flash (Available)
model = genai.GenerativeModel('models/gemini-2.0-flash')

SYSTEM_PROMPT = """
You are a Direct Response Copywriter expert in the style of Sabri Suby.
Your goal is to write a High Value Content Offer (HVCO) blog post.
Style Guidelines:
- Use short, punchy sentences.
- Agitate the pain strongly.
- NO fluff.
- Output MUST be raw HTML (no <html> tags).
"""

PROMPT = """
Write a blog post titled "The Death of the Middle Manager: How AI Agents are Flattening Logistics Orgs".
Key Points:
1. Hook: Middle Management is the "silent killer" of logistics margins.
2. Pain: The endless game of "telephone" between dispatch, drivers, and clients.
3. Solution: Autonomous AI Agents don't just "report" data, they Act.
4. Proof: Explain how an Agent can negotiate a rate, book a load, and update the CRM in 30 seconds.
5. Prediction: By 2027, logistics companies will run with 90% fewer managers.
6. CTA: Don't fire your team, upgrade them to "Agent Architects".
"""

def generate_single():
    print("🚀 Generating Single Article: Death of the Middle Manager...")
    
    import time
    from google.api_core import exceptions
    
    max_retries = 5
    base_delay = 20 # Start with 20s
    
    content_html = None
    
    for attempt in range(max_retries):
        try:
            print(f"🔄 Attempt {attempt+1}/{max_retries}...")
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\nTASK:\n{PROMPT}")
            content_html = response.text.replace("```html", "").replace("```", "")
            break
        except exceptions.ResourceExhausted:
            wait_time = base_delay * (2 ** attempt)
            print(f"⚠️ Rate Limit Hit. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"❌ Error: {e}")
            return

    if not content_html:
        print("❌ Failed to generate content after retries.")
        return

    try:
        blog_gen = BlogGenerator()
        filename = blog_gen.create_post(
            title="The Death of the Middle Manager",
            content_html=content_html,
            original_link="https://aicorelogic.com/future"
        )
        
        blog_gen.update_index(
            title="The Death of the Middle Manager",
            summary="Why AI Agents are flattening logistics orgs.",
            filename=filename
        )
        
        print("☁️ Auto-Deploying...")
        blog_gen.deploy_to_github()
        
    except Exception as e:
        print(f"❌ Error during file creation/deploy: {e}")

if __name__ == "__main__":
    generate_single()
