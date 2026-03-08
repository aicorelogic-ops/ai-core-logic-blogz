#!/bin/bash
# =============================================================
# AI Core Logic - News Bot Pipeline Runner
# Runs: Blog Generation → Facebook Posting
# Can be triggered by cron OR manually by the assistant
# =============================================================

set -e

# Navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Logging
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/pipeline_$(date +%Y%m%d_%H%M%S).log"

echo "=============================================" | tee -a "$LOG_FILE"
echo "Pipeline started: $(date)" | tee -a "$LOG_FILE"
echo "=============================================" | tee -a "$LOG_FILE"

# Activate virtual environment if it exists
if [ -d "$PROJECT_ROOT/.venv" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
    echo "✅ Virtual environment activated" | tee -a "$LOG_FILE"
elif [ -d "$PROJECT_ROOT/venv" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
    echo "✅ Virtual environment activated" | tee -a "$LOG_FILE"
fi

# Step 1: Generate Blog Post
echo "" | tee -a "$LOG_FILE"
echo "📝 Step 1: Generating blog post..." | tee -a "$LOG_FILE"
python -m news_bot.main 2>&1 | tee -a "$LOG_FILE"
BLOG_EXIT=$?

if [ $BLOG_EXIT -ne 0 ]; then
    echo "❌ Blog generation failed (exit code: $BLOG_EXIT)" | tee -a "$LOG_FILE"
    exit 1
fi

echo "✅ Blog generation complete" | tee -a "$LOG_FILE"

# Brief pause between steps
sleep 5

# Step 2: Generate and Post to Facebook
echo "" | tee -a "$LOG_FILE"
echo "📘 Step 2: Posting to Facebook..." | tee -a "$LOG_FILE"
python -m news_bot.facebook_blog_poster 2>&1 | tee -a "$LOG_FILE"
FB_EXIT=$?

if [ $FB_EXIT -ne 0 ]; then
    echo "❌ Facebook posting failed (exit code: $FB_EXIT)" | tee -a "$LOG_FILE"
    exit 2
fi

echo "✅ Facebook posting complete" | tee -a "$LOG_FILE"

# Cleanup old logs (keep last 30 days)
find "$LOG_DIR" -name "pipeline_*.log" -mtime +30 -delete 2>/dev/null

echo "" | tee -a "$LOG_FILE"
echo "=============================================" | tee -a "$LOG_FILE"
echo "Pipeline finished: $(date)" | tee -a "$LOG_FILE"
echo "=============================================" | tee -a "$LOG_FILE"
