"""
Standalone Facebook Blog Poster

Selects existing blog posts and posts them to Facebook with Vertex AI generated images.
Tracks what's been posted to prevent duplicates.

Usage:
    python -m news_bot.facebook_blog_poster
"""

import os
import json
from datetime import datetime
from pathlib import Path
import re
from bs4 import BeautifulSoup


class BlogScanner:
    """Scans blog/posts/ directory and parses blog HTML files."""
    
    def __init__(self, blog_dir="blog/posts"):
        self.blog_dir = Path(blog_dir)
    
    def get_all_blogs(self):
        """Returns list of all blog posts with metadata."""
        blogs = []
        
        if not self.blog_dir.exists():
            print(f"❌ Blog directory not found: {self.blog_dir}")
            return blogs
        
        for html_file in self.blog_dir.glob("*.html"):
            try:
                blog_data = self._parse_blog(html_file)
                if blog_data:
                    blogs.append(blog_data)
            except Exception as e:
                print(f"⚠️ Failed to parse {html_file.name}: {e}")
        
        return sorted(blogs, key=lambda b: b['date'], reverse=True)
    
    def _parse_blog(self, html_file):
        """Parses a blog HTML file and extracts metadata."""
        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract title
        title_tag = soup.find('h1')
        title = title_tag.get_text().strip() if title_tag else html_file.stem
        
        # Extract date from filename (format: YYYY-MM-DD-title.html)
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', html_file.name)
        date_str = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")
        
        # Extract first paragraph as summary
        article_body = soup.find('div', class_='article-body')
        summary = ""
        if article_body:
            first_p = article_body.find('p')
            if first_p:
                summary = first_p.get_text().strip()[:200]
        
        # Construct blog URL
        blog_url = f"https://aicorelogic-ops.github.io/ai-core-logic-blogz/blog/posts/{html_file.name}"
        
        return {
            'filename': html_file.name,
            'filepath': str(html_file),
            'title': title,
            'date': date_str,
            'summary': summary,
            'url': blog_url
        }


