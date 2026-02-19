import time
from datetime import datetime
from .collector import NewsCollector
from .processor import NewsProcessor
# from .publisher import FacebookPublisher  # Removed - Facebook posting now in facebook_blog_poster.py
from .blog_generator import BlogGenerator
from .article_tracker import ArticleTracker
# from .viral_reel_generator import ViralReelGenerator  # Removed per user request
from .image_design_helper import analyze_article_visual_context, create_news_overlay_prompt

def run_bot():
    print("Starting AI Core Logic News Bot...")

    # Initialize tracker
    tracker = ArticleTracker()
    
    # 1. Collect
    collector = NewsCollector()
    # Fetch only the first 10 posts from each RSS feed to analyze for viral potential
    articles = collector.fetch_news(hours_back=168, max_posts_per_feed=10)
    print(f"Found {len(articles)} potential articles.")

    if not articles:
        print("No new articles found. Sleeping.")
        return

    # 2. Score Articles for Viral Potential (Select BEST, not newest)
    print("Scoring articles for viral potential...")
    
    def score_viral_potential(article):
        # (existing scoring logic unchanged)
        try:
            import google.generativeai as genai
            from .settings import GOOGLE_API_KEY
            
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel('gemini-flash-latest')
            
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
            print(f"Scoring error: {e}")
            return 50  # Default middle score if error
    
    # Score all articles
    articles_with_scores = []
    for article in articles:
        # Check if already processed
        if tracker.is_processed(article['link']):
            print(f"  Skipping score for processed article: {article['title'][:60].encode('ascii', 'ignore').decode('ascii')}...")
            continue
            
        score = score_viral_potential(article)
        articles_with_scores.append((article, score))
        print(f"  '{article['title'][:60].encode('ascii', 'ignore').decode('ascii')}...' -> Score: {score}")
    
    if not articles_with_scores:
        print("All found articles have already been processed. Nothing to do.")
        return

    # Select the HIGHEST scoring article
    best_article, best_score = max(articles_with_scores, key=lambda x: x[1])
    print(f"\nSelected BEST article (Score: {best_score}): {best_article['title'].encode('ascii', 'ignore').decode('ascii')}\n")
    
    # 3. Process & Generate Blog for the BEST article
    processor = NewsProcessor()
    blog_gen = BlogGenerator()
    # viral_gen = ViralReelGenerator()  # Removed per user request

    # Process only the BEST article (highest viral score)
    # UPDATED: Loop through top 3 articles in case the best one is a duplicate
    articles_with_scores.sort(key=lambda x: x[1], reverse=True)
    
    selected_article = None
    
    for article, score in articles_with_scores[:3]:
        print(f"Checking candidate: {article['title'].encode('ascii', 'ignore').decode('ascii')} (Score: {score})")
        
        # Check against existing filesystem (Title Similarity)
        is_dup, existing_file = blog_gen.is_duplicate_title(article['title'])
        if is_dup:
             print(f"  SKIP: Similar article already exists: {existing_file}")
             # Mark as processed so we don't check it again next time
             tracker.mark_as_processed(article['link'], {'title': article['title'], 'status': 'duplicate_skipped'})
             continue
             
        selected_article = article
        break
    
    if not selected_article:
        print("All top candidates were duplicates or processed. Sleeping.")
        return

    for article in [selected_article]:  # Process only the winner
        print(f"Processing: {article['title'].encode('ascii', 'ignore').decode('ascii')}")
        
        # Generates DICT: {'blog_html': ..., 'facebook_msg': ...}
        content_package = processor.summarize(article)
        
        if content_package:
            # A. Create Blog Post HTML
            fname, generated_image_url = blog_gen.create_post(
                article['title'], 
                content_package['blog_html'], 
                article['link'],
                # image_url=article.get('image_url'),
                image_url=None, # FORCE GENERATION: User selected "Always Generate AI Images"
                # image_url=article.get('image_url'),
                tldr_summary=content_package.get('tldr_summary'),
                editorial_prospect=content_package.get('editorial_prospect'),
                summary=article.get('summary', '')  # Pass summary for content-aware image gen
            )
            
            # B. Update Index
            # If create_post generated a new image, use it. Otherwise fall back to what we had.
            final_image_url = generated_image_url if generated_image_url else article.get('image_url')
            
            blog_gen.update_index(
                article['title'],
                content_package['tldr_summary'],
                fname,
                image_url=final_image_url
            )
            
            # C. Deploy to GitHub
            is_deployed = blog_gen.deploy_to_github()
            
            if not is_deployed:
                print("GitHub deploy reported failure (might just be 'no changes'), proceeding anyway...")
            
            # Generate blog URL for tracking
            blog_url = f"https://aicorelogic-ops.github.io/ai-core-logic-blogz/blog/posts/{fname}"
            
            print(f"✅ Blog post created and deployed: {fname}")
            print(f"   URL: {blog_url}")
            print(f"📢 To post to Facebook, run: python -m news_bot.facebook_blog_poster")
            
            # D. Track as processed (blog created)
            tracker.mark_as_processed(article['link'], {
                'title': article['title'],
                'blog_path': f"blog/posts/{fname}",
                'blog_url': blog_url,
                'processed_date': datetime.now().isoformat()
            })
            
            # Sleep to avoid spamming
            time.sleep(10)
        else:
            print("Failed to process article.")

if __name__ == "__main__":
    run_bot()
