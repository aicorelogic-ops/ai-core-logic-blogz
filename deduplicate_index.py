"""
Deduplicate article cards in index.html
"""

import re
import os

def deduplicate_index(index_path="blog/index.html"):
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by <article ...> </article>
    # We want to keep everything before the first article, then the unique articles, then everything after the last article
    
    # Simple regex to find all article cards
    article_pattern = re.compile(r'<article class="article-card">.*?</article>', re.DOTALL)
    articles = article_pattern.findall(content)
    
    if not articles:
        print("No articles found in index.html")
        return

    # Find unique articles by the href link
    unique_articles = []
    seen_links = set()
    
    link_pattern = re.compile(r'href="([^"]+)"')
    
    for art in articles:
        link_match = link_pattern.search(art)
        if link_match:
            link = link_match.group(1)
            # Skip placeholders like "#"
            if link == "#":
                unique_articles.append(art)
                continue
                
            if link not in seen_links:
                seen_links.add(link)
                unique_articles.append(art)
            else:
                print(f"Removing duplicate: {link}")
        else:
            unique_articles.append(art)
            
    # Now we need to put them back.
    # We'll find the main container start and end
    main_start_tag = '<main id="news-feed">'
    main_end_tag = '</main>'
    
    try:
        header_part = content.split(main_start_tag)[0] + main_start_tag
        footer_part = main_end_tag + content.split(main_end_tag)[-1]
        
        # Join unique articles with some spacing
        new_content = header_part + "\n\n        " + "\n\n        ".join(unique_articles) + "\n\n    " + footer_part
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Successfully deduplicated index.html. Kept {len(unique_articles)} unique articles.")
    except Exception as e:
        print(f"Error rebuilding index.html: {e}")

if __name__ == "__main__":
    deduplicate_index()
