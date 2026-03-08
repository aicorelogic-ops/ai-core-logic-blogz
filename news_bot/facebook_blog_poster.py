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
import re
from bs4 import BeautifulSoup
import requests
import time


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
    
    def _extract_blog_text(self, blog):
        """Extract clean text content from the blog HTML file (up to ~2000 chars).

        Why read the full content instead of just the 200-char summary:
        Gemini needs enough material to identify real business insights,
        actionable takeaways, and specific numbers/stats to quote.
        """
        try:
            with open(blog['filepath'], 'r', encoding='utf-8') as f:
                html = f.read()
            soup = BeautifulSoup(html, 'html.parser')

            # Get all paragraph text from the article body
            article_body = soup.find('div', class_='article-body')
            if article_body:
                paragraphs = [p.get_text().strip() for p in article_body.find_all('p')]
                full_text = "\n".join(paragraphs)
            else:
                # Fallback: grab all paragraph text
                full_text = "\n".join(p.get_text().strip() for p in soup.find_all('p'))

            # Cap at ~2000 chars to stay within prompt budget
            return full_text[:2000] if full_text else blog.get('summary', '')
        except Exception as e:
            print(f"   [Warn] Could not read full blog content: {e}")
            return blog.get('summary', '')

    def generate_facebook_post(self, blog):
        """
        Generate a B2B-focused Facebook post using Gemini.

        Strategy shift: Instead of 'viral emotion' clickbait, we now position
        ai.corelogic as a consultancy that translates AI news into business value.
        Hook → Value Translation → Bullet Points → CTA.
        """
        import google.generativeai as genai
        from .settings import GOOGLE_API_KEY

        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-flash-latest')

        # Read the full blog content for richer material
        blog_content = self._extract_blog_text(blog)

        prompt = f"""
Role: Expert B2B Social Media Copywriter for 'ai.corelogic', an agency dedicated to helping businesses seamlessly incorporate AI to drastically improve efficiency, streamline workflows, and drive better results.

Task: Write a highly engaging Facebook text post based on the following blog article. Do NOT just summarize it — sell the value of the information to a business owner.

Article Title: {blog['title']}
Article Content: {blog_content}

FOLLOW THIS EXACT STRUCTURE:

1. **The Hook** (1-2 sentences): Start with a scroll-stopping question or bold statement. Target a common business pain point (wasted time, high overhead, manual bottlenecks) that the article addresses. Do NOT start with a bracket tag like [ALERT]. You may start with a single relevant emoji.

2. **The Value Translation** (2-3 sentences): Explain in plain, accessible English how the AI concept discussed in the article solves that problem. Strip away heavy technical jargon; focus on the business outcome (ROI, speed, accuracy).

3. **Key Takeaways** (Bullet Points): Provide 2-3 quick bullet points extracting the most actionable insights from the post. Use simple emojis as bullets (e.g., ✅, 🚀, or ⚙️).

4. **Call to Action** (CTA): End by directing the reader to click the link in the comments to read the full guide, or to message us to see how this AI workflow can be implemented in their company. Use exactly: "Full breakdown in the comments 👇"

5. **Formatting Rules**:
   - Use generous double line breaks between each section so it reads well on mobile.
   - Keep paragraphs to 1-2 sentences maximum.
   - NO walls of text.

6. **Hashtags**: Include 3-4 highly relevant hashtags at the very bottom, separated from the CTA by a line break.

Output ONLY the Facebook post text. Do NOT include the blog URL in the post body.
"""

        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"   [Warn] AI text generation failed: {e}")
            # Fallback: clean, professional, still on-brand
            return (
                f"New on the blog: {blog['title']}\n\n"
                f"Read our latest breakdown on how AI can streamline "
                f"your business workflows.\n\n"
                f"Full breakdown in the comments 👇\n\n"
                f"#AICoreLogic #AI #BusinessEfficiency"
            )
    
    def verify_live_url(self, url, retries=30):
        """Checks if the URL returns 200 OK. Retries a few times."""
        for i in range(retries):
            try:
                r = requests.head(url, timeout=5)
                if r.status_code == 200:
                    print(f"   ✅ URL is Live (HTTP 200)")
                    return True
                else:
                    print(f"   ⚠️ Url check {i+1}/{retries}: Status {r.status_code}")
            except Exception as e:
                print(f"   ⚠️ Url check {i+1}/{retries} failed: {e}")
            time.sleep(2)
        return False

    def run(self):
        """Main execution flow."""
        print("🔍 Scanning blog posts...")
        all_blogs = self.scanner.get_all_blogs()
        print(f"   Found {len(all_blogs)} total blog posts")
        
        # User Constraint: Only look at the 20 newest posts to handle high volume days
        recent_blogs = all_blogs[:20]
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

        # NEW: Verify URL is actually live before posting (Ghost Post Prevention)
        print("   Verifying if blog post is live on the internet...")
        if not self.verify_live_url(blog['url']):
             print(f"❌ SKIPPING: URL returned 404. The blog post hasn't deployed to GitHub Pages yet.")
             print(f"   Action: Run `python news_bot/publish_git.py` (or similar) to deploy first.")
             return

        # Generate Facebook post content
        print("\n[Generate] Generating Facebook post...", flush=True)
        fb_post = self.generate_facebook_post(blog)
        print(f"   Preview: {fb_post[:100]}...")

        # Facebook Strategy: "Status Update with Photo attachment"
        # User requested: "Not a picture post, but a text post with a picture attached"
        # Logic: 
        # 1. Upload photo with published=False (to get ID)
        # 2. Post to FEED with attached_media pointing to that ID
        # 3. Post link in comments
        
        # Generate viral image with Vertex AI
        print("\n[Image] Generating image with Vertex AI Imagen...", flush=True)
        from .image_generator import ImageGenerator
        img_gen = ImageGenerator()
        # Use new facebook specific content-aware prompt generation
        viral_prompt = img_gen.create_facebook_image_prompt(blog['title'], summary=blog['summary'])
        local_image_path = img_gen.generate_image(viral_prompt, title=blog['title'])
        
        if not local_image_path:
            print("❌ Image generation failed. Aborting.")
            return
        
        print(f"✅ Image generated: {local_image_path}")

        # Step 2: Stamp crisp headline + branding with PIL (two-step approach).
        # AI image models garble text — PIL renders pixel-perfect typography.
        print("[Overlay] Applying programmatic text overlay...", flush=True)
        img_gen.add_facebook_overlay(local_image_path, blog['title'])
        
        # Post to Facebook
        print("\n[Post] Posting Photo to Facebook Timeline...", flush=True)
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
                print(f"[Warn] Failed to post link comment. You may need to add it manually.")
        else:
            print("[Error] Facebook posting failed")

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
