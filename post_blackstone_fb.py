"""
Post the latest Blackstone blog post to Facebook using Google Gemini Imagen 3
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from news_bot.publisher import FacebookPublisher
from news_bot.image_generator import ImageGenerator

# Initialize components
publisher = FacebookPublisher()
img_gen = ImageGenerator()

# Blog post URL 
blog_url = "https://aicorelogic-ops.github.io/ai-core-logic-blogz/blog/posts/2026-02-15-blackstone-to-lead--600-million-investment-in-ai-f.html"

# Facebook post caption with viral copy
fb_caption = """💰 $600,000,000.00 

That's the massive stack of cash Blackstone just threw down to DOMINATE the AI infrastructure game.

While most business owners are waiting for AI to "settle down," the world's biggest fund is buying up the digital land and power that every chatbot lives on.

🔥 The brutal reality? 
→ Institutional investors are moving at predatory speed
→ Infrastructure is where the 10x returns are hiding  
→ India's explosive AI market is being claimed RIGHT NOW

Are you going to be a tenant in someone else's digital empire, or will you secure your position?

The gatekeepers are already at the door. 

📊 Read the full analysis → {blog_url}

#AIInfrastructure #Blackstone #AIInvestment #BusinessStrategy #AIRevolution #SmallBusiness #Automation #TechNews
""".replace("{blog_url}", blog_url)

# Generate viral image using Imagen 3
article_title = "Blackstone to Lead $600 Million Investment in AI Firm Neysa"
visual_style = "cinematic lighting, high contrast, 8k resolution, hyperrealistic, news graphic style, modern tech aesthetic"
prompt = f"Editorial news graphic about {article_title}, {visual_style}"

print(f"🎨 Generating viral image with Imagen 3...")
print(f"   Prompt: {prompt[:100]}...")

# Generate and save locally
image_path = img_gen.generate_viral_image(prompt)

if image_path:
    print(f"✅ Image generated: {image_path}")
    
    print(f"📱 Posting to Facebook...")
    print(f"Caption: {fb_caption[:100]}...")
    
    # Post to Facebook using local file
    post_id = publisher.post_photo(photo_source=image_path, message=fb_caption)

    if post_id:
        print(f"✅ Success! Post ID: {post_id}")
        print(f"🔗 View on Facebook: https://www.facebook.com/{post_id}")
    else:
        print(f"❌ Failed to post to Facebook")
else:
    print(f"❌ Failed to generate image with Imagen")
