#!/usr/bin/env python3
"""Fetch and condense F1 news articles for use in predictions."""
import json
import feedparser
from datetime import datetime
from pathlib import Path

ARTICLE_FETCH_LIMIT = 9

RSS_FEEDS = [
    "https://www.formula1.com/en/latest/all.xml",
    "https://racer.com/f1/feed",
    "https://feeds.bbci.co.uk/sport/formula1/rss.xml",  # BBC F1
]

def fetch_f1_news():
    articles = []

    try:
        articles = _fetch_from_rss()
    except Exception as e:
        print(f"RSS fetch failed: {e}")

    # store the latest ARTICLE_FETCH_LIMIT articles in cache
    articles.sort(key=lambda x: x.get("published_at", ""), reverse=True)
    articles = articles[:ARTICLE_FETCH_LIMIT]

    # Save to cache
    _save_news_cache(articles)

    return articles

def _fetch_from_rss():
    articles = []
    for rss_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(rss_url)

            for entry in feed.entries[:ARTICLE_FETCH_LIMIT]:
                title = entry.get("title", "")
                summary = entry.get("summary", "") or entry.get("description", "")
                link = entry.get("link", "")
                published = entry.get("published", "") or entry.get("updated", "")

                # Condense to a short paragraph
                condensed = _condense_article(title, summary, "")

                if condensed:
                    source_name = _extract_source_name(rss_url)
                    articles.append({
                        "title": title,
                        "summary": condensed,
                        "source": source_name,
                        "published_at": published,
                        "url": link,
                    })

            if articles:
                return articles[:ARTICLE_FETCH_LIMIT]
        except Exception as e:
            continue  # Try next feed on error

    return articles

def _extract_source_name(rss_url):
    """Extract source name from RSS feed URL."""
    if "motorsport" in rss_url:
        return "Motorsport.com"
    elif "sky" in rss_url:
        return "Sky Sports"
    elif "bbci" in rss_url:
        return "BBC Sport"
    else:
        return "F1 News"

def _condense_article(title, description, content):
    """
    Condense article to a short paragraph.
    Combines title with description/content and limits to ~150 characters.
    """
    # Use description if available, otherwise use content preview
    text = description or content or ""

    # Remove HTML tags if present
    text = text.replace("<p>", "").replace("</p>", "").replace("<br>", " ")

    # Combine title with summary
    if title and text:
        combined = f"{title}. {text}"
    else:
        combined = title or text

    # Truncate to ~300 characters for prompt
    if len(combined) > 300:
        combined = combined[:300] + "..."

    return combined.strip()

def _save_news_cache(articles):
    """Save fetched news to a cache file."""
    cache_path = Path(__file__).parent.parent / "data" / "f1_news_cache.json"
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    cache = {
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "articles": articles,
    }

    cache_path.write_text(json.dumps(cache, indent=2))
    print(f"Saved {len(articles)} articles to {cache_path}")

def format_news_for_prompt(articles):
    """Format articles into a string suitable for the prediction prompt."""
    if not articles:
        return "(No recent F1 news available)"

    lines = ["**Recent F1 News:**"]
    for i, article in enumerate(articles, 1):
        lines.append(f"{i}. {article['summary']}")
        lines.append(f"   (Source: {article['source']}, {article['published_at'][:10]})")

    return "\n".join(lines)

def main():
    print("Fetching latest F1 news articles...")
    articles = fetch_f1_news()

    if not articles:
        print("Failed to fetch any articles. Check your internet connection.")
        return

    # Show formatted version
    print("\n" + "=" * 60)
    print("Formatted for prediction prompt:")
    print("=" * 60)
    print(format_news_for_prompt(articles))


if __name__ == "__main__":
    main()
