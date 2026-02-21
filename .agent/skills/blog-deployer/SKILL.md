---
name: blog-deployer
description: Automates the deployment of blog design and content changes to GitHub. Use this skill when the user asks to "push changes", "deploy blog", "update live site", or "publish updates" after modifying HTML, CSS, JS, or content files in the blog directory.
---

# Blog Deployer

This skill automates the process of committing and pushing changes from the local blog directory to the GitHub repository.

## Usage

Run the deployment script to push all current changes to the `main` branch.

```python
python .agent/skills/blog-deployer/scripts/deploy.py
```

## Workflow

1.  **Cache Busting**: Scans all `.html` files in the blog directory and increments the `style.css?v=X` version number. This ensures users see design changes immediately.
2.  **Git Operations**:
    *   Stages all changes (`git add .`).
    *   Commits with a timestamped message.
    *   Pushes to `origin main`.
3.  **Verification**: Checks exit codes to ensure successful push.

## Requirements

-   Git must be installed and configured.
-   The `blog/` directory must be a git repository.
-   SSH keys or credentials for pushing to GitHub must be set up.
