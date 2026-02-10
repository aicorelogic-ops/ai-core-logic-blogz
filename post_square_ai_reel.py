"""
Post Square AI reel to Facebook
"""

from news_bot.publisher import FacebookPublisher

# Reel file path
reel_path = "blog/reels/Introducing_Square_AI:_Helping.mp4"

# Engaging caption for Facebook Reels
caption = """🚨 Your "gut feeling" is costing you £50,000 a year

Most business owners are gamblers. They just don't know it yet.

You wake up. Check your bank balance. And GUESS what to do next. 

That's not instinct. That's a slow-motion train wreck. 💣

Square just changed the game for UK small businesses with Square AI.

Businesses using AI assistants are moving 40% FASTER than those stuck in manual mode.

Within 12 months, if you aren't using AI to guide decisions, you'll be out-competed.

Stop guessing. Start knowing. ✅

Full breakdown in bio 👆

#AI #SmallBusiness #SquareAI #BusinessAutomation #UKBusiness #Entrepreneurship #DataDriven"""

# Post to Facebook
print("📤 Posting Square AI reel to Facebook...")
publisher = FacebookPublisher()
result = publisher.post_reel(reel_path, caption)

if result:
    print(f"\n✅ Reel posted successfully!")
    print(f"Facebook Post ID: {result}")
else:
    print("\n❌ Failed to post reel")
