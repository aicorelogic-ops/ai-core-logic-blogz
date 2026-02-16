import feedparser
from datetime import datetime, timedelta
from news_bot.settings import RSS_FEEDS, KEYWORDS

def debug_feeds():
    print("Debugging RSS Feeds...")
    print(f"Keywords: {KEYWORDS}")
    
    hours_back = 72
    time_threshold = datetime.now() - timedelta(hours=hours_back)
    
    for feed_url in RSS_FEEDS:
        print(f"\nChecking {feed_url}...")
        try:
            feed = feedparser.parse(feed_url)
            print(f"  Entries found: {len(feed.entries)}")
            
            # Check first 5 entries
            for i, entry in enumerate(feed.entries[:5]):
                print(f"  [{i}] {entry.title}")
                
                # Check date
                published = getattr(entry, "published_parsed", None)
                if published:
                    pub_date = datetime(*published[:6])
                    print(f"      Date: {pub_date} (Age: {datetime.now() - pub_date})")
                    if pub_date < time_threshold:
                        print(f"      ❌ Too old (Threshold: {time_threshold})")
                    else:
                        print(f"      ✅ Date OK")
                else:
                    print("      ⚠️ No date found")
                    
                # Check keywords
                title = entry.title.lower()
                summary = getattr(entry, "summary", "").lower()
                matches = [kw for kw in KEYWORDS if kw in title or kw in summary]
                if matches:
                    print(f"      ✅ Keywords found: {matches}")
                else:
                    print(f"      ❌ No keywords match")
                    
        except Exception as e:
            print(f"  ❌ Error parsing feed: {e}")

if __name__ == "__main__":
    debug_feeds()
