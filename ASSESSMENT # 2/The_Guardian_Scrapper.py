"""
THE GUARDIAN COMPLETE SCRAPER - TARGET 250 ARTICLES
Multi-method approach with incremental saving
"""

import feedparser
import json
import csv
import time
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse

# ============================================
# CONFIGURATION
# ============================================
CONFIG = {
    "total_articles": 250,
    # MULTIPLE RSS FEEDS FOR THE GUARDIAN
    # Simply add /rss to any Guardian URL [citation:5][citation:9]
    "feeds": [
        "https://www.theguardian.com/rss",  # Top stories [citation:9]
        "https://www.theguardian.com/world/rss",  # World news [citation:1][citation:10]
        "https://www.theguardian.com/uk/rss",  # UK news [citation:11]
        "https://www.theguardian.com/us/rss",  # US news [citation:4]
        "https://www.theguardian.com/politics/rss",
        "https://www.theguardian.com/business/rss",
        "https://www.theguardian.com/technology/rss",
        "https://www.theguardian.com/science/rss",
        "https://www.theguardian.com/environment/rss",
        "https://www.theguardian.com/sport/rss",
        "https://www.theguardian.com/commentisfree/rss",
        "https://www.theguardian.com/culture/rss",
        "https://www.theguardian.com/mostviewed/rss",  # Most popular [citation:9]
        "https://www.theguardian.com/tone/obituaries/rss",  # Obituaries [citation:12]
    ],
    # Selenium fallback sections
    "selenium_urls": [
        "https://www.theguardian.com/world",
        "https://www.theguardian.com/uk",
        "https://www.theguardian.com/us",
        "https://www.theguardian.com/politics",
        "https://www.theguardian.com/business",
        "https://www.theguardian.com/technology",
        "https://www.theguardian.com/science",
        "https://www.theguardian.com/environment",
        "https://www.theguardian.com/sport",
        "https://www.theguardian.com/commentisfree",
    ],
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# ============================================
# GLOBAL VARIABLES FOR INCREMENTAL SAVING
# ============================================
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
JSON_FILE = f"guardian_live_{TIMESTAMP}.json"
CSV_FILE = f"guardian_live_{TIMESTAMP}.csv"
ALL_ARTICLES = []
SEEN_URLS = set()

def save_incremental():
    """Save current articles to JSON and CSV incrementally"""
    global ALL_ARTICLES, JSON_FILE, CSV_FILE

    if not ALL_ARTICLES:
        return

    print(f"\n💾 Saving {len(ALL_ARTICLES)} articles...")

    # Save to JSON
    try:
        data = {
            'metadata': {
                'source': 'The Guardian',
                'total_scraped': len(ALL_ARTICLES),
                'scraped_at': datetime.now().isoformat(),
                'target': CONFIG['total_articles']
            },
            'articles': ALL_ARTICLES
        }
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"   ✅ JSON: {JSON_FILE}")
    except Exception as e:
        print(f"   ❌ JSON save error: {e}")

    # Save to CSV
    try:
        fieldnames = ['title', 'url', 'summary', 'date', 'author', 'categories', 'source', 'scrape_method', 'scraped_at']
        has_full = any(a.get('full_content') for a in ALL_ARTICLES)
        if has_full:
            fieldnames.extend(['full_content', 'word_count'])

        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for article in ALL_ARTICLES:
                row = {
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'summary': article.get('summary', ''),
                    'date': article.get('date', ''),
                    'author': article.get('author', ''),
                    'categories': ', '.join(article.get('categories', [])),
                    'source': article.get('source', ''),
                    'scrape_method': article.get('scrape_method', ''),
                    'scraped_at': article.get('scraped_at', '')
                }
                if has_full:
                    row['full_content'] = article.get('full_content', '')
                    row['word_count'] = article.get('word_count', 0)
                writer.writerow(row)
        print(f"   ✅ CSV: {CSV_FILE}")
    except Exception as e:
        print(f"   ❌ CSV save error: {e}")

# ============================================
# METHOD 1: RSS SCRAPING (Primary)
# ============================================
def fetch_rss_feed(feed_url: str) -> List[Dict]:
    """Fetch and parse an RSS feed"""
    try:
        print(f"📡 Fetching RSS: {feed_url}")
        feed = feedparser.parse(feed_url)

        if feed.bozo:
            print(f"   ⚠️ Warning: {feed.bozo_exception}")

        entries = feed.entries
        print(f"   ✅ Found {len(entries)} articles")
        return entries

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return []

def extract_from_rss_entry(entry: feedparser.FeedParserDict) -> Dict[str, Any]:
    """Extract clean data from an RSS entry"""
    try:
        title = entry.get('title', '').strip()
        if not title:
            title = "No title available"

        url = entry.get('link', '')
        if not url:
            url = entry.get('guid', '')

        # The Guardian RSS provides FULL CONTENT [citation:9]
        summary = entry.get('description', '')
        if not summary:
            summary = entry.get('summary', '')
        if summary:
            summary = re.sub(r'<[^>]+>', '', summary)
            summary = re.sub(r'\s+', ' ', summary).strip()
        else:
            summary = "No summary available"

        # Extract full content from the feed (The Guardian provides full articles) [citation:9]
        full_content = ""
        if hasattr(entry, 'content'):
            for content in entry.content:
                if content.get('value'):
                    full_content = re.sub(r'<[^>]+>', '', content.value)
                    full_content = re.sub(r'\s+', ' ', full_content).strip()
                    break
        elif hasattr(entry, 'summary'):
            full_content = re.sub(r'<[^>]+>', '', entry.summary)
            full_content = re.sub(r'\s+', ' ', full_content).strip()

        date = None
        date_parsed = None

        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            date_parsed = entry.published_parsed
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            date_parsed = entry.updated_parsed
        elif entry.get('pubDate'):
            date = entry.get('pubDate')
        elif entry.get('updated'):
            date = entry.get('updated')

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

        author = entry.get('author', '')
        if not author and hasattr(entry, 'authors'):
            authors = entry.authors
            if authors and isinstance(authors, list) and len(authors) > 0:
                author = authors[0].get('name', '')

        categories = []
        if hasattr(entry, 'tags') and entry.tags:
            categories = [tag.term for tag in entry.tags if hasattr(tag, 'term')]

        return {
            'title': title,
            'url': url,
            'summary': summary,
            'full_content': full_content if full_content else summary,
            'word_count': len(full_content.split()) if full_content else len(summary.split()),
            'date': date,
            'author': author if author else "The Guardian Staff",
            'categories': categories,
            'source': 'The Guardian (RSS)',
            'scraped_at': datetime.now().isoformat(),
            'scrape_method': 'RSS'
        }

    except Exception as e:
        return {
            'title': 'Error extracting data',
            'url': '',
            'summary': '',
            'date': '',
            'error': str(e)
        }

def scrape_with_rss(feeds: List[str]) -> int:
    """Scrape articles using RSS feeds"""
    global ALL_ARTICLES, SEEN_URLS

    print("\n" + "="*80)
    print("📡 METHOD 1: SCRAPING WITH RSS FEEDS")
    print("="*80)
    print("   ℹ️  The Guardian RSS provides FULL CONTENT [citation:9]")

    count = 0

    for feed_url in feeds:
        if len(ALL_ARTICLES) >= CONFIG['total_articles']:
            break

        entries = fetch_rss_feed(feed_url)

        for entry in entries:
            if len(ALL_ARTICLES) >= CONFIG['total_articles']:
                break

            article = extract_from_rss_entry(entry)

            if article.get('url') and article['url'] not in SEEN_URLS:
                SEEN_URLS.add(article['url'])
                ALL_ARTICLES.append(article)
                count += 1
                print(f"   ✅ {len(ALL_ARTICLES):3d}/{CONFIG['total_articles']} - {article['title'][:50]}...")

                # Save every 10 articles
                if len(ALL_ARTICLES) % 10 == 0:
                    save_incremental()

    print(f"\n📊 RSS Method: Added {count} articles")
    print(f"📊 Current total: {len(ALL_ARTICLES)}/{CONFIG['total_articles']} articles")

    save_incremental()
    return count

# ============================================
# METHOD 2: SELENIUM (Fallback)
# ============================================
def scrape_with_selenium(urls: List[str], total_needed: int) -> int:
    """Scrape with Selenium as fallback"""
    global ALL_ARTICLES, SEEN_URLS

    print("\n" + "="*80)
    print("🔄 METHOD 2: SCRAPING WITH SELENIUM (FALLBACK)")
    print("="*80)
    print(f"   Need {total_needed} more articles")

    if len(ALL_ARTICLES) >= CONFIG['total_articles']:
        print("   Already have enough articles!")
        return 0

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"user-agent={CONFIG['user_agent']}")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = None
    count = 0

    selectors = [
        'article',
        '.fc-item',
        '.fc-item__container',
        '.u-faux-block-link',
        '.js-headline-text',
        '.headline',
        '.story-card',
        '.card',
        'h2 a',
        '.title a',
    ]

    try:
        print("   Launching Chrome...")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        for url in urls:
            if len(ALL_ARTICLES) >= CONFIG['total_articles']:
                break

            try:
                print(f"\n🌐 Loading: {url}")
                driver.get(url)

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "article, .fc-item, .js-headline-text"))
                    )
                except:
                    pass

                time.sleep(3)

                # Scroll to load more
                for scroll in range(3):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                articles = []
                for selector in selectors:
                    found = soup.select(selector)
                    if found and len(found) > len(articles):
                        articles = found

                print(f"   Found {len(articles)} articles on page")

                for article in articles:
                    if len(ALL_ARTICLES) >= CONFIG['total_articles']:
                        break

                    try:
                        title_elem = (
                            article.select_one('h1') or
                            article.select_one('h2') or
                            article.select_one('h3') or
                            article.select_one('.js-headline-text') or
                            article.select_one('.headline') or
                            article.select_one('.title') or
                            article.select_one('a')
                        )

                        title = title_elem.text.strip() if title_elem else "No title"

                        if len(title) < 3:
                            continue

                        link_elem = article.select_one('a')
                        if not link_elem and title_elem and title_elem.name == 'a':
                            link_elem = title_elem
                        elif not link_elem:
                            link_elem = article.find('a')

                        url_link = link_elem.get('href') if link_elem else ""
                        if url_link:
                            if url_link.startswith('/'):
                                url_link = 'https://www.theguardian.com' + url_link
                            elif not url_link.startswith('http'):
                                url_link = 'https://www.theguardian.com/' + url_link

                        if not url_link or url_link in SEEN_URLS:
                            continue

                        summary_elem = (
                            article.select_one('p') or
                            article.select_one('.summary') or
                            article.select_one('.description') or
                            article.select_one('.excerpt')
                        )
                        summary = summary_elem.text.strip() if summary_elem else "No summary available"
                        summary = re.sub(r'\s+', ' ', summary).strip()
                        if len(summary) < 10:
                            summary = "No summary available"

                        date_elem = (
                            article.select_one('time') or
                            article.select_one('.date') or
                            article.select_one('.datetime') or
                            article.select_one('.timestamp')
                        )
                        date = date_elem.get('datetime') if date_elem else ""
                        if not date and date_elem:
                            date = date_elem.text.strip()
                        if not date:
                            date = "No date available"

                        author_elem = article.select_one('.author, .byline')
                        author = author_elem.text.strip() if author_elem else "The Guardian Staff"

                        SEEN_URLS.add(url_link)
                        ALL_ARTICLES.append({
                            'title': title,
                            'url': url_link,
                            'summary': summary,
                            'full_content': "",
                            'word_count': 0,
                            'date': date,
                            'author': author,
                            'categories': ['The Guardian'],
                            'source': 'The Guardian (Selenium)',
                            'scraped_at': datetime.now().isoformat(),
                            'scrape_method': 'Selenium'
                        })
                        count += 1

                        print(f"   ✅ {len(ALL_ARTICLES):3d}/{CONFIG['total_articles']} - {title[:50]}...")

                        if len(ALL_ARTICLES) % 5 == 0:
                            save_incremental()

                    except Exception as e:
                        continue

            except Exception as e:
                print(f"   ❌ Error loading {url}: {str(e)[:100]}")
                continue

        print(f"\n📊 Selenium Total: Added {count} new articles")
        print(f"📊 Current total: {len(ALL_ARTICLES)}/{CONFIG['total_articles']} articles")

        save_incremental()
        return count

    except Exception as e:
        print(f"❌ Selenium error: {e}")
        return count

    finally:
        if driver:
            driver.quit()
            print("🔒 Browser closed")

# ============================================
# METHOD 3: FULL CONTENT EXTRACTION (FALLBACK)
# ============================================
def scrape_full_content(max_articles: int = 30) -> int:
    """Scrape FULL content from article URLs (if RSS didn't provide it)"""
    global ALL_ARTICLES

    print("\n" + "="*80)
    print("📄 METHOD 3: SCRAPING FULL CONTENT")
    print("="*80)
    print("   ℹ️  The Guardian RSS usually provides full content [citation:9]")
    print("   This is a fallback for any missing content")

    articles_to_process = []
    for a in ALL_ARTICLES:
        if not a.get('full_content') and a.get('url'):
            url = a.get('url', '')
            if url:
                articles_to_process.append(a)

    print(f"   Found {len(articles_to_process)} articles without full content")

    if not articles_to_process:
        print("   All articles already have full content from RSS!")
        return 0

    articles_to_process = articles_to_process[:max_articles]

    count = 0
    headers = {
        'User-Agent': CONFIG['user_agent'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    content_selectors = [
        '.article-body',
        '.content__article-body',
        '.js-article__body',
        '.from-content-api',
        '.prose',
        'main article',
        '.story-content',
    ]

    for article in articles_to_process:
        url = article.get('url')
        if not url:
            continue

        try:
            print(f"   📥 Fetching: {url[:80]}...")

            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code != 200:
                print(f"      ⚠️ Status: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            content = None
            for selector in content_selectors:
                content = soup.select_one(selector)
                if content:
                    break

            if content:
                for unwanted in content.select('script, style, .ad, .related, .share, .sidebar, .newsletter'):
                    unwanted.decompose()

                full_text = content.text.strip()
                full_text = re.sub(r'\s+', ' ', full_text).strip()

                if len(full_text) > 200:
                    article['full_content'] = full_text
                    article['word_count'] = len(full_text.split())
                    count += 1
                    print(f"      ✅ {len(full_text)} characters, {len(full_text.split())} words")
                    save_incremental()
                else:
                    print(f"      ⚠️ Too short ({len(full_text)} chars)")
            else:
                print(f"      ❌ No content found")

            time.sleep(0.3)

        except Exception as e:
            print(f"      ❌ Error: {str(e)[:50]}")
            continue

    print(f"\n📊 Full Content: Added {count} full articles")
    return count

# ============================================
# MAIN FUNCTION
# ============================================
def scrape_guardian_complete(total_articles: int = 250) -> Dict[str, Any]:
    """Main function that combines ALL methods"""
    global ALL_ARTICLES, SEEN_URLS

    print("="*80)
    print("📰 THE GUARDIAN COMPLETE SCRAPER - TARGET 250")
    print("="*80)
    print(f"🎯 Target: {total_articles} articles")
    print("="*80)
    print("\n📁 Files will be saved incrementally:")
    print(f"   📄 JSON: {JSON_FILE}")
    print(f"   📄 CSV: {CSV_FILE}")
    print("="*80)
    print("\nStrategy:")
    print("1️⃣ RSS Feeds - Multiple categories (FASTEST + FULL CONTENT) [citation:9]")
    print("2️⃣ Selenium - Fallback for more articles")
    print("3️⃣ Full Content - Fallback for any missing content")
    print("="*80)

    start_time = time.time()
    methods_used = []

    # METHOD 1: RSS Feeds
    print("\n🔍 METHOD 1: Fetching RSS feeds...")
    print("   ℹ️  The Guardian provides FULL ARTICLE CONTENT in RSS [citation:9]")
    rss_count = scrape_with_rss(CONFIG['feeds'])
    if rss_count > 0:
        methods_used.append('RSS')

    # METHOD 2: Selenium (if needed)
    if len(ALL_ARTICLES) < total_articles:
        needed = total_articles - len(ALL_ARTICLES)
        print(f"\n🔄 METHOD 2: Using Selenium to get {needed} more articles...")

        selenium_count = scrape_with_selenium(CONFIG['selenium_urls'], needed)
        if selenium_count > 0:
            methods_used.append('Selenium')

    # METHOD 3: Full Content (fallback for any missing)
    if len(ALL_ARTICLES) > 0:
        print(f"\n📄 METHOD 3: Checking for missing full content...")
        full_count = scrape_full_content(max_articles=30)
        if full_count > 0:
            methods_used.append('Full Content')

    # Final save
    save_incremental()

    # Prepare final output
    result = {
        'metadata': {
            'source': 'The Guardian',
            'total_scraped': len(ALL_ARTICLES),
            'target': total_articles,
            'scraping_duration': round(time.time() - start_time, 2),
            'scraped_at': datetime.now().isoformat(),
            'methods_used': methods_used,
            'has_full_content': any(a.get('full_content') for a in ALL_ARTICLES)
        },
        'articles': ALL_ARTICLES[:total_articles]
    }

    print("\n" + "="*80)
    print("📊 SCRAPING COMPLETE!")
    print("="*80)
    print(f"   ✅ Total Scraped: {len(ALL_ARTICLES)} articles")
    print(f"   📡 Methods Used: {' + '.join(methods_used)}")
    print(f"   📝 Full Content: {'Yes' if result['metadata']['has_full_content'] else 'No'}")
    print(f"   ⏱️  Duration: {result['metadata']['scraping_duration']} seconds")
    print(f"   📁 JSON: {JSON_FILE}")
    print(f"   📁 CSV: {CSV_FILE}")
    print("="*80)

    return result

# ============================================
def display_results(data: Dict):
    """Pretty display scraped data"""
    articles = data.get('articles', [])
    metadata = data.get('metadata', {})

    print("\n" + "="*80)
    print(f"📊 SCRAPED {len(articles)} ARTICLES FROM THE GUARDIAN")
    print("="*80)
    print(f"   ⏱️  Duration: {metadata.get('scraping_duration', 0)} seconds")
    print(f"   📡 Methods: {' + '.join(metadata.get('methods_used', []))}")
    print(f"   📝 Full Content: {'Yes' if metadata.get('has_full_content') else 'No'}")
    print("="*80)

    for i, article in enumerate(articles[:5], 1):
        print(f"\n📌 Article #{i}")
        print(f"📰 TITLE: {article['title']}")
        print(f"📝 SUMMARY: {article['summary'][:150]}..." if len(article['summary']) > 150 else f"📝 SUMMARY: {article['summary']}")
        print(f"📅 DATE: {article['date']}")
        if article.get('author'):
            print(f"✍️  AUTHOR: {article['author']}")
        print(f"📡 SCRAPED WITH: {article.get('scrape_method', 'Unknown')}")
        if article.get('full_content'):
            print(f"📄 FULL CONTENT: {article['full_content'][:200]}..." if len(article['full_content']) > 200 else f"📄 FULL CONTENT: {article['full_content']}")
            print(f"📊 WORD COUNT: {article.get('word_count', 0)}")
        print("-"*80)

# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    print("🚀 STARTING THE GUARDIAN SCRAPER - TARGET 250 ARTICLES")
    print("="*80)
    print("💡 Files are saved EVERY 5-10 articles so you can see progress!")
    print("💡 The Guardian RSS provides FULL CONTENT - no extra scraping needed! [citation:9]")
    print("="*80)

    # Scrape
    scraped_data = scrape_guardian_complete(total_articles=250)

    if scraped_data['articles']:
        display_results(scraped_data)

        print("\n" + "="*80)
        print("✅ SUCCESS!")
        print("="*80)
        print(f"   ✅ Total: {len(scraped_data['articles'])} articles")
        print(f"   📁 JSON: {JSON_FILE}")
        print(f"   📁 CSV: {CSV_FILE}")
        if scraped_data['metadata'].get('has_full_content'):
            print("   📝 Full content extracted from RSS feeds!")
        print("="*80)
    else:
        print("\n❌ No articles scraped. Check your internet connection and URLs.")