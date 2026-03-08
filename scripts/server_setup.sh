#!/bin/bash
# =============================================================
# AI Core Logic - Server Setup Script
# Run this ONCE on the DigitalOcean droplet after uploading
# =============================================================

set -e

echo "🚀 AI Core Logic - Server Setup"
echo "================================"

PROJECT_DIR="/opt/ai-core-logic"

# 1. Create project directory
echo ""
echo "📁 Setting up project directory..."
sudo mkdir -p "$PROJECT_DIR"
sudo chown "$USER:$USER" "$PROJECT_DIR"

# 2. Check if archive was uploaded to /tmp
if [ -f "/tmp/ai-core-logic-deploy.tar.gz" ]; then
    echo "📦 Extracting deployment archive..."
    tar -xzf /tmp/ai-core-logic-deploy.tar.gz -C "$PROJECT_DIR"
    echo "✅ Archive extracted to $PROJECT_DIR"
else
    echo "❌ Archive not found at /tmp/ai-core-logic-deploy.tar.gz"
    echo "   Upload it first: scp ai-core-logic-deploy.tar.gz root@YOUR_SERVER:/tmp/"
    exit 1
fi

# 3. Create Python virtual environment
echo ""
echo "🐍 Setting up Python virtual environment..."
cd "$PROJECT_DIR"
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r news_bot/requirements.txt

# 5. Make scripts executable
echo ""
echo "🔧 Setting permissions..."
chmod +x scripts/run_pipeline.sh

# 6. Create necessary directories
mkdir -p temp_images
mkdir -p logs
mkdir -p blog/posts
mkdir -p blog/assets
mkdir -p blog/css
mkdir -p blog/js

# 7. Configure Git (needed for deploying blog to GitHub Pages)
echo ""
echo "🔧 Configuring Git..."
git config --global user.email "aicorelogic.ops@gmail.com"
git config --global user.name "AI Core Logic Bot"

# Check if git repo already initialized
if [ ! -d ".git" ]; then
    echo "   Initializing git repo..."
    git init
    git remote add origin https://github.com/aicorelogic-ops/ai-core-logic-blogz.git
    echo "   ⚠️  You need to configure git credentials for pushing."
    echo "   Run: git config --global credential.helper store"
    echo "   Then do a manual push to save credentials."
fi

# 8. Set up cron jobs (3x daily: 7am, 1pm, 7pm EST)
echo ""
echo "⏰ Setting up cron jobs (3x daily)..."

# Create a cron entry
CRON_CMD="cd $PROJECT_DIR && source venv/bin/activate && bash scripts/run_pipeline.sh >> logs/cron.log 2>&1"

# Write cron entries (avoid duplicates)
(crontab -l 2>/dev/null | grep -v "run_pipeline.sh"; \
 echo "# AI Core Logic - News Bot Pipeline (3x daily)"; \
 echo "0 7 * * * $CRON_CMD"; \
 echo "0 13 * * * $CRON_CMD"; \
 echo "0 19 * * * $CRON_CMD") | crontab -

echo "   ✅ Cron jobs installed:"
echo "   - 7:00 AM daily"
echo "   - 1:00 PM daily"  
echo "   - 7:00 PM daily"

# 9. Summary
echo ""
echo "============================================="
echo "✅ Setup Complete!"
echo "============================================="
echo ""
echo "Project location: $PROJECT_DIR"
echo ""
echo "Manual commands:"
echo "  Run full pipeline:     cd $PROJECT_DIR && source venv/bin/activate && bash scripts/run_pipeline.sh"
echo "  Run blog only:         cd $PROJECT_DIR && source venv/bin/activate && python -m news_bot.main"
echo "  Run facebook only:     cd $PROJECT_DIR && source venv/bin/activate && python -m news_bot.facebook_blog_poster"
echo "  View logs:             ls -la $PROJECT_DIR/logs/"
echo "  View cron schedule:    crontab -l"
echo ""
echo "⚠️  IMPORTANT: Before the first run, make sure Git credentials are configured"
echo "   so the bot can push blog updates to GitHub Pages."
echo "   Run: cd $PROJECT_DIR && git push (and enter your credentials when prompted)"
echo ""
