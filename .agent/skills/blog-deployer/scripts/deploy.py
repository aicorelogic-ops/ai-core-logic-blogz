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
