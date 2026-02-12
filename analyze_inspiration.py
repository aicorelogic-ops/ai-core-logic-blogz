
import os
import google.generativeai as genai
from news_bot.settings import GOOGLE_API_KEY
import time

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
# Use a model that supports vision
model = genai.GenerativeModel('models/gemini-2.0-flash') 

INSPIRATION_DIR = r"c:\Users\OlgaKorniichuk\Documents\antiGravity Projects\Facebok AI.corelogic\facebook post insperation pictures"

def analyze_images():
    print(f"📂 Scanning folder: {INSPIRATION_DIR}")
    
    if not os.path.exists(INSPIRATION_DIR):
        print(f"❌ Error: Directory not found: {INSPIRATION_DIR}")
        return

    image_files = [f for f in os.listdir(INSPIRATION_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    if not image_files:
        print("❌ No image files found in the directory.")
        return

    print(f"📸 Found {len(image_files)} images. Analyzing the FIRST one only to avoid API limits...")
    
    # Analyze ONLY 1 image first to test
    images_to_analyze = image_files[:1]
    uploaded_files = []
    
    try:
        for img_file in images_to_analyze:
            path = os.path.join(INSPIRATION_DIR, img_file)
            print(f"   - Uploading {img_file}...")
            # Upload to Gemini File API
            myfile = genai.upload_file(path)
            uploaded_files.append(myfile)
            
        print("🧠 Asking Gemini to reverse-engineer the style...")
        
        prompt = """
        You are an Expert Visual Prompt Engineer.
        
        Analyze this image and describe its visual style so I can recreate it with AI.
        Focus on:
        1. Lighting
        2. Color Palette
        3. Composition
        4. Mood
        5. Specific Elements (e.g., grain, blur, minimalism)
        
        OUTPUT FORMAT:
        Comma-separated keywords defining the style.
        """
        
        response = model.generate_content([prompt, *uploaded_files])
        
        print("\n✨ ANALYSIS COMPLETE. HERE IS THE EXTRACTED STYLE PROMPT:\n")
        print(response.text)
        
        # Save to file
        with open("style_analysis.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
            
    except Exception as e:
        error_msg = f"❌ Error during analysis: {e}"
        print(error_msg)
        with open("analysis_error.log", "w") as f:
            f.write(str(e))
            import traceback
            traceback.print_exc(file=f)

if __name__ == "__main__":
    analyze_images()
