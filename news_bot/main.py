import time
from .collector import NewsCollector
from .processor import NewsProcessor
from .publisher import FacebookPublisher
from .blog_generator import BlogGenerator

def run_bot():
    print("🤖 Starting AI Core Logic News Bot...")

    # 1. Collect
    collector = NewsCollector()
    # Using 72 hours window for testing to ensure we find something
    articles = collector.fetch_news(hours_back=72)
    print(f"📥 Found {len(articles)} potential articles.")

    if not articles:
        print("😴 No new articles found. Sleeping.")
        return

    # 2. Process & Publish
    processor = NewsProcessor()
    publisher = FacebookPublisher()
    blog_gen = BlogGenerator()

    # Process only the FIRST article (limit to 1 post per run)
    for article in articles[:1]:  # [:1] takes only the first article

        print(f"📝 Processing: {article['title']}")
        
        # Generates DICT: {'blog_html': ..., 'facebook_msg': ...}
        content_package = processor.summarize(article)
        
        if content_package:
            # A. Create Blog Post
            filename = blog_gen.create_post(
                article['title'], 
                content_package['blog_html'], 
                article['link'],
                image_url=article.get('image_url')
            )
            
            # B. Update Index
            blog_gen.update_index(
                article['title'], 
                "New AI Analysis available.", # Simple snippet
                filename,
                image_url=article.get('image_url')
            )
            
            # C. Prepare Facebook Link
            # Production URL structure for GitHub Pages
            blog_url = f"https://aicorelogic-ops.github.io/ai-core-logic/blog/posts/{filename}" 
            
            fb_message = content_package['facebook_msg'].replace("[LINK]", blog_url)
            
            # D. Deploy to GitHub
            is_deployed = blog_gen.deploy_to_github()
            
            if not is_deployed:
                print("⚠️ GitHub deploy reported failure (might just be 'no changes'), proceeding anyway...")

            # E. Post to Facebook as PHOTO POST (Higher Engagement)
            # Hyper-dopamine strategy: Photo posts stop the scroll, link is in caption
            print(f"🚀 Publishing to Facebook as photo post...")
            
            # VIRAL IMAGE GENERATION - Pattern Interrupt Strategy for Facebook
            import urllib.parse
            import random
            
            # Extract the "Bleeding Neck" problem from title
            image_hook = article['title'][:60] if len(article['title']) <= 60 else article['title'].split(':')[0][:60]
            
            # Apply Direct Response Marketer Framework
            
            # Option A: "Raw Native" / Leaked Evidence
            raw_native = (
                f"iPhone photo amateur candid shot, first-person POV, "
                f"computer screen showing shocking data about '{image_hook}', "
                f"messy desk, RED CIRCLE hand-drawn around key detail, "
                f"harsh office lighting, grainy quality, user-generated content, "
                f"flash photography, NOT professional, leaked evidence style"
            )
            
            # Option B: "Breaking News" 
            breaking_news = (
                f"Breaking news screenshot style, person looking SHOCKED, "
                f"holding document about '{image_hook}', "
                f"'BREAKING NEWS' or 'EXPOSED' banner, TMZ viral news style, "
                f"candid amateur photo, harsh flash lighting, grainy iPhone quality"
            )
            
            # Option C: "Weird" Visual
            weird_visual = (
                f"Close-up macro photo of weird detail about '{image_hook}', "
                f"magnified mistake, confusing composition, "
                f"makes viewer ask 'what the hell is that?', "
                f"amateur grainy texture, harsh lighting, pattern interrupt"
            )
            
            chosen_style = random.choice([raw_native, breaking_news, weird_visual])
            safe_prompt = urllib.parse.quote(chosen_style)
            photo_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1200&height=630&nologo=true"
            
            publisher.post_photo(photo_url=photo_url, message=fb_message)
            
            # Sleep to avoid spamming
            time.sleep(10)
        else:
            print("❌ Failed to process article.")

if __name__ == "__main__":
    run_bot()
