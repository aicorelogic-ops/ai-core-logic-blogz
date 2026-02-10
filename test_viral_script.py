"""
Test the viral script generator with Square AI article
"""

from news_bot.reel_script_generator import ReelScriptGenerator

# Square AI article
article_title = "Introducing Square AI: Helping UK Small Businesses Turn Instinct Into Confident Decisions"

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

# Generate script
print("🎬 Generating viral reel script...\n")
generator = ReelScriptGenerator()
script = generator.generate_viral_script(article_title, blog_html)

if script:
    print("\n" + "="*60)
    print(generator.format_script_for_display(script))
    print("="*60)
    
    # Save for inspection
    import json
    with open("viral_script_output.json", "w") as f:
        json.dump(script, f, indent=2)
    print("\n✅ Script saved to viral_script_output.json")
else:
    print("\n❌ Script generation failed")
