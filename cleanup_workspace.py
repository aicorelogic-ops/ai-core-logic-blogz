import os
import shutil
import glob

# Configuration
DELETE_PATTERNS = [
    "debug_*.py",
    "test_*.py",
    "list_models*.py",
    "check_*.py",
    "error_*.txt",
    "fb_error.txt",
    "diff_*.txt",
    "debug_output.txt",
    "token_check*.txt",
    "duplicate_report.txt",
    "style_analysis.txt",
    "force_rebuild.txt",
    "valid_models.txt",
    "models.txt",
    "models_list*.txt",
    "all_models.txt",
    "post_blackstone_fb.py",
    "post_square_*.py",
    "retry_last.py",
    "do_exchange.py",
    "token_exchange.py",
    "temp_viral_bg_*.jpg",
    "test_graphic.jpg",
    "viral_script_output.json",
    "__pycache__"
]

ARCHIVE_PATTERNS = [
    "deduplicate_*.py",
    "delete_duplicates.py",
    "find_duplicates.py",
    "fix_editorial_title.py",
    "migrate_blog_posts.py",
    "regenerate_*.py",
    "update_blog_posts.py",
    "generate_categories.py",
    "generate_hvco.py",
    "analyze_inspiration.py"
]

ARCHIVE_DIR = "scripts/archive"

def cleanup():
    print("Starting workspace cleanup...")
    
    # Create archive directory
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)
        print(f"Created archive directory: {ARCHIVE_DIR}")

    # Delete files
    for pattern in DELETE_PATTERNS:
        files = glob.glob(pattern)
        for f in files:
            try:
                if os.path.isdir(f):
                    shutil.rmtree(f)
                    print(f"Deleted directory: {f}")
                else:
                    os.remove(f)
                    print(f"Deleted file: {f}")
            except Exception as e:
                print(f"Error deleting {f}: {e}")

    # Archive files
    for pattern in ARCHIVE_PATTERNS:
        files = glob.glob(pattern)
        for f in files:
            try:
                dest = os.path.join(ARCHIVE_DIR, os.path.basename(f))
                shutil.move(f, dest)
                print(f"Archived file: {f} -> {dest}")
            except Exception as e:
                print(f"Error archiving {f}: {e}")
                
    # Clean temp_images content but keep folder
    if os.path.exists("temp_images"):
        for f in os.listdir("temp_images"):
            path = os.path.join("temp_images", f)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"Cleaned temp image: {path}")
            except Exception as e:
                print(f"Error cleaning temp image {path}: {e}")

    print("Cleanup complete.")

if __name__ == "__main__":
    cleanup()
