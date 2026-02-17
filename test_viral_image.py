"""
Test the fixed Pollinations implementation with viral prompts
"""
import sys
sys.path.insert(0, '.')

from news_bot.image_generator import ImageGenerator

# Initialize generator
gen = ImageGenerator()

# Create viral prompt
title = 'AI Takes Over Software Industry in Historic Shift'
prompt = gen.create_viral_prompt(title)

print(f'\n📝 Generated viral prompt:')
print(f'   {prompt[:150]}...')
print()

# Generate image
try:
    path = gen.generate_viral_image(prompt)
    
    if path:
        print(f'\n✅ SUCCESS!')
        print(f'   Image saved to: {path}')
        
        import os
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f'   File size: {size:,} bytes')
    else:
        print(f'\n❌ FAILED - returned None')
        
except Exception as e:
    print(f'\n❌ FAILED with error:')
    print(f'   {type(e).__name__}: {e}')
