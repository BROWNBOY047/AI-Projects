import feedparser
import json
from datetime import datetime
import time
import re
from typing import List, Dict, Any

# ============================================
# STEP 1: CONFIGURATION
# ============================================
CONFIG = {
    "total_articles": 150,
    "feeds": [
        "https://www.euronews.com/rss?format=mrss&level=theme&name=news",
        "https://www.euronews.com/rss?level=tag&name=ukraine",
        "https://www.euronews.com/rss?level=tag&name=climate",
        "https://www.euronews.com/rss?level=tag&name=economy",
    ],
    "output_format": "json",  # Can be 'json', 'csv', or 'both'
    "timeout": 10,  # Seconds to wait for feed
}

# ============================================
# STEP 2: FETCH AND PARSE RSS FEED
# ============================================
def fetch_rss_feed(feed_url: str, timeout: int = 10) -> List[Dict]:
    """
    Fetch and parse an RSS feed using feedparser

    Args:
        feed_url: RSS feed URL
        timeout: Request timeout in seconds

    Returns:
        List of article entries
    """
    try:
        print(f"📡 Fetching: {feed_url}")

        # Parse the feed
        feed = feedparser.parse(feed_url)

        # Check for errors
        if feed.bozo:
            print(f"⚠️ Warning: {feed.bozo_exception}")

        entries = feed.entries
        print(f"   ✅ Found {len(entries)} articles")

        return entries

    except Exception as e:
        print(f"❌ Error fetching {feed_url}: {e}")
        return []

# ============================================
# STEP 3: EXTRACT DATA FROM ENTRY
# ============================================
def extract_article_data(entry: feedparser.FeedParserDict) -> Dict[str, Any]:
    """
    Extract clean data from an RSS entry

    Args:
        entry: RSS feed entry

    Returns:
        Dictionary with article data
    """
    try:
        # --- TITLE ---
        title = entry.get('title', '').strip()
        if not title:
            title = "No title available"

        # --- URL ---
        url = entry.get('link', '')
        if not url:
            url = entry.get('guid', '')

        # --- SUMMARY ---
        summary = entry.get('description', '')
        if not summary:
            summary = entry.get('summary', '')
        # Clean HTML tags
        if summary:
            summary = re.sub(r'<[^>]+>', '', summary)
            summary = re.sub(r'\s+', ' ', summary).strip()
        else:
            summary = "No summary available"

        # --- DATE ---
        date = None
        date_parsed = None

        # Try different date fields
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            date_parsed = entry.published_parsed
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            date_parsed = entry.updated_parsed
        elif entry.get('pubDate'):
            date = entry.get('pubDate')
        elif entry.get('updated'):
            date = entry.get('updated')

        # Convert parsed date to string
        if date_parsed:
            try:
                date = datetime(*date_parsed[:6]).isoformat()
            except:
                try:
                    date = datetime(*date_parsed[:6]).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    date = str(date_parsed)

        if not date:
            date = "No date available"

        # --- IMAGE (if available) ---
        image_url = None
        if hasattr(entry, 'media_content') and entry.media_content:
            for media in entry.media_content:
                if media.get('url'):
                    image_url = media.get('url')
                    break
        elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            for thumb in entry.media_thumbnail:
                if thumb.get('url'):
                    image_url = thumb.get('url')
                    break

        # --- CATEGORIES ---
        categories = []
        if hasattr(entry, 'tags') and entry.tags:
            categories = [tag.term for tag in entry.tags if hasattr(tag, 'term')]

        # --- SOURCE ---
        source = {}
        if hasattr(entry, 'source') and entry.source:
            source = {
                'title': entry.source.get('title', ''),
                'url': entry.source.get('href', '')
            }

        # --- FULL CONTENT (if available) ---
        full_content = ''
        if hasattr(entry, 'content'):
            for content in entry.content:
                if content.get('value'):
                    # Clean HTML
                    clean_text = re.sub(r'<[^>]+>', '', content.value)
                    full_content = re.sub(r'\s+', ' ', clean_text).strip()
                    break
        elif hasattr(entry, 'summary'):
            full_content = entry.get('summary', '')

        return {
            'title': title,
            'url': url,
            'summary': summary,
            'date': date,
            'image_url': image_url,
            'categories': categories,
            'source': source,
            'full_content': full_content[:500] if full_content else '',  # Limit for JSON size
            'scraped_at': datetime.now().isoformat(),
            'feed_source': entry.get('feed_url', '') if hasattr(entry, 'feed_url') else ''
        }

    except Exception as e:
        print(f"⚠️ Error extracting data: {e}")
        return {
            'title': 'Error extracting data',
            'url': '',
            'summary': '',
            'date': '',
            'error': str(e)
        }

