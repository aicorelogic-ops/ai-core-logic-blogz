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

    # 2. Score Articles for Viral Potential (Select BEST, not newest)
    print("🎯 Scoring articles for viral potential...")
    
    def score_viral_potential(article):
        """Score article 0-100 based on engagement potential"""
        try:
            import google.generativeai as genai
            from .settings import GOOGLE_API_KEY
            
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            prompt = f"""Score this article for VIRAL POTENTIAL in the logistics/business automation niche (0-100).

Title: {article['title']}
Summary: {article.get('summary', '')[:300]}

Scoring Factors:
1. SPECIFICITY: Does it have specific numbers/data? ($40k, 30% increase, etc.)
2. CONTROVERSY: Is it provocative or against conventional wisdom?
3. URGENCY: Does it create time pressure or FOMO?
4. EMOTIONAL HOOK: Does it trigger fear, curiosity, or anger?
5. RELEVANCE: Will logistics/small business owners care?
6. CLICKBAIT FACTOR: Does the title create a curiosity gap?

Return ONLY a number 0-100. No explanation."""

            response = model.generate_content(prompt)
            score = int(response.text.strip())
            return max(0, min(100, score))  # Clamp between 0-100
        except Exception as e:
            print(f"⚠️ Scoring error: {e}")
            return 50  # Default middle score if error
    
    # Score all articles
    articles_with_scores = []
    for article in articles:
        score = score_viral_potential(article)
        articles_with_scores.append((article, score))
        print(f"  📊 '{article['title'][:60]}...' → Score: {score}")
    
    # Select the HIGHEST scoring article
    best_article, best_score = max(articles_with_scores, key=lambda x: x[1])
    print(f"\n🏆 Selected BEST article (Score: {best_score}): {best_article['title']}\n")
    
    # 3. Process & Publish the BEST article
    processor = NewsProcessor()
    publisher = FacebookPublisher()
    blog_gen = BlogGenerator()

    # Process only the BEST article (highest viral score)
    for article in [best_article]:  # Process only the winner

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
