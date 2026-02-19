
import os
import sys
from news_bot.image_generator import ImageGenerator

def test_generation():
    print("🚀 Starting reproduction test...")
    
    title = "Rapidata emerges to shorten AI model development cycles from months to days with near real-time RLHF"
    summary = "Rapidata uses twenty million mobile app users to slash AI training cycles from months to near real-time. You can now process over one million human annotations every single hour. Stop using slow offshore contractors and switch to gamified human feedback."
    
    gen = ImageGenerator()
    
    # 1. Test Prompt Generation
    print("\n--------------------------------")
    print("1. Testing create_content_aware_prompt...")
    try:
        prompt = gen.create_content_aware_prompt(title, summary)
        print(f"✅ Generated Prompt:\n{prompt}")
    except Exception as e:
        print(f"❌ Prompt Generation Failed: {e}")
        return

    # 2. Test Image Generation
    print("\n--------------------------------")
    print("2. Testing generate_image with the generated prompt...")
    try:
        image_path = gen.generate_image(prompt, title=title)
        if image_path:
            print(f"✅ Image generated successfully: {image_path}")
        else:
            print("❌ Image generation returned None (failed)")
    except Exception as e:
        print(f"❌ Image Generation Threw Exception: {e}")

if __name__ == "__main__":
    test_generation()
