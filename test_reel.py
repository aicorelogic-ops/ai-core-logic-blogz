"""
Test script for manual reel generation
Run this to create a sample reel without posting to Facebook
"""

from news_bot.reel_generator import ReelGenerator
from news_bot.publisher import FacebookPublisher

# Sample article data
test_article = {
    'title': 'Your Payroll Is A Ticking Time Bomb - AI Automation Could Save You $50k',
    'summary': 'Small businesses are losing thousands to manual payroll processes while competitors automate.',
}

test_blog_html = """
<h3>Your competitors are weaponizing their data while you're still wrestling with spreadsheets.</h3>
<p>Right now, your dispatcher is likely leaking cash faster than a punctured fuel tank.</p>
<p>You're bleeding cash. Every month. Every week. Every hour.</p>
<p>Most owners think they need better people. They're wrong. You have a logic problem.</p>
"""

# Generate the reel
print("🎬 Starting reel generation test...")
generator = ReelGenerator()

reel_path = generator.create_reel(
    article=test_article,
    blog_html=test_blog_html,
    image_url="https://example.com/image.jpg"  # Not used yet
)

if reel_path:
    print(f"\n✅ SUCCESS! Reel created at: {reel_path}")
    print("\n📋 Next Steps:")
    print("1. Open the video file to review it")
    print("2. If it looks good, uncomment the Facebook upload code below")
    print("3. Run this script again to upload to Facebook")
    
    # UNCOMMENT THESE LINES TO TEST FACEBOOK UPLOAD:
    # publisher = FacebookPublisher()
    # caption = "🚨 Your payroll is bleeding cash. Here's what we discovered... Full story in bio! 👆 #AI #Automation #SmallBusiness"
    # publisher.post_reel(reel_path, caption)
else:
    print("\n❌ Reel generation failed. Check the errors above.")
