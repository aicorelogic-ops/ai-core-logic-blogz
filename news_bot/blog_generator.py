import os
from datetime import datetime

BLOG_DIR = "blog"
POSTS_DIR = os.path.join(BLOG_DIR, "posts")

# Ensure posts directory exists
os.makedirs(POSTS_DIR, exist_ok=True)

class BlogGenerator:
    def create_post(self, title, content_html, original_link):
        """
        Creates a new HTML file for the blog post and returns its relative path.
        """
        # Create a safe filename
        safe_title = "".join([c if c.isalnum() else "-" for c in title]).lower()
        filename = f"{datetime.now().strftime('%Y-%m-%d')}-{safe_title[:30]}.html"
        filepath = os.path.join(POSTS_DIR, filename)
        
        # HTML Template for individual post
        post_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | AI Core Logic</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
<header>
    <div class="nav-container" style="display:flex; justify-content:center; padding: 1rem;">
        <a href="../index.html">
            <img src="../assets/logo.png" alt="AI.Core Logic" style="height: 50px; border-radius: 6px;">
        </a>
    </div>
</header>

<main>
    <article class="article-card">
        <div class="article-date">{datetime.now().strftime('%B %d, %Y')}</div>
        <h1>{title}</h1>
        <div class="article-body">
            {content_html}
        </div>
        <hr style="border-color: #233554; margin: 2rem 0;">
        <p><em>Source: <a href="{original_link}" target="_blank" style="color: var(--brand-blue);">Read original article</a></em></p>
        <br>
        <a href="../index.html" class="read-more">← Back to Home</a>
    </article>
</main>

<footer>
    <p>&copy; 2026 AI Core Logic.</p>
</footer>
</body>
</html>
        """
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(post_html)
            
        print(f"✅ Blog post created: {filepath}")
        return filename

    def update_index(self, title, summary, filename):
        """
        Injects the new post into the top of index.html
        """
        index_path = os.path.join(BLOG_DIR, "index.html")
        
        # Bento Grid Logic: Randomly assign a size class
        import random
        # 15% chance of being a huge feature, 25% chance of being wide, 60% standard
        rand_val = random.random()
        if rand_val < 0.15:
            card_class = "article-card featured"
        elif rand_val < 0.40:
            card_class = "article-card wide"
        else:
            card_class = "article-card"

        # New entry HTML with dynamic class
        new_entry = f"""
    <article class="{card_class}">
        <div class="article-date">{datetime.now().strftime('%B %d')}</div>
        <h2><a href="posts/{filename}">{title}</a></h2>
        <p class="article-snippet">{summary}...</p>
        <a href="posts/{filename}" class="read-more">Read Analysis →</a>
    </article>
        """
        
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find the injection point (after <main id="news-feed">)
            marker = '<main id="news-feed">'
            if marker in content:
                updated_content = content.replace(marker, marker + "\n" + new_entry)
                
                with open(index_path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                print("✅ Index.html updated.")
            else:
                print("❌ Could not find injection marker in index.html")
                
        except Exception as e:
            print(f"❌ Error updating index: {e}")

    def deploy_to_github(self):
        """
        Commits and pushes the new changes to GitHub so the link becomes live.
        """
        import subprocess
        
        print("☁️ Auto-Deploying to GitHub...")
        try:
            # 1. Add changes
            subprocess.run(["C:\\Program Files\\Git\\cmd\\git.exe", "add", "."], check=True)
            
            # 2. Commit
            try:
                subprocess.run(["C:\\Program Files\\Git\\cmd\\git.exe", "commit", "-m", "Auto-publish new article"], check=True)
            except subprocess.CalledProcessError:
                print("⚠️ Nothing to commit (files already exist). Proceeding to push...")
            
            # 3. Push
            # Note: This relies on your cached credentials.
            subprocess.run(["C:\\Program Files\\Git\\cmd\\git.exe", "push"], check=True)
            
            print("✅ Successfully deployed to https://aicorelogic-ops.github.io/ai-core-logic/")
            return True
        except Exception as e:
            print(f"❌ Deploy failed: {e}")
            return False

if __name__ == "__main__":
    # Test
    gen = BlogGenerator()
    fname = gen.create_post("Test Article", "<p>This is a test.</p>", "http://google.com")
    gen.update_index("Test Article", "This is a short summary.", fname)
    # gen.deploy_to_github() # Uncomment to test deploy
