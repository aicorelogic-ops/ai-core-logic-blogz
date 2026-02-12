
import os
import re
from datetime import datetime
from news_bot.blog_generator import BlogGenerator

POSTS_DIR = os.path.join("blog", "posts")

def parse_date(date_str):
    """Parses date string from various formats to YYYY-MM-DD"""
    try:
        # Try YYYY-MM-DD (Already correct)
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        pass
    
    try:
        # Try "February 10, 2026"
        dt = datetime.strptime(date_str, "%B %d, %Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return datetime.now().strftime("%Y-%m-%d") # Fallback

def migrate_posts():
    generator = BlogGenerator()
    
    if not os.path.exists(POSTS_DIR):
        print("No posts directory found.")
        return

    files = [f for f in os.listdir(POSTS_DIR) if f.endswith(".html")]
    print(f"Found {len(files)} posts to migrate...")

    for filename in files:
        filepath = os.path.join(POSTS_DIR, filename)
        
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # 1. Extract Title
        title_match = re.search(r'<title>(.*?) \|', content)
        if not title_match:
            print(f"Skipping {filename}: No title found")
            continue
        title = title_match.group(1).strip()

        # 2. Extract Date
        # Try new format first: <span>2026-02-11</span>
        date_match = re.search(r'<span>(\d{4}-\d{2}-\d{2})</span>', content)
        if not date_match:
            # Try old format: February 10, 2026 &bull;
            date_match = re.search(r'(\w+ \d{1,2}, \d{4}) (&bull;|•)', content)
        
        date_str = parse_date(date_match.group(1)) if date_match else datetime.now().strftime("%Y-%m-%d")

        # 3. Extract Image URL
        # Try new format (background url)
        img_match = re.search(r"\.article-hero \{.*?background: url\('(.*?)'\)", content, re.DOTALL)
        if not img_match:
            # Try old format (img src)
            img_match = re.search(r'<img src="(.*?)" alt="Hero Image"', content)
        
        image_url = img_match.group(1) if img_match else None

        # 4. Extract TLDR
        # Look for the list inside quick-summary
        tldr_match = re.search(r'<div class="quick-summary">.*?<ul>(.*?)</ul>', content, re.DOTALL)
        if tldr_match:
            tldr_summary = f"<ul>{tldr_match.group(1)}</ul>"
        else:
            # Try matching new format where it might just be the content of the div if not ul?
            # Or maybe just grab the inner text?
            # Let's try to match the placeholder area if it was filled
            tldr_match_2 = re.search(r'<div class="quick-summary">\s*<strong>.*?</strong>\s*(.*?)\s*</div>', content, re.DOTALL)
            tldr_summary = tldr_match_2.group(1).strip() if tldr_match_2 else None

        # 5. Extract Body Content
        # We want inner HTML of article-body.
        # Be careful to exclude the <h1> if distinct.
        body_match = re.search(r'<div class="article-body".*?>\s*(.*?)\s*(?:<hr|<div class="author-bio"|<div style="margin-top)', content, re.DOTALL)
        
        if body_match:
            body_content = body_match.group(1)
            # Remove the first <h1>...</h1> if it mirrors the title
            body_content = re.sub(r'^\s*<h1.*?>.*?</h1>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
        else:
            print(f"Skipping {filename}: No body content found")
            continue

        # 6. Regenerate
        safe_title_print = title.encode('ascii', 'ignore').decode('ascii')
        print(f"Migrating: {safe_title_print}")
        generator.create_post(
            title=title,
            content=body_content,
            link="#", # Not used in template
            image_url=image_url,
            tldr_summary=tldr_summary,
            date_str=date_str
        )

    print("Migration complete. updating index...")
    # Just run it once at the end
    import subprocess
    subprocess.run(["python", "generate_categories.py"], check=True)

if __name__ == "__main__":
    migrate_posts()
