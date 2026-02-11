"""
Article Tracker - Prevent duplicate posts
Tracks which articles have been processed to avoid posting the same content twice
"""

import json
import os
from datetime import datetime
from pathlib import Path

class ArticleTracker:
    def __init__(self, tracking_file="blog/processed_articles.json"):
        self.tracking_file = tracking_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create tracking file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.tracking_file), exist_ok=True)
        if not os.path.exists(self.tracking_file):
            with open(self.tracking_file, 'w') as f:
                json.dump({}, f)
    
    def _load_data(self):
        """Load tracking data from JSON"""
        try:
            with open(self.tracking_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] Error loading tracker: {e}")
            return {}
    
    def _save_data(self, data):
        """Save tracking data to JSON"""
        try:
            with open(self.tracking_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Error saving tracker: {e}")
    
    def is_processed(self, article_url):
        """
        Check if article has already been processed
        
        Args:
            article_url: URL of the article
            
        Returns:
            bool: True if already processed, False otherwise
        """
        data = self._load_data()
        return article_url in data
    
    def mark_as_processed(self, article_url, metadata):
        """
        Mark article as processed with metadata
        
        Args:
            article_url: URL of the article
            metadata: Dict with keys like:
                - title: Article title
                - blog_path: Path to generated blog
                - image_path: Path to viral image
                - reel_path: Path to viral reel
                - facebook_post_id: FB post ID
        """
        data = self._load_data()
        
        # Add timestamp
        metadata['processed_date'] = datetime.now().isoformat()
        
        # Store
        data[article_url] = metadata
        self._save_data(data)
        
        print(f"[OK] Tracked: {metadata.get('title', article_url)}")
    
    def get_processed_count(self):
        """Get total number of processed articles"""
        data = self._load_data()
        return len(data)
    
    def get_recent_articles(self, days=7):
        """
        Get articles processed in the last N days
        
        Args:
            days: Number of days to look back
            
        Returns:
            list: List of (url, metadata) tuples
        """
        from datetime import timedelta
        
        data = self._load_data()
        cutoff = datetime.now() - timedelta(days=days)
        
        recent = []
        for url, metadata in data.items():
            try:
                processed_date = datetime.fromisoformat(metadata['processed_date'])
                if processed_date >= cutoff:
                    recent.append((url, metadata))
            except:
                continue
        
        # Sort by date (newest first)
        recent.sort(key=lambda x: x[1]['processed_date'], reverse=True)
        return recent
    
    def get_article_info(self, article_url):
        """
        Get metadata for a specific article
        
        Args:
            article_url: URL of the article
            
        Returns:
            dict: Metadata or None if not found
        """
        data = self._load_data()
        return data.get(article_url)
    
    def remove_article(self, article_url):
        """
        Remove article from tracking (for reprocessing)
        
        Args:
            article_url: URL of the article to remove
        """
        data = self._load_data()
        if article_url in data:
            del data[article_url]
            self._save_data(data)
            print(f"[REMOVED] Removed from tracking: {article_url}")
            return True
        return False
    
    def list_all_articles(self):
        """Get all tracked articles"""
        data = self._load_data()
        articles = []
        
        for url, metadata in data.items():
            articles.append({
                'url': url,
                'title': metadata.get('title', 'Unknown'),
                'processed_date': metadata.get('processed_date', 'Unknown'),
                'facebook_post_id': metadata.get('facebook_post_id', 'N/A')
            })
        
        # Sort by date (newest first)
        articles.sort(key=lambda x: x['processed_date'], reverse=True)
        return articles
    
    def print_summary(self):
        """Print summary of tracked articles"""
        articles = self.list_all_articles()
        
        print(f"\n[Article Tracker Summary]")
        print(f"{'='*60}")
        print(f"Total Processed: {len(articles)}")
        print(f"\nRecent Articles (last 7 days): {len(self.get_recent_articles(7))}")
        
        if articles:
            print(f"\n5 Most Recent:")
            for article in articles[:5]:
                print(f"  - {article['title'][:50]}")
                print(f"    Date: {article['processed_date'][:10]}")
                print(f"    FB ID: {article['facebook_post_id']}")
                print()


if __name__ == "__main__":
    # Test tracker
    tracker = ArticleTracker()
    tracker.print_summary()
