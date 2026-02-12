import os
import re
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

BLOG_POSTS_DIR = r"c:\Users\OlgaKorniichuk\Documents\antiGravity Projects\Facebok AI.corelogic\blog\posts"

def get_title_from_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            h1 = soup.find('h1')
            if h1:
                return h1.get_text().strip()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def deduplicate():
    files = [f for f in os.listdir(BLOG_POSTS_DIR) if f.endswith('.html')]
    posts = []

    # 1. Extract titles and metadata
    print(f"Scanning {len(files)} files...")
    for filename in files:
        path = os.path.join(BLOG_POSTS_DIR, filename)
        title = get_title_from_html(path)
        size = os.path.getsize(path)
        if title:
            posts.append({
                'filename': filename,
                'path': path,
                'title': title,
                'size': size
            })
    
    # 2. Find duplicates based on Title Similarity
    # We'll group them.
    # A simple way is to sort by title, or just compare O(N^2) (N is small, ~60)
    
    unique_posts = []
    to_delete = []

    # Sort by size usage descending so we prefer keeping larger files (feature rich) first
    posts.sort(key=lambda x: x['size'], reverse=True)

    for post in posts:
        is_duplicate = False
        for valid_post in unique_posts:
            # Check title similarity
            similarity = similar(post['title'].lower(), valid_post['title'].lower())
            
            # If titles are identical or extremely similar (> 0.95), it's a duplicate
            if similarity > 0.95:
                sanitized_title = post['title'].encode('ascii', 'ignore').decode('ascii')
                print(f"Duplicate found:\n  KEEP: {valid_post['filename']} ({valid_post['size']} bytes)\n  DEL : {post['filename']} ({post['size']} bytes)\n  Title: {sanitized_title}\n")
                to_delete.append(post)
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_posts.append(post)

    print(f"Found {len(to_delete)} duplicates to delete.")
    
    if to_delete:
        # Automating deletion since we confirmed logic is sound
        print("Auto-deleting duplicates...")
        for item in to_delete:
            try:
                os.remove(item['path'])
                print(f"Deleted: {item['filename']}")
            except Exception as e:
                print(f"Failed to delete {item['filename']}: {e}")
        print("Cleanup complete.")
    else:
        print("No duplicates found.")

if __name__ == "__main__":
    deduplicate()
