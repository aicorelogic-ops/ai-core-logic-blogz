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

1.  The script navigates to the blog directory.
2.  It stages all changes (`git add .`).
3.  It commits changes with a timestamped message (or user-provided message).
4.  It pushes the commit to `origin main`.
5.  It verifies the push command exit code.

## Requirements

-   Git must be installed and configured.
-   The `blog/` directory must be a git repository.
-   SSH keys or credentials for pushing to GitHub must be set up.
