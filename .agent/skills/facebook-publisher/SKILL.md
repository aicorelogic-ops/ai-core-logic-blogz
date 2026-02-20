---
name: facebook-publisher
description: Automatically publish latest blog posts to the AI Core Logic Facebook page. It handles content generation (Gemini), viral image creation (Vertex AI), and link-in-comments posting. Use this skill when the user wants to share new blog content to Facebook without requiring browser-based verification.
---

# Facebook Publisher Skill

This skill automates the process of sharing blog posts from the `AI Core Logic` blog to the official Facebook Page with high-engagement formatting and visuals.

## 🚀 Usage

Run the following command to identify the latest unpublished blog and post it to Facebook:

```powershell
python -m news_bot.facebook_blog_poster
```

## 🛠️ Workflow

1.  **Scanner**: Scans `blog/posts/` for the most recent HTML files.
2.  **Filter**: Checks `news_bot/posted_to_facebook.json` to ensure the post hasn't been shared yet.
3.  **Live Verification (Web First)**: Pings the blog post's public URL. If it returns `404 Not Found`, the process **aborts**. The post must be live on GitHub Pages before Facebook generation begins.
4.  **Viral Copy**: Uses Gemini to write a high-arousal social post (Hook + Scannable Bullets + Link-in-Comments CTA).
5.  **"Infotainment" Graphic**: Generates a **"Breaking News" Graphic** using the **Split Composition** (Top Photo / Bottom Dark Block).
    *   **Prompt Logic**: Enforces a top-heavy photo, a bottom dark text container, tighter inset anchoring, and a massive **Text Stack** (Headline + Subheader with Yellow Highlight Bar).
    *   **Style**: Dense, urgent, cable news alert style.
6.  **Publish**: Uploads the photo to the Facebook feed and automatically adds the blog link as the first comment.

## 🛡️ Reliability Protocol (Web-First)

The process is designed to be **fail-proof** with the following mechanisms:

1.  **Selection Logic (Newest Unpublished)**: Scans the **Top 20** newest blog posts (sorted by date) and automatically selects the **single most recent one** that has NOT yet been posted to Facebook. It ignores older or already-published articles.
2.  **Live URL Verification (Ghost Post Prevention)**:
    *   **Strict Check**: The script pings the public GitHub Pages URL.
    *   **Retry Logic**: Waits up to **60 seconds** (30 retries) for the deployment to propagate.
    *   **Abort Criteria**: If the URL returns `404` after retries, the process **stops** to prevent broken links.
3.  **Graphic Standards**:
    *   **"High-Impact" Template**: Enforces a massive 2-line headline with **mandatory yellow highlighting** and a strict 50% dark gradient.
    *   **Brand Safety**: The "AI CORE LOGIC" logo is always placed in a semi-transparent banner for readability.

## 🛡️ Posting Policy

*   **Verification**: ⚠️ **SKIPPED**. For this specific skill, manual or browser-based verification of the feed is NOT required. The API confirmation (Post ID) is considered sufficient.
*   **Duplicate Prevention**: The script automatically maintains the tracking JSON; do not force-post if the script says "All blogs have been posted".
*   **Aesthetics**: Always ensure `image_generator.py` is using the latest "Infotainment News Graphic" prompt logic for high-quality visuals.

## 📂 Configuration

*   **`news_bot/posted_to_facebook.json`**: History of all shared posts.
*   **`news_bot/publisher.py`**: Contains the low-level `FacebookPublisher` logic (Graph API).
*   **`news_bot/facebook_blog_poster.py`**: The main orchestrator and formatting logic.