class FacebookTracker:
    """Tracks which blogs have been posted to Facebook."""
    
    def __init__(self, tracking_file="news_bot/posted_to_facebook.json"):
        self.tracking_file = Path(tracking_file)
        self.data = self._load()
    
    def _load(self):
        """Load tracking data from JSON file."""
        if self.tracking_file.exists():
            with open(self.tracking_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save(self):
        """Save tracking data to JSON file."""
        self.tracking_file.parent.mkdir(exist_ok=True)
        with open(self.tracking_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def is_posted(self, blog_filename):
        """Check if blog has been posted to Facebook."""
        return blog_filename in self.data
    
    def mark_posted(self, blog_filename, photo_id, post_url):
        """Mark blog as posted to Facebook."""
        self.data[blog_filename] = {
            'posted_date': datetime.now().isoformat(),
            'facebook_photo_id': photo_id,
            'post_url': post_url
        }
        self._save()
    
    def get_unpublished_blogs(self, all_blogs):
        """Filter blogs that haven't been posted yet."""
        return [b for b in all_blogs if not self.is_posted(b['filename'])]


class FacebookBlogPoster:
    """Main orchestrator for posting blogs to Facebook."""
    
    def __init__(self):
        self.scanner = BlogScanner()
        self.tracker = FacebookTracker()
    
    def select_blog_to_post(self, unpublished_blogs):
        """Select which blog to post (newest unpublished)."""
        if not unpublished_blogs:
            return None
        
        # Return the newest unpublished blog
        return unpublished_blogs[0]
    
    def generate_facebook_post(self, blog):
        """Generate Facebook post content from blog data."""
        # Use Gemini to create engaging Facebook post
        import google.generativeai as genai
        from .settings import GOOGLE_API_KEY
        
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""
**Role:** You are a Viral Content Strategist and Behavioral Psychologist.

**Objective:** Write a high-engagement Facebook post about this blog article:
Title: {blog['title']}
Summary: {blog['summary']}
URL: {blog['url']}

**Constraints & Guidelines:**

1.  **Emotional Arousal:** The tone must evoke a High-Arousal emotion. Choose one of the following: **Awe** (shock/wonder), **Amusement** (humor), **Anger** (righteous indignation), or **Anxiety** (warning/urgency). Do NOT write a "sad" or "relaxing" post.

2.  **The Hook (Front-Loading):**
    *   **Emoji First:** Start the post with a SINGLE, high-impact emoji that matches the emotion. Do NOT use the same emoji every time. Vary it based on context (e.g., 🚨, 🤯, 📉, ⚠️, 🚀, 💡, 🛑).
    *   **No Brackets:** Do NOT use text tags like [ALERT] or [UPDATE].
    *   **Inverted Pyramid:** The text immediately following the emoji must contain the most shocking or valuable information in the first 5 words.

3.  **Layout & Scannability (F-Pattern):**
    *   **No Walls of Text:** Paragraphs must be 1-2 sentences maximum.
    *   **Active Whitespace:** Leave double spacing between thoughts to create a "luxurious" and readable feel.
    *   **Lists:** Use a bulleted list (using emojis like 👉 or ✅ as bullets) for the core value points. This caters to "layer-cake" scanning behavior.

4.  **The Ending (TAC Formula):**
    *   **Transition:** Use a short sentence signaling the wrap-up (e.g., "Here is the bottom line.").
    *   **Ask:** Ask a specific, closed-ended question to drive comments (e.g., "Do you prefer A or B?" rather than "Thoughts?").
    *   **Call to Action:** End with exactly: "Link in comments 👇" (Do NOT include the actual URL in the text).

5.  **Hashtags:** Use 3-5 keywords relevant to the niche for categorization, placed at the very bottom so they do not clutter the visual hierarchy.

**Output Format:**
Output ONLY the Facebook post text. Do NOT include the URL.
"""
        
        try:
            response = model.generate_content(prompt)
            return response.text.strip() + "\n\n#AICoreLogic"
        except Exception as e:
            print(f"⚠️ AI generation failed: {e}")
            # Fallback post
            return f"🚀 New Analysis: {blog['title']}\n\n#AICoreLogic\n\nRead more: {blog['url']}"
    
    def run(self):
        """Main execution flow."""
        print("🔍 Scanning blog posts...")
        all_blogs = self.scanner.get_all_blogs()
        print(f"   Found {len(all_blogs)} total blog posts")
        
        # User Constraint: Only look at the 4 newest posts
        recent_blogs = all_blogs[:4]
        print(f"   Refining scope to top {len(recent_blogs)} newest posts")
        
        unpublished = self.tracker.get_unpublished_blogs(recent_blogs)
        print(f"   {len(unpublished)} unpublished in recent window")
        
        if not unpublished:
            print("✅ All blogs have been posted to Facebook!")
            return
        
        blog = self.select_blog_to_post(unpublished)
        print(f"\n📝 Selected: {blog['title']}")
        print(f"   Date: {blog['date']}")
        print(f"   URL: {blog['url']}")
        
        # Generate Facebook post content
        print("\n✍️ Generating Facebook post...")
        fb_post = self.generate_facebook_post(blog)
        print(f"   Preview: {fb_post[:100]}...")
        
        # Facebook Strategy: "Status Update with Photo attachment"
        # User requested: "Not a picture post, but a text post with a picture attached"
        # Logic: 
        # 1. Upload photo with published=False (to get ID)
        # 2. Post to FEED with attached_media pointing to that ID
        # 3. Post link in comments
        
        # Generate viral image with Vertex AI
        print("\n🎨 Generating image with Vertex AI Imagen...")
        from .image_generator import ImageGenerator
        img_gen = ImageGenerator()
        viral_prompt = img_gen.create_viral_prompt(blog['title'])
        local_image_path = img_gen.generate_image(viral_prompt, title=blog['title'])
        
        if not local_image_path:
            print("❌ Image generation failed. Aborting.")
            return
        
        print(f"✅ Image generated: {local_image_path}")
        
        # Post to Facebook
        print("\n📤 Posting Photo to Facebook Timeline...")
        from .publisher import FacebookPublisher
        publisher = FacebookPublisher()
        
        # Direct Photo Posting (The Photo IS the Post)
        # This ensures it appears on the Timeline/Feed as a large Photo Post
        # and avoids the "hidden" status of attached_media
        print(f"   Posting to Feed with caption...")
        post_id = publisher.post_photo(photo_source=local_image_path, message=fb_post, published=True)
        
        if post_id:
            print(f"✅ Posted Photo to Timeline! ID: {post_id}")
            self.tracker.mark_posted(blog['filename'], post_id, blog['url'])
            
            # Post link in comments
            print(f"💬 Posting link in comments...")
            import time
            time.sleep(5) # Wait a bit longer for the photo to fully propagate
            comment_id = publisher.post_comment(post_id, f"Read the full article here: {blog['url']}")
            
            if comment_id:
                print(f"✅ Link posted in comments! ID: {comment_id}")
            else:
                print(f"⚠️ Failed to post link comment. You may need to add it manually.")
        else:
            print("❌ Facebook posting failed")

        print("\n" + "="*60)
        print("🛡️ SAFE POSTING VERIFICATION REQUIRED")
        from .settings import FB_PAGE_ID
        print("To comply with 'facebook-posting-safety.md', you MUST now:")
        print(f"1. VISUALLY VERIFY the post on the Page Feed: https://www.facebook.com/{FB_PAGE_ID}")
        print("2. Ensure it appears on the MAIN 'Home' tab, not just 'Photos'.")
        print("3. Take a screenshot of the feed as the Completion Artifact.")
        print("="*60 + "\n")


def main():
    """CLI entry point."""
    poster = FacebookBlogPoster()
    poster.run()


if __name__ == "__main__":
    main()
