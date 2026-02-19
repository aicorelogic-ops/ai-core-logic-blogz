---
name: news-publisher
description: Automated workflow for curated AI news publishing. Use this skill when the user wants to publish a new blog post. It handles fetching news, scoring virality, generating content-aware images (Vertex AI/PIL), and deploying to GitHub.
---

# News Publisher Skill

This skill guides the automated process of fetching, analyzing, generating, and publishing high-quality AI news content to the **AI Core Logic** blog.

## 🚀 Usage

Run the main bot script to execute the full pipeline:

```powershell
python -m news_bot.main
```

## 🛠️ Workflow Overview

1.  **Fetch & Filter**: Scrapes RSS feeds (TechCrunch, Verge, etc.) defined in `settings.py`.
2.  **Score & Select**: Uses Gemini to score articles for "Viral Potential". The highest scoring article wins.
3.  **Generate Content**:
    *   Summarizes the article.
    *   Generates a **Content-Aware Image**.
4.  **Publish**:
    *   Creates an HTML blog post in `blog/posts/`.
    *   Updates `blog/index.html`.
    *   **Auto-Deploys** to GitHub Pages (commits and pushes).

## 🎨 Image Generation Logic

The system uses a robust cascading fallback mechanism to ensure every post has an image:

1.  **Primary**: **Vertex AI Imagen 3.0** (Google Cloud).
    *   *Config*: Region **MUST** be set to `us-east4` in `settings.py` for stability.
    *   *Prompt Style*: **"Clean & Professional"** — Gemini acts as an AI Art Director, extracting 3 variables from the article to build the final prompt:
        *   **`[Core Subject]`**: The most tangible object, setting, or person in the article.
        *   **`[Key Visual Details]`**: Specific visual elements to integrate (company logos, devices, relevant CEOs if they are the main subject). Logos are placed organically (on a device, wall, etc). **Public figures are NEVER hallucinated** — they are only included if explicitly the article's main focus.
        *   **`[Color Palette]`**: Psychology-matched color (e.g., Blue=trust, Green=growth).
    *   *Aesthetic*: Understated editorial photography. 40%+ active whitespace. No surrealism, no cartoons.
2.  **Secondary**: **Vertex AI Imagen 2.0** (automatic fallback if Imagen 3.0 quota is hit).
3.  **Tertiary**: **Pollinations AI** (External API, free).
4.  **Safety Net**: **PIL (Python Imaging Library)**.
    *   Generates a clean "Title Card" with the article headline if all AI generation fails.
    *   Prevents broken layouts or missing image updates.

### Debugging Image Issues

If images are missing or look wrong:

1.  **Check Logs**:
    *   View `image_gen_errors.log` in the root directory for specific API failures (Quota, Auth, timeouts).
2.  **Verify Region**:
    *   Ensure `VERTEX_LOCATION = "us-east4"` in `news_bot/settings.py`. `us-central1` is prone to quotas.
3.  **Force Regeneration**:
    *   If a post was created with a bad image, **DELETE** the HTML file in `blog/posts/`.
    *   **REMOVE** the article URL entry from `blog/processed_articles.json`.
    *   Run `python -m news_bot.main` again.

## 📂 Configuration

*   **`news_bot/settings.py`**: API Keys (`GOOGLE_API_KEY`, `VERTEX_PROJECT_ID`), Target Feeds, and Keywords.
*   **`blog/processed_articles.json`**: Tracks history to prevent duplicate posts. Delete entries here to re-run specific articles.
*   **`news_bot/image_generator.py`**: Contains `create_content_aware_prompt()` (the Gemini Art Director with Clean & Professional rules) and the `_generate_with_vertex` / `_generate_with_pil` implementations.

## 📢 Post-Publishing

After the blog post is live (verified on GitHub Pages), you can generate a social media version:

```powershell
python -m news_bot.facebook_blog_poster
```
