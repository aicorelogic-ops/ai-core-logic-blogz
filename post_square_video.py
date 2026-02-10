"""
Post Square AI reel as regular video to Facebook
(Fallback: Reels API not working, using regular video endpoint)
"""

from news_bot.publisher import FacebookPublisher

# Reel file path
reel_path = "blog/reels/Introducing_Square_AI:_Helping.mp4"

# Engaging caption
caption = """🚨 Your "gut feeling" is costing you £50,000 a year

Most business owners are gamblers. They just don't know it yet.

You wake up. Check your bank balance. And GUESS what to do next. 

That's not instinct. That's a slow-motion train wreck. 💣

Square just changed the game for UK small businesses with Square AI.

Businesses using AI assistants are moving 40% FASTER than those stuck in manual mode.

Within 12 months, if you aren't using AI to guide decisions, you'll be out-competed.

Stop guessing. Start knowing. ✅

Full breakdown at aicorelogic-ops.github.io/ai-core-logic 👆

#AI #SmallBusiness #SquareAI #BusinessAutomation #UKBusiness #Entrepreneurship #DataDriven"""

# Post as regular video (Reels API not available)
print("📤 Posting as video to Facebook...")
publisher = FacebookPublisher()
result = publisher.post_video(reel_path, caption)

if result:
    print(f"\n✅ Video posted successfully!")
    print(f"Facebook Post ID: {result}")
else:
    print("\n❌ Failed to post video")
