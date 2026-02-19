import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Facebook Config
FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")

# AI Config
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# OpenAI Config (optional, for DALL-E 3 image generation)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Optional: for premium image generation

# Vertex AI Config (for Imagen) - DEPRECATED, models unavailable
VERTEX_PROJECT_ID = os.getenv("VERTEX_PROJECT_ID")  # e.g., "my-project-123456"
VERTEX_LOCATION = os.getenv("VERTEX_LOCATION", "us-east4")  # Changed to us-east4 for better availability
VERTEX_KEY_PATH = os.getenv("VERTEX_KEY_PATH")  # Optional: path to service account JSON

# News Sources (RSS)
# News Sources (RSS)
RSS_FEEDS = [
    # Major Tech News (Reliable)
    "https://techcrunch.com/feed/", 
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "https://venturebeat.com/feed/",
    
    # AI Specific
    "https://www.artificialintelligence-news.com/feed/",
    
    # Original feeds (commented out as they appear empty)
    # "https://rss.app/feeds/tbdDfZBy9mkg0nUM.xml",
    # "https://rss.app/feeds/top5xHlZ2Hs26yLJ.xml",
]

# Filtering keywords
KEYWORDS = ["automation", "productivity", "efficiency", "small business", "AI tool", "software", "generative ai", "startup"]
