"""
Test viral reel generator with AI scripts
"""

from news_bot.viral_reel_generator import ViralReelGenerator

# Square AI article
article = {
    'title': 'Introducing Square AI: Helping UK Small Businesses'
}

blog_html = """
<h3>Your "Gut Feeling" Is Costing You £50,000 A Year</h3>
<p>Most business owners are gamblers. They just don't know it yet.</p>
<p>You wake up. You check your bank balance. And you <b>guess</b> what to do next.</p>
<p>In the UK, small businesses are bleeding cash through <b>analysis paralysis</b>.</p>

<h3>The Silent Profit Killer</h3>
<p>Every hour you spend squinting at spreadsheets is an hour you aren't growing.</p>
<p>This isn't just "part of the job." It's a <b>systemic failure</b>.</p>

<h3>What We Discovered</h3>
<p>Square just changed the game. They launched Square AI.</p>
<p>Businesses using AI assistants are moving <b>40% faster</b> than those stuck in manual mode.</p>

<h3>The Prediction: Adapt or Evaporate</h3>
<p>Within 12 months, if you aren't using AI, you will be out-competed.</p>
<p><b>Stop guessing. Start knowing.</b></p>
"""

image_url = "https://s.yimg.com/os/en/business-wire.com/4bfd8c8441798502255682e8261f77e6"

# Generate viral reel
print("🎬 Generating VIRAL reel with AI scripts...\n")
generator = ViralReelGenerator()
reel_path = generator.create_viral_reel(article, blog_html, image_url)

if reel_path:
    print(f"\n✅ SUCCESS! Viral reel created!")
    print(f"Path: {reel_path}")
    print("\nThis reel uses:")
    print("- AI-generated script (Hyper-Dopamine framework)")
    print("- Pattern interrupt hook ('STOP SCROLLING')")
    print("- Specific numbers (£50K, 40%)")
    print("- Urgent text overlays (ALL CAPS)")
    print("- Sell-the-click CTA")
else:
    print("\n❌ Viral reel generation failed")
