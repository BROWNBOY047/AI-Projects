"""
POLITICO COMPLETE SCRAPER - VERSION 2
Reaches 150 articles using multiple sources:
1. Multiple RSS Feeds (Primary - Working)
2. Different POLITICO sections (URL-based)
3. Selenium with better selectors (Fallback)
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
import os

# ============================================
# CONFIGURATION - EXPANDED FEEDS
# ============================================
CONFIG = {
    "total_articles": 150,
    # MORE RSS FEEDS - including different sections
    "feeds": [
        # Already working feeds
        "http://www.politico.com/rss/playbook.xml",
        "http://www.politico.com/rss/politicopicks.xml",
        "http://www.politico.com/rss/congress.xml",

        # Additional feeds - different topics
        "http://www.politico.com/rss/morningtech.xml",
        "http://www.politico.com/rss/morningagriculture.xml",
        "http://www.politico.com/rss/morningeducation.xml",
        "http://www.politico.com/rss/morningenergy.xml",
        "http://www.politico.com/rss/morninghealthcare.xml",
        "http://www.politico.com/rss/morningshift.xml",
        "http://www.politico.com/rss/morningtransportation.xml",
        "http://www.politico.com/rss/morningtrade.xml",
        "http://www.politico.com/rss/pros.xml",
        "http://www.politico.com/rss/morningcybersecurity.xml",
    ],
    # Direct URLs to scrape (with Selenium)
    "direct_urls": [
        "https://www.politico.com/news",
        "https://www.politico.com/news/politics",
        "https://www.politico.com/news/congress",
        "https://www.politico.com/news/playbook",
        "https://www.politico.com/news/magazine",
        "https://www.politico.com/news/elections",
        "https://www.politico.com/news/national-security",
        "https://www.politico.com/news/energy-and-environment",
        "https://www.politico.com/news/health-care",
        "https://www.politico.com/news/technology",
    ],
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# ============================================
# FUNCTION 1: FETCH RSS FEEDS (MULTIPLE)
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

        summary = entry.get('description', '')
        if not summary:
            summary = entry.get('summary', '')
        if summary:
            summary = re.sub(r'<[^>]+>', '', summary)
            summary = re.sub(r'\s+', ' ', summary).strip()
        else:
            summary = "No summary available"

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
            'date': date,
            'author': author,
            'categories': categories,
            'source': 'POLITICO (RSS)',
            'scraped_at': datetime.now().isoformat(),
            'scrape_method': 'RSS'
        }

    except Exception as e:
        print(f"   ⚠️ Error extracting data: {e}")
        return {
            'title': 'Error extracting data',
            'url': '',
            'summary': '',
            'date': '',
            'error': str(e)
        }

def scrape_all_rss_feeds(feeds: List[str], total_articles: int, existing_urls: set = None) -> List[Dict]:
    """Scrape articles from ALL RSS feeds, avoiding duplicates"""
    print("\n" + "="*80)
    print("📡 SCRAPING ALL RSS FEEDS")
    print("="*80)

    if existing_urls is None:
        existing_urls = set()

    all_articles = []
    seen_urls = existing_urls.copy()

    for feed_url in feeds:
        if len(all_articles) >= total_articles:
            break

        entries = fetch_rss_feed(feed_url)

        for entry in entries:
            if len(all_articles) >= total_articles:
                break

            article = extract_from_rss_entry(entry)

            if article.get('url') and article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                all_articles.append(article)
                print(f"   ✅ {len(all_articles):3d}/{total_articles} - {article['title'][:50]}...")

    print(f"\n📊 RSS Total: {len(all_articles)} new articles")
    return all_articles

# ============================================
# FUNCTION 2: SCRAPE WITH REQUESTS (NO SELENIUM)
# ============================================
def scrape_with_requests(url: str) -> List[Dict]:
    """Scrape articles using requests (lighter than Selenium)"""
    try:
        print(f"🌐 Fetching: {url}")

        headers = {
            'User-Agent': CONFIG['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            print(f"   ❌ Status: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        # Try multiple selectors
        articles = (
            soup.select('article') or
            soup.select('.story-frag') or
            soup.select('.story-item') or
            soup.select('.tease') or
            soup.select('[data-article]') or
            soup.select('.featured-story') or
            soup.select('.headline')
        )

        print(f"   Found {len(articles)} articles")
        scraped = []

        for article in articles[:50]:  # Limit per page
            try:
                # Title
                title_elem = (
                    article.select_one('h1') or
                    article.select_one('h2') or
                    article.select_one('h3') or
                    article.select_one('.headline') or
                    article.select_one('.title') or
                    article.select_one('a')
                )
                title = title_elem.text.strip() if title_elem else "No title"

                # URL
                link_elem = article.select_one('a')
                url_link = link_elem.get('href') if link_elem else ""
                if url_link:
                    if url_link.startswith('/'):
                        url_link = 'https://www.politico.com' + url_link
                    elif not url_link.startswith('http'):
                        url_link = 'https://www.politico.com/' + url_link

                if url_link:
                    scraped.append({
                        'title': title,
                        'url': url_link,
                        'summary': "Scraped via Requests",
                        'date': "No date",
                        'author': "POLITICO Staff",
                        'categories': ['POLITICO'],
                        'source': 'POLITICO (Requests)',
                        'scraped_at': datetime.now().isoformat(),
                        'scrape_method': 'Requests'
                    })

            except Exception as e:
                continue

        return scraped

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return []

def scrape_all_direct_urls(urls: List[str], total_articles: int, existing_urls: set = None) -> List[Dict]:
    """Scrape articles from direct URLs using requests"""
    print("\n" + "="*80)
    print("🌐 SCRAPING DIRECT URLs (WITH REQUESTS)")
    print("="*80)

    if existing_urls is None:
        existing_urls = set()

    all_articles = []
    seen_urls = existing_urls.copy()

    for url in urls:
        if len(all_articles) >= total_articles:
            break

        scraped = scrape_with_requests(url)

        for article in scraped:
            if len(all_articles) >= total_articles:
                break
            if article.get('url') and article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                all_articles.append(article)
                print(f"   ✅ {len(all_articles):3d}/{total_articles} - {article['title'][:50]}...")

    print(f"\n📊 Direct URLs Total: {len(all_articles)} new articles")
    return all_articles

# ============================================
# FUNCTION 3: SELENIUM (FIXED - WITHOUT HEADLESS)
# ============================================
def scrape_with_selenium_fixed(urls: List[str], total_articles: int, existing_urls: set = None) -> List[Dict]:
    """Scrape with Selenium - FIXED version"""
    print("\n" + "="*80)
    print("🔄 SCRAPING WITH SELENIUM (FIXED)")
    print("="*80)
    print("   (Using visible browser to avoid detection)")

    if existing_urls is None:
        existing_urls = set()

    chrome_options = Options()
    # NOT headless - visible browser works better
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(f"user-agent={CONFIG['user_agent']}")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = None
    all_articles = []
    seen_urls = existing_urls.copy()

    try:
        print("   Launching Chrome...")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        for url in urls:
            if len(all_articles) >= total_articles:
                break

            try:
                print(f"\n🌐 Loading: {url}")
                driver.get(url)
                time.sleep(5)  # Wait for page to load

                # Scroll to load more
                for scroll in range(2):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                # Get page source
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Find articles with multiple selectors
                articles = (
                    soup.select('article') or
                    soup.select('.story-frag') or
                    soup.select('.story-item') or
                    soup.select('.tease') or
                    soup.select('[data-article]') or
                    soup.select('.featured-story')
                )

                print(f"   Found {len(articles)} articles")

                for article in articles:
                    if len(all_articles) >= total_articles:
                        break

                    try:
                        # Title
                        title_elem = (
                            article.select_one('h1') or
                            article.select_one('h2') or
                            article.select_one('h3') or
                            article.select_one('.headline') or
                            article.select_one('.title') or
                            article.select_one('a')
                        )
                        title = title_elem.text.strip() if title_elem else "No title"

                        # Summary
                        summary_elem = (
                            article.select_one('p') or
                            article.select_one('.dek') or
                            article.select_one('.summary') or
                            article.select_one('.description')
                        )
                        summary = summary_elem.text.strip() if summary_elem else "No summary"

                        # URL
                        link_elem = article.select_one('a')
                        url_link = link_elem.get('href') if link_elem else ""
                        if url_link:
                            if url_link.startswith('/'):
                                url_link = 'https://www.politico.com' + url_link
                            elif not url_link.startswith('http'):
                                url_link = 'https://www.politico.com/' + url_link

                        # Date
                        date_elem = (
                            article.select_one('time') or
                            article.select_one('.datetime') or
                            article.select_one('.date')
                        )
                        date = date_elem.get('datetime') if date_elem else ""
                        if not date and date_elem:
                            date = date_elem.text.strip()
                        if not date:
                            date = "No date available"

                        if url_link and url_link not in seen_urls:
                            seen_urls.add(url_link)
                            all_articles.append({
                                'title': title,
                                'url': url_link,
                                'summary': summary,
                                'date': date,
                                'author': 'POLITICO Staff',
                                'categories': ['POLITICO'],
                                'source': 'POLITICO (Selenium)',
                                'scraped_at': datetime.now().isoformat(),
                                'scrape_method': 'Selenium'
                            })

                            print(f"   ✅ {len(all_articles):3d}/{total_articles} - {title[:50]}...")

                    except Exception as e:
                        continue

            except Exception as e:
                print(f"   ❌ Error loading {url}: {str(e)[:100]}")
                continue

        print(f"\n📊 Selenium Total: {len(all_articles)} new articles")
        return all_articles

    except Exception as e:
        print(f"❌ Selenium error: {e}")
        return []

    finally:
        if driver:
            driver.quit()
            print("🔒 Browser closed")

# ============================================
# MAIN FUNCTION - COMBINES ALL METHODS
# ============================================
def scrape_politico_complete(total_articles: int = 150) -> Dict[str, Any]:
    """
    Main function that combines ALL methods to reach 150 articles
    """
    print("="*80)
    print("📰 POLITICO COMPLETE SCRAPER V2")
    print("="*80)
    print(f"🎯 Target: {total_articles} articles")
    print("="*80)
    print("\nStrategy:")
    print("1️⃣ RSS Feeds (Multiple topics) - FASTEST")
    print("2️⃣ Direct URLs with Requests - MEDIUM")
    print("3️⃣ Selenium (Visible browser) - RELIABLE")
    print("="*80)

    start_time = time.time()
    all_articles = []
    seen_urls = set()
    methods_used = []

    # METHOD 1: All RSS Feeds
    print("\n🔍 METHOD 1: Fetching ALL RSS feeds...")
    rss_articles = scrape_all_rss_feeds(CONFIG['feeds'], total_articles, seen_urls)

    for article in rss_articles:
        if article['url'] not in seen_urls:
            seen_urls.add(article['url'])
            all_articles.append(article)

    if rss_articles:
        methods_used.append('RSS')

    print(f"\n📊 Current total: {len(all_articles)}/{total_articles} articles")

    # METHOD 2: Direct URLs with Requests (if needed)
    if len(all_articles) < total_articles:
        remaining = total_articles - len(all_articles)
        print(f"\n🔄 METHOD 2: Fetching direct URLs (need {remaining} more)...")

        direct_articles = scrape_all_direct_urls(CONFIG['direct_urls'], remaining, seen_urls)

        for article in direct_articles:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                all_articles.append(article)

        if direct_articles:
            methods_used.append('Requests')

        print(f"\n📊 Current total: {len(all_articles)}/{total_articles} articles")

    # METHOD 3: Selenium (if still needed)
    if len(all_articles) < total_articles:
        remaining = total_articles - len(all_articles)
        print(f"\n🔄 METHOD 3: Using Selenium (need {remaining} more)...")

        selenium_articles = scrape_with_selenium_fixed(CONFIG['direct_urls'], remaining * 2, seen_urls)

        for article in selenium_articles:
            if article['url'] not in seen_urls and len(all_articles) < total_articles:
                seen_urls.add(article['url'])
                all_articles.append(article)

        if selenium_articles:
            methods_used.append('Selenium')

        print(f"\n📊 Current total: {len(all_articles)}/{total_articles} articles")

    # Prepare final output
    result = {
        'metadata': {
            'source': 'POLITICO',
            'total_scraped': len(all_articles),
            'target': total_articles,
            'scraping_duration': round(time.time() - start_time, 2),
            'scraped_at': datetime.now().isoformat(),
            'methods_used': methods_used,
        },
        'articles': all_articles[:total_articles]
    }

    print("\n" + "="*80)
    print("📊 SCRAPING COMPLETE!")
    print("="*80)
    print(f"   ✅ Total Scraped: {len(all_articles)} articles")
    print(f"   📡 Methods Used: {' + '.join(methods_used)}")
    print(f"   ⏱️  Duration: {result['metadata']['scraping_duration']} seconds")
    print("="*80)

    return result

# ============================================
# SAVE FUNCTIONS
# ============================================
def save_to_json(data: Dict, filename_prefix: str = 'politico_complete') -> str:
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

def save_to_csv(data: Dict, filename_prefix: str = 'politico_complete') -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.csv"

    try:
        articles = data.get('articles', [])
        if not articles:
            return ""

        fieldnames = ['title', 'url', 'summary', 'date', 'author', 'categories', 'source', 'scrape_method', 'scraped_at']

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for article in articles:
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
                writer.writerow(row)

        print(f"💾 CSV saved to: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")
        return ""

# ============================================
def display_results(data: Dict):
    articles = data.get('articles', [])
    metadata = data.get('metadata', {})

    print("\n" + "="*80)
    print(f"📊 SCRAPED {len(articles)} ARTICLES FROM POLITICO")
    print("="*80)
    print(f"   ⏱️  Duration: {metadata.get('scraping_duration', 0)} seconds")
    print(f"   📡 Methods: {' + '.join(metadata.get('methods_used', []))}")
    print("="*80)

    for i, article in enumerate(articles[:5], 1):
        print(f"\n📌 Article #{i}")
        print(f"📰 TITLE: {article['title']}")
        print(f"📝 SUMMARY: {article['summary'][:150]}..." if len(article['summary']) > 150 else f"📝 SUMMARY: {article['summary']}")
        print(f"📅 DATE: {article['date']}")
        print(f"📡 SCRAPED WITH: {article.get('scrape_method', 'Unknown')}")
        print("-"*80)

# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    print("🚀 STARTING POLITICO COMPLETE SCRAPER V2")
    print("="*80)

    # Scrape
    scraped_data = scrape_politico_complete(total_articles=150)

    if scraped_data['articles']:
        display_results(scraped_data)

        json_file = save_to_json(scraped_data)
        csv_file = save_to_csv(scraped_data)

        print("\n" + "="*80)
        print("✅ SUCCESS!")
        print("="*80)
        print(f"   ✅ Total: {len(scraped_data['articles'])} articles")
        print(f"   📁 JSON: {json_file}")
        print(f"   📁 CSV: {csv_file}")
        print("="*80)
    else:
        print("❌ No articles scraped")