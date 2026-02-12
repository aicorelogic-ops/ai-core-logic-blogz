
import json
import os
import time
import urllib.parse
from .publisher import FacebookPublisher
from .article_tracker import ArticleTracker
from dotenv import load_dotenv

load_dotenv()

def retry_latest_post():
    tracker = ArticleTracker()
    
    # 1. Load the tracking file
    if not os.path.exists(tracker.tracking_file):
        print("No tracking file found.")
        return

    with open(tracker.tracking_file, 'r') as f:
        data = json.load(f)
    
    # 2. Find the latest article that has NO photo_id
    # Sort by date descending
    sorted_items = sorted(data.items(), key=lambda x: x[1].get('processed_date', ''), reverse=True)
    
    target_url = None
    article_data = None
    
    for url, info in sorted_items:
        # Check for missing photo ID and ensure it's a blog post we generated
        if info.get('facebook_photo_id') is None and 'blog_path' in info:
            target_url = url
            article_data = info
            break
            
    if not target_url:
        print("No pending articles found to retry.")
        return

    print(f"Retrying Facebook post for: {article_data['title']}")

    # 3. Reconstruct the Data (simulating what main.py does)
    publisher = FacebookPublisher()
    
    # Image Generation (Re-using the logic from main.py)
    # NEW APPROACH: Enhanced "Stop the Scroll" Prompt
    visual_style = "cinematic lighting, high contrast, 8k resolution, hyperrealistic, news graphic style"
    base_prompt = f"Editorial news graphic about {article_data['title']}, {visual_style}"
    
    # Sanitize just in case
    import re
    clean_prompt = re.sub(r'[^a-zA-Z0-9, ]', '', base_prompt)
    encoded_prompt = urllib.parse.quote(clean_prompt.strip())
    
    photo_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630&nologo=true"
    
    print(f"Generated Image URL: {photo_url}")
    
    # Caption Construction
    # We don't have the original caption saved in JSON, so we have to regenerate or fallback.
    # WAIT! The prompt update changed how the caption is generated. 
    # If I just regenerate it here, I won't know if the ORIGINAL generation worked.
    # However, since the original generation failed to post, we HAVE to regenerate it or use a fallback.
    # Actually, the 'main.py' generates the caption and TRIES to post. If it fails, the caption is lost unless saved.
    # We only save the title/url.
    # SO: We will run the Prompt again here to see if the NEW prompt logic works.
    
    import google.generativeai as genai
    from .settings import GOOGLE_API_KEY
    
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest')
    
    # Re-run the specific Facebook Prompt
    prompt = f"""
    You are a Direct Response Copywriter.
    Input Title: {article_data['title']}
    Input URL: https://aicorelogic-ops.github.io/ai-core-logic/{article_data['blog_path']}
    
    TASK: Write a Facebook Post using the NotebookLM "PPT + TAC" Formula.
    - Hook: [BRACKETS] in first 3 words.
    - Emotion: Awe or Anxiety.
    - Length: Under 100 words.
    
    Output ONLY the post text.
    """
    
    try:
        response = model.generate_content(prompt)
        caption = response.text.strip()
    except Exception as e:
        print(f"Error generating caption: {e}")
        caption = f"New Article: {article_data['title']}\n\nRead here: https://aicorelogic-ops.github.io/ai-core-logic/{article_data['blog_path']}"

    # Verify Output (Print safely for Windows)
    print(f"Caption: {caption.encode('ascii', 'ignore').decode('ascii')}")
    
    # Post
    try:
        photo_id = publisher.post_photo(photo_url=photo_url, message=caption)
        
        if photo_id:
            print(f"SUCCESS! Posted to Facebook. ID: {photo_id}")
            # Update the JSON so we don't retry again
            tracker.mark_as_processed(target_url, {'facebook_photo_id': photo_id})
            print("Updated processed_articles.json")
        else:
            print("FAILED. Publisher returned None.")
            
    except Exception as e:
        print(f"Exception during retry: {e}")

if __name__ == "__main__":
    retry_latest_post()
