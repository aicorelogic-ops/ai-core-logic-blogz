import requests
import os

# The dynamic URL that was generated
image_url = "https://image.pollinations.ai/prompt/editorial%20illustration%20for%20news%20article%3A%20The%20Death%20of%20the%20Middle%20Manager.%20cyberpunk%20style%2C%20neon%2C%20data%20visualization%2C%20minimalist%2C%203d%20render%2C%20high%20quality%2C%208k%2C%20dark%20blue%20and%20mint%20green%20palette?width=1200&height=600&nologo=true"

# Target path
assets_dir = os.path.join("blog", "assets")
os.makedirs(assets_dir, exist_ok=True)
save_path = os.path.join(assets_dir, "middle_manager.jpg")

print(f"⬇️ Downloading image from Pollinations...")
try:
    response = requests.get(image_url, timeout=30)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Image saved to {save_path}")
    else:
        print(f"❌ Failed to download: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")
