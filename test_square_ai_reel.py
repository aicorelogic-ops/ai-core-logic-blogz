"""
Test script for Square AI article reel
"""

from news_bot.reel_generator import ReelGenerator

# Square AI article data
test_article = {
    'title': 'Introducing Square AI: Helping UK Small Businesses Turn Instinct Into Confident Decisions',
    'summary': 'Square AI gives small businesses the analytical power of Fortune 500 companies for free.',
}

test_blog_html = """
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

# Generate the reel
print("🎬 Starting Square AI reel generation...")
generator = ReelGenerator()

reel_path = generator.create_reel(
    article=test_article,
    blog_html=test_blog_html,
    image_url="https://s.yimg.com/os/en/business-wire.com/4bfd8c8441798502255682e8261f77e6"
)

if reel_path:
    print(f"\n✅ SUCCESS! Reel created at: {reel_path}")
    print("\n📋 This reel is for the Square AI article!")
else:
    print("\n❌ Reel generation failed.")