# ============================================
# STEP 4: MAIN SCRAPING FUNCTION
# ============================================
def scrape_euronews_articles(
    feeds: List[str],
    total_articles: int = 150
) -> Dict[str, Any]:
    """
    Scrape articles from multiple RSS feeds

    Args:
        feeds: List of RSS feed URLs
        total_articles: Total articles to scrape

    Returns:
        Dictionary with scraped data and metadata
    """
    print("="*80)
    print("📰 EURONEWS RSS SCRAPER (WITH JSON OUTPUT)")
    print("="*80)
    print(f"🎯 Target: {total_articles} articles\n")

    start_time = time.time()
    all_articles = []
    seen_urls = set()
    duplicates = 0
    feed_stats = {}

    for feed_url in feeds:
        if len(all_articles) >= total_articles:
            break

        feed_start = time.time()
        entries = fetch_rss_feed(feed_url)

        feed_stats[feed_url] = {
            'total_entries': len(entries),
            'scraped': 0,
            'time': 0
        }

        for entry in entries:
            if len(all_articles) >= total_articles:
                break

            article = extract_article_data(entry)

            # Avoid duplicates
            if article.get('url') and article['url'] in seen_urls:
                duplicates += 1
                continue

            if article.get('url'):
                seen_urls.add(article['url'])
                all_articles.append(article)
                feed_stats[feed_url]['scraped'] += 1

                # Progress indicator
                print(f"✅ {len(all_articles):3d}/{total_articles} - {article['title'][:50]}...")

        feed_stats[feed_url]['time'] = round(time.time() - feed_start, 2)

    # Prepare final output
    result = {
        'metadata': {
            'total_scraped': len(all_articles),
            'target': total_articles,
            'duplicates_skipped': duplicates,
            'feeds_used': len(feeds),
            'scraping_duration': round(time.time() - start_time, 2),
            'scraped_at': datetime.now().isoformat(),
            'feed_stats': feed_stats
        },
        'articles': all_articles
    }

    print(f"\n📊 Scraping complete!")
    print(f"   ✅ Scraped: {len(all_articles)} articles")
    print(f"   ⏭️  Duplicates skipped: {duplicates}")
    print(f"   ⏱️  Duration: {result['metadata']['scraping_duration']} seconds")

    return result

# ============================================
# STEP 5: SAVE TO JSON
# ============================================
def save_to_json(data: Dict, filename_prefix: str = 'euronews_articles') -> str:
    """
    Save scraped data to JSON file

    Args:
        data: Dictionary with scraped data
        filename_prefix: Prefix for filename

    Returns:
        Filename of saved JSON
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.json"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"💾 JSON saved to: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error saving JSON: {e}")
        return ""

# ============================================
# STEP 6: SAVE TO CSV (Optional)
# ============================================
def save_to_csv(data: Dict, filename_prefix: str = 'euronews_articles') -> str:
    """
    Save scraped data to CSV file (flat version)

    Args:
        data: Dictionary with scraped data
        filename_prefix: Prefix for filename

    Returns:
        Filename of saved CSV
    """
    import csv

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.csv"

    try:
        articles = data.get('articles', [])
        if not articles:
            print("⚠️ No articles to save to CSV")
            return ""

        # CSV columns
        fieldnames = ['title', 'url', 'summary', 'date', 'categories', 'source', 'scraped_at']

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for article in articles:
                # Flatten nested data
                row = {
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'summary': article.get('summary', ''),
                    'date': article.get('date', ''),
                    'categories': ', '.join(article.get('categories', [])),
                    'source': article.get('source', {}).get('title', ''),
                    'scraped_at': article.get('scraped_at', '')
                }
                writer.writerow(row)

        print(f"💾 CSV saved to: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")
        return ""

# ============================================
# STEP 7: DISPLAY RESULTS
# ============================================
def display_results(data: Dict):
    """Pretty display scraped data"""
    articles = data.get('articles', [])
    metadata = data.get('metadata', {})

    print("\n" + "="*80)
    print(f"📊 SCRAPED {len(articles)} ARTICLES")
    print("="*80)
    print(f"   ⏱️  Duration: {metadata.get('scraping_duration', 0)} seconds")
    print(f"   📡 Feeds used: {metadata.get('feeds_used', 0)}")
    print(f"   ⏭️  Duplicates skipped: {metadata.get('duplicates_skipped', 0)}")
    print("="*80)

    # Show first 3 articles
    for i, article in enumerate(articles[:3], 1):
        print(f"\n📌 Article #{i}")
        print(f"📰 TITLE: {article['title']}")
        print(f"📝 SUMMARY: {article['summary'][:120]}..." if len(article['summary']) > 120 else f"📝 SUMMARY: {article['summary']}")
        print(f"📅 DATE: {article['date']}")
        print(f"🔗 URL: {article['url'][:80]}..." if len(article['url']) > 80 else f"🔗 URL: {article['url']}")
        if article.get('categories'):
            print(f"🏷️  CATEGORIES: {', '.join(article['categories'][:3])}")
        print("-"*80)

# ============================================
# STEP 8: MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    # Configuration
    FEEDS = [
        "https://www.euronews.com/rss?format=mrss&level=theme&name=news",
        "https://www.euronews.com/rss?level=tag&name=ukraine",
        "https://www.euronews.com/rss?level=tag&name=climate",
        "https://www.euronews.com/rss?level=tag&name=economy",
    ]
    TOTAL_ARTICLES = 150

    # Scrape articles
    scraped_data = scrape_euronews_articles(FEEDS, TOTAL_ARTICLES)

    if scraped_data['articles']:
        # Display results
        display_results(scraped_data)

        # Save to JSON
        json_file = save_to_json(scraped_data)

        # Save to CSV (optional)
        csv_file = save_to_csv(scraped_data)

        print(f"\n✅ SUCCESS! Scraped {len(scraped_data['articles'])} articles")
        print(f"   📁 JSON: {json_file}")
        if csv_file:
            print(f"   📁 CSV: {csv_file}")
    else:
        print("❌ No articles scraped. Check the RSS feed URLs.")