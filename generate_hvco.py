import os
import google.generativeai as genai
from dotenv import load_dotenv
from news_bot.blog_generator import BlogGenerator

# Load Environment Variables
load_dotenv(os.path.join("news_bot", ".env"))
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in news_bot/.env")

genai.configure(api_key=API_KEY)

# The "Sabri Suby" System Prompt
SYSTEM_PROMPT = """
You are a Direct Response Copywriter expert in the style of Sabri Suby.
Your goal is to write a High Value Content Offer (HVCO) blog post.

Style Guidelines:
- Use short, punchy sentences. (The "Slippery Slope" method).
- Agitate the pain strongly before offering the solution.
- Use subheads to break up text.
- Tone: Authoritative, slightly controversial, but backed by logic.
- NO fluff. NO generic "In today's fast-paced world..." intros.
- Start with a "Pattern Interrupt" hook.

Format options:
- Use <b> bold </b> for emphasis.
- Use <ul><li> for lists.
- Use <h3> for subheaders.
- Output MUST be raw HTML (no <html> tags, just the body content).
"""

ARTICLES = [
    {
        "type": "Provocative",
        "title": "The Death of the Middle Manager",
        "summary": "Why AI Agents are flattening logistics orgs and saving 40% overhead.",
        "prompt": """
        Write a blog post titled "The Death of the Middle Manager: How AI Agents are Flattening Logistics Orgs".
        
        Key Points:
        1. Hook: Middle Management is the "silent killer" of logistics margins.
        2. Pain: The endless game of "telephone" between dispatch, drivers, and clients.
        3. Solution: Autonomous AI Agents don't just "report" data, they Act.
        4. Proof: Explain how an Agent can negotiate a rate, book a load, and update the CRM in 30 seconds.
        5. Prediction: By 2027, logistics companies will run with 90% fewer managers.
        6. CTA: Don't fire your team, upgrade them to "Agent Architects".
        """
    },
    {
        "type": "Case Study",
        "title": "Case Study: Automating a 50-Person Dispatch Team",
        "summary": "The exact blueprint we used to recover 20 hours/week per dispatcher.",
        "prompt": """
        Write a Case Study titled "We Automated a 50-Person Dispatch Team. Here's the Exact Blueprint."
        
        Key Points:
        1. The Problem: A mid-sized logistics firm was drowning in email. 4,000 emails/day.
        2. The Bottleneck: Humans can't read fast enough. Missed loads = Lost revenue.
        3. The Fix: We deployed "NewsBot's Cousin" - a tailored Inbox Agent.
        4. The Process: It reads probability of booking, drafts replies, and flags high-value loads.
        5. The Result: 20 hours saved per week per dispatcher. Revenue up 15%.
        6. The Blueprint: Step 1 (Audit), Step 2 (Connect API), Step 3 (Train).
        """
    },
    {
        "type": "Tutorial",
        "title": "Tutorial: Build Your Own 'Email Sorter' Bot",
        "summary": "A 10-minute guide to building your first AI logic filter.",
        "prompt": """
        Write a technical but accessible Tutorial titled "How to Build Your Own 'Email Sorter' Bot in 10 Minutes".
        
        Key Points:
        1. The Promise: You don't need to be a coder to use Logic.
        2. The Stack: Python + Gemini API + Gmail API.
        3. The Concept: "If Email contains 'Invoice', move to 'Finance'. Else, archive."
        4. The Code: Provide pseudo-code or simple Python snippets for the logic loop.
        5. The Benefit: "One clean inbox = Peace of mind."
        """
    }
]

def generate_hvco():
    print("🚀 Starting HVCO Generator (Sabri Mode)...")
    
    blog_gen = BlogGenerator()
    # Updated to use the available model from list_models.py
    model = genai.GenerativeModel('models/gemini-2.0-flash')

    import time
    from google.api_core import exceptions

    for article in ARTICLES:
        print(f"\n✍️ Writing: {article['title']}...")
        
        # Retry Logic for Rate Limits
        max_retries = 5
        base_delay = 10
        
        for attempt in range(max_retries):
            try:
                # Generate Content
                full_prompt = f"{SYSTEM_PROMPT}\n\nTASK:\n{article['prompt']}"
                response = model.generate_content(full_prompt)
                content_html = response.text.replace("```html", "").replace("```", "")
                break # Success, exit retry loop
            except exceptions.ResourceExhausted:
                wait_time = base_delay * (2 ** attempt)
                print(f"⚠️ Rate Limit Hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            except Exception as e:
                print(f"❌ Error generating content: {e}")
                content_html = None
                break
        
        if not content_html:
            print(f"❌ Skipping {article['title']} after failures.")
            continue

        # Create Post
        filename = blog_gen.create_post(
            title=article['title'],
            content_html=content_html,
            original_link="https://aicorelogic.com/services"  # Self-referential source
        )
        
        # Update Index
        blog_gen.update_index(
            title=article['title'],
            summary=article['summary'],
            filename=filename
        )
        
        # Safety Sleep between articles
        print("💤 Cooling down API for 20 seconds...")
        time.sleep(20)

    # Deploy
    print("\n☁️ Deploying all changes to GitHub...")
    blog_gen.deploy_to_github()

if __name__ == "__main__":
    generate_hvco()
