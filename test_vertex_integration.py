"""Test the complete Vertex AI Imagen integration with viral prompts"""
import sys
sys.path.insert(0, '.')

from news_bot.image_generator import ImageGenerator

# Initialize generator
gen = ImageGenerator()

# Create viral prompt
title = 'Google Reveals Shocking AI Breakthrough That Changes Everything'
prompt = gen.create_viral_prompt(title)

print(f'\n📝 Generated viral prompt:')
print(f'   {prompt[:200]}...')
print()

# Generate image with Vertex AI
try:
    print(f'🎨 Testing Vertex AI Imagen 3.0...\n')
    path = gen.generate_viral_image(prompt, use_vertex=True)
    
    if path:
        print(f'\n✅✅✅ SUCCESS! ✅✅✅')
        print(f'   Image saved to: {path}')
        
        import os
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f'   File size: {size:,} bytes ({size / 1024:.1f} KB)')
            print(f'\n🎉 Vertex AI Imagen is working perfectly!')
    else:
        print(f'\n❌ FAILED - returned None')
        
except Exception as e:
    print(f'\n❌ FAILED with error:')
    print(f'   {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()
