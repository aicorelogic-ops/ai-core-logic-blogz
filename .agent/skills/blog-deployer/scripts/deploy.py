import os
import subprocess
import sys
import datetime

# Configuration
BLOG_DIR = r"c:\Users\OlgaKorniichuk\Documents\antiGravity Projects\Facebok AI.corelogic\blog"

def run_command(command, cwd=BLOG_DIR):
    """Runs a shell command in the specified directory."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8' # Force UTF-8 for Windows output
        )
        print(f"✅ Executed: {command}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing: {command}")
        print(f"   Exit Code: {e.returncode}")
        print(f"   Stderr: {e.stderr}")
        return False

def main():
    print(f"🚀 Starting Blog Deployment...")
    print(f"   Directory: {BLOG_DIR}")

    if not os.path.exists(BLOG_DIR):
        print(f"❌ Error: Blog directory not found: {BLOG_DIR}")
        sys.exit(1)

    # 0. Auto-Bump CSS Version (Cache Busting)
    print("\n🔄 Checking CSS version in HTML files...")
    import re
    
    html_files_count = 0
    updated_files_count = 0
    
    # Regex to find style.css?v=NUMBER
    css_version_pattern = re.compile(r'(href=["\']css/style\.css\?v=)(\d+)(["\'])')

    for root, dirs, files in os.walk(BLOG_DIR):
        for file in files:
            if file.endswith(".html"):
                html_files_count += 1
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Search for current version
                    match = css_version_pattern.search(content)
                    if match:
                        current_ver = int(match.group(2))
                        new_ver = current_ver + 1
                        
                        # Replace with new version
                        new_content = css_version_pattern.sub(f'\g<1>{new_ver}\g<3>', content)
                        
                        if content != new_content:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            print(f"   ✨ Bumped CSS version to v{new_ver} in {file}")
                            updated_files_count += 1
                except Exception as e:
                    print(f"   ⚠️ Warning: Could not process {file}: {e}")

    if updated_files_count > 0:
        print(f"   ✅ Updated {updated_files_count} HTML files (Cache Busting Applied).")
    else:
        print(f"   ℹ️ No HTML files needed CSS version update (or pattern not found).")


    # 1. Check Status
    print("\n📊 Checking Git Status...")
    run_command("git status")

    # 2. Add Changes
    print("\n➕ Staging all changes...")
    if not run_command("git add ."):
        print("❌ Failed to stage changes.")
        sys.exit(1)

    # 3. Commit
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Auto-deploy: Update blog content and design - {timestamp}"
    print(f"\n💾 Committing: '{commit_msg}'")
    
    # Check if there are changes to commit first
    status_result = subprocess.run("git status --porcelain", cwd=BLOG_DIR, shell=True, capture_output=True, text=True)
    if not status_result.stdout.strip():
        print("⚠️ No changes to commit. Exiting.")
        sys.exit(0)

    if not run_command(f'git commit -m "{commit_msg}"'):
        print("❌ Failed to commit. (Run manual check if 'nothing to commit')")
        # Proceeding anyway in case it was just empty, but git status check above handles it.

    # 4. Push
    print("\n⬆️ Pushing to GitHub (origin main)...")
    if run_command("git push origin main"):
        print("\n✅ Deployment Successful! The blog will update on GitHub Pages shortly.")
    else:
        print("\n❌ Deployment Failed. Please check the logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
