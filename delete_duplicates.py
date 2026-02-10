"""
Find and delete duplicate blog posts - with delete functionality
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import sys


def extract_title_from_filename(filename):
    """Extract normalized title from filename"""
    # Remove .html or .md extension
    name = filename.replace('.html', '').replace('.md', '')
    
    # Remove date prefix (e.g., "2026-02-08-")
    name = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', name)
    
    # Normalize: lowercase, remove special chars except hyphens
    name = name.lower().strip()
    return name

def find_duplicate_posts(blog_dir="blog"):
    """Find blog posts with duplicate titles"""
    
    # Get all .html and .md files
    blog_files = []
    for file in os.listdir(blog_dir):
        if file.endswith('.html') or file.endswith('.md'):
            filepath = os.path.join(blog_dir, file)
            # Get file stats
            stat = os.stat(filepath)
            blog_files.append({
                'filename': file,
                'filepath': filepath,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'title': extract_title_from_filename(file)
            })
    
    print(f"📁 Found {len(blog_files)} total posts\n")
    
    # Group by normalized title
    title_groups = defaultdict(list)
    for post in blog_files:
        title_groups[post['title']].append(post)
    
    # Find duplicates
    duplicates = {}
    for title, posts in title_groups.items():
        if len(posts) > 1:
            # Sort by modified date (newest first)
            posts.sort(key=lambda x: x['modified'], reverse=True)
            duplicates[title] = posts
    
    return duplicates

def delete_duplicate_posts(duplicates, dry_run=True):
    """Delete duplicate posts (keep newest)"""
    
    deleted_count = 0
    kept_count = 0
    deleted_files = []
    
    for title, posts in duplicates.items():
        print(f"\n📄 Title: {title}")
        print(f"   Found {len(posts)} duplicates:")
        
        # Keep the first (newest)
        keep_post = posts[0]
        print(f"   ✅ KEEP: {keep_post['filename']} (newest)")
        kept_count += 1
        
        # Delete the rest
        for post in posts[1:]:
            print(f"   🗑️ DELETE: {post['filename']}")
            
            if not dry_run:
                try:
                    os.remove(post['filepath'])
                    print(f"      ✅ Deleted successfully")
                    deleted_files.append(post['filename'])
                    deleted_count += 1
                except Exception as e:
                    print(f"      ❌ Error deleting: {e}")
            else:
                deleted_files.append(post['filename'])
                deleted_count += 1
    
    return kept_count, deleted_count, deleted_files


if __name__ == "__main__":
    print("🔍 Scanning blog/posts for duplicate posts...\n")
    
    duplicates = find_duplicate_posts("blog/posts")
    
    if not duplicates:
        print("✅ No duplicates found!")
    else:
        print(f"⚠️ Found {len(duplicates)} titles with duplicates\n")
        print("="*60)
        
        # Check if --delete flag is present
        do_delete = "--delete" in sys.argv
        
        # Show/delete duplicates
        kept, deleted, file_list = delete_duplicate_posts(duplicates, dry_run=not do_delete)
        
        print("\n" + "="*60)
        print(f"\n📊 Summary:")
        print(f"   Files to keep: {kept}")
        print(f"   Files {'deleted' if do_delete else 'to delete'}: {deleted}")
        
        if not do_delete:
            print("\n⚠️ This was a DRY RUN. No files were deleted.")
            print("\nTo actually delete duplicates, run:")
            print("python delete_duplicates.py --delete")
        else:
            print("\n✅ Duplicates deleted successfully!")
            print("\nDeleted files:")
            for f in file_list:
                print(f"   - {f}")
