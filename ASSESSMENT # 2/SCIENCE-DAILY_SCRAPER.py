"""
SCIENCEDAILY COMPLETE SCRAPER - TARGET 250 ARTICLES
Multi-method approach: RSS (Primary) → Selenium (Fallback) → Playwright (Last Resort)
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
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Try to import Playwright
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright not installed. Run: pip install playwright && playwright install")

# ============================================
# CONFIGURATION
# ============================================
CONFIG = {
    "total_articles": 250,
    # Primary RSS Feeds (Fastest, No Blocking)
    "rss_feeds": [
        "https://www.sciencedaily.com/rss/all.xml",
        "https://www.sciencedaily.com/rss/top.xml",
        "https://www.sciencedaily.com/rss/top/science.xml",
        "https://www.sciencedaily.com/rss/top/health.xml",
        "https://www.sciencedaily.com/rss/top/technology.xml",
        "https://www.sciencedaily.com/rss/top/environment.xml",
        "https://www.sciencedaily.com/rss/top/society.xml",
        "https://www.sciencedaily.com/rss/strange_offbeat.xml",
        "https://www.sciencedaily.com/rss/most_popular.xml",
    ],
    # Selenium Fallback URLs
    "selenium_urls": [
        "https://www.sciencedaily.com/news/",
        "https://www.sciencedaily.com/news/top/",
        "https://www.sciencedaily.com/news/earth_climate/",
        "https://www.sciencedaily.com/news/health_medicine/",
        "https://www.sciencedaily.com/news/mind_brain/",
        "https://www.sciencedaily.com/news/space_time/",
        "https://www.sciencedaily.com/news/matter_energy/",
        "https://www.sciencedaily.com/news/computers_math/",
    ],
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# ============================================
# GLOBAL VARIABLES FOR INCREMENTAL SAVING
# ============================================
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
JSON_FILE = f"sciencedaily_live_{TIMESTAMP}.json"
CSV_FILE = f"sciencedaily_live_{TIMESTAMP}.csv"
ALL_ARTICLES = []
SEEN_URLS = set()

def save_incremental():
    """Save current articles to JSON and CSV incrementally"""
    global ALL_ARTICLES, JSON_FILE, CSV_FILE

    if not ALL_ARTICLES:
        return

    print(f"\n💾 Saving {len(ALL_ARTICLES)} articles...")

    try:
        data = {
            'metadata': {
                'source': 'ScienceDaily',
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
        print(f"   ❌ JSON error: {e}")

    try:
        fieldnames = ['title', 'url', 'summary', 'date', 'source', 'scrape_method']
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
                    'source': article.get('source', 'ScienceDaily'),
                    'scrape_method': article.get('scrape_method', 'RSS')
                }
                if has_full:
                    row['full_content'] = article.get('full_content', '')
                    row['word_count'] = article.get('word_count', 0)
                writer.writerow(row)
        print(f"   ✅ CSV: {CSV_FILE}")
    except Exception as e:
        print(f"   ❌ CSV error: {e}")

# ============================================
# METHOD 1: RSS SCRAPING (Primary - Fastest)
# ============================================
def fetch_rss_feed(feed_url: str) -> List[Dict]:
    """Fetch and parse RSS feed - ScienceDaily RSS is FREE and UNBLOCKED"""
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
    """Extract data from RSS entry"""
    try:
        title = entry.get('title', 'No title').strip()
        url = entry.get('link', '')
        if not url:
            url = entry.get('guid', '')

        # Clean description
        summary = entry.get('description', '')
        if not summary:
            summary = entry.get('summary', '')
        if summary:
            summary = re.sub(r'<[^>]+>', '', summary)
            summary = re.sub(r'\s+', ' ', summary).strip()
        else:
            summary = "No summary available"

        # Get date
        date = "No date"
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                date = datetime(*entry.published_parsed[:6]).isoformat()
            except:
                pass
        elif entry.get('pubDate'):
            date = entry.get('pubDate')

        return {
            'title': title,
            'url': url,
            'summary': summary,
            'date': date,
            'source': 'ScienceDaily',
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

def scrape_with_rss() -> int:
    """Scrape all RSS feeds"""
    global ALL_ARTICLES, SEEN_URLS

    print("\n" + "="*80)
    print("📡 METHOD 1: RSS SCRAPING (PRIMARY)")
    print("="*80)
    print("   ✅ ScienceDaily RSS is FREE and publicly available")
    print("   ✅ No anti-bot protection on RSS feeds")
    print("="*80)

    count = 0

    for feed_url in CONFIG['rss_feeds']:
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

                if len(ALL_ARTICLES) % 10 == 0:
                    save_incremental()

    print(f"\n📊 RSS Method: Added {count} articles")
    print(f"📊 Current total: {len(ALL_ARTICLES)}/{CONFIG['total_articles']} articles")

    save_incremental()
    return count

# ============================================
# METHOD 2: SELENIUM (Fallback)
# ============================================
def scrape_with_selenium(total_needed: int) -> int:
    """Scrape with Selenium as fallback"""
    global ALL_ARTICLES, SEEN_URLS

    print("\n" + "="*80)
    print("🔄 METHOD 2: SELENIUM (FALLBACK)")
    print("="*80)
    print(f"   Need {total_needed} more articles")

    if len(ALL_ARTICLES) >= CONFIG['total_articles']:
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
        'article', '.news-item', '.story', '.featured-story',
        '.headline', 'h2 a', '.title a', '.story-link'
    ]

    try:
        print("   Launching Chrome...")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        driver.set_page_load_timeout(30)

        for url in CONFIG['selenium_urls']:
            if len(ALL_ARTICLES) >= CONFIG['total_articles']:
                break

            try:
                print(f"\n🌐 Loading: {url}")
                driver.get(url)

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "article, .news-item, .story, h2 a"))
                    )
                except TimeoutException:
                    print("   ⚠️ Timeout waiting for content")
                    continue

                time.sleep(2)

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

                print(f"   Found {len(articles)} articles")

                for article in articles:
                    if len(ALL_ARTICLES) >= CONFIG['total_articles']:
                        break

                    try:
                        title_elem = (
                            article.select_one('h1') or article.select_one('h2') or article.select_one('h3') or
                            article.select_one('.headline') or article.select_one('.title') or article.select_one('a')
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
                                url_link = 'https://www.sciencedaily.com' + url_link
                            elif not url_link.startswith('http'):
                                url_link = 'https://www.sciencedaily.com/' + url_link

                        if not url_link or url_link in SEEN_URLS:
                            continue

                        summary_elem = article.select_one('p, .summary, .description, .excerpt')
                        summary = summary_elem.text.strip() if summary_elem else "No summary available"
                        summary = re.sub(r'\s+', ' ', summary).strip()
                        if len(summary) < 10:
                            summary = "No summary available"

                        date_elem = article.select_one('time, .date, .datetime')
                        date = date_elem.get('datetime') if date_elem else ""
                        if not date and date_elem:
                            date = date_elem.text.strip()
                        if not date:
                            date = "No date available"

                        SEEN_URLS.add(url_link)
                        ALL_ARTICLES.append({
                            'title': title,
                            'url': url_link,
                            'summary': summary,
                            'date': date,
                            'source': 'ScienceDaily',
                            'scrape_method': 'Selenium'
                        })
                        count += 1

                        print(f"   ✅ {len(ALL_ARTICLES):3d}/{CONFIG['total_articles']} - {title[:50]}...")

                        if len(ALL_ARTICLES) % 5 == 0:
                            save_incremental()

                    except Exception as e:
                        continue

            except Exception as e:
                print(f"   ❌ Error: {str(e)[:100]}")
                continue

        print(f"\n📊 Selenium: Added {count} articles")
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
# METHOD 3: PLAYWRIGHT (Last Resort)
# ============================================
def scrape_with_playwright(total_needed: int) -> int:
    """Scrape with Playwright (bypasses most anti-bot)"""
    global ALL_ARTICLES, SEEN_URLS

    print("\n" + "="*80)
    print("🔄 METHOD 3: PLAYWRIGHT (LAST RESORT)")
    print("="*80)
    print(f"   Need {total_needed} more articles")

    if not PLAYWRIGHT_AVAILABLE:
        print("   ❌ Playwright not available")
        return 0

    if len(ALL_ARTICLES) >= CONFIG['total_articles']:
        return 0

    count = 0

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                ]
            )
            context = browser.new_context(
                user_agent=CONFIG['user_agent'],
                viewport={'width': 1920, 'height': 1080}
            )
            page = context.new_page()

            for url in CONFIG['selenium_urls']:
                if len(ALL_ARTICLES) >= CONFIG['total_articles']:
                    break

                try:
                    print(f"\n🌐 Loading: {url}")
                    page.goto(url, timeout=30000)
                    page.wait_for_load_state('networkidle', timeout=10000)

                    # Scroll to load more
                    for scroll in range(3):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        page.wait_for_timeout(2000)

                    content = page.content()
                    soup = BeautifulSoup(content, 'html.parser')

                    selectors = ['article', '.news-item', '.story', '.featured-story', '.headline', 'h2 a']
                    articles = []
                    for selector in selectors:
                        found = soup.select(selector)
                        if found and len(found) > len(articles):
                            articles = found

                    print(f"   Found {len(articles)} articles")

                    for article in articles:
                        if len(ALL_ARTICLES) >= CONFIG['total_articles']:
                            break

                        try:
                            title_elem = (
                                article.select_one('h1') or article.select_one('h2') or
                                article.select_one('h3') or article.select_one('.headline') or article.select_one('a')
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
                                    url_link = 'https://www.sciencedaily.com' + url_link
                                elif not url_link.startswith('http'):
                                    url_link = 'https://www.sciencedaily.com/' + url_link

                            if not url_link or url_link in SEEN_URLS:
                                continue

                            summary_elem = article.select_one('p, .summary, .description')
                            summary = summary_elem.text.strip() if summary_elem else "No summary available"

                            SEEN_URLS.add(url_link)
                            ALL_ARTICLES.append({
                                'title': title,
                                'url': url_link,
                                'summary': summary,
                                'date': "No date",
                                'source': 'ScienceDaily',
                                'scrape_method': 'Playwright'
                            })
                            count += 1

                            print(f"   ✅ {len(ALL_ARTICLES):3d}/{CONFIG['total_articles']} - {title[:50]}...")

                            if len(ALL_ARTICLES) % 5 == 0:
                                save_incremental()

                        except Exception as e:
                            continue

                except Exception as e:
                    print(f"   ❌ Error: {str(e)[:100]}")
                    continue

            browser.close()

        print(f"\n📊 Playwright: Added {count} articles")
        save_incremental()
        return count

    except Exception as e:
        print(f"❌ Playwright error: {e}")
        return 0

# ============================================
# METHOD 4: FULL CONTENT EXTRACTION
# ============================================
def scrape_full_content(max_articles: int = 30) -> int:
    """Scrape full content from article URLs"""
    global ALL_ARTICLES

    print("\n" + "="*80)
    print("📄 METHOD 4: FULL CONTENT EXTRACTION")
    print("="*80)

    articles_to_process = [a for a in ALL_ARTICLES if not a.get('full_content') and a.get('url')]
    articles_to_process = articles_to_process[:max_articles]

    print(f"   Processing {len(articles_to_process)} articles...")

    count = 0
    headers = {
        'User-Agent': CONFIG['user_agent'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    content_selectors = ['.article-content', '.story-content', '.content', '.article-body', 'main article', '.text']

    for article in articles_to_process:
        url = article.get('url')
        if not url:
            continue

        try:
            print(f"   📥 {url[:70]}...")

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                content = None
                for selector in content_selectors:
                    content = soup.select_one(selector)
                    if content:
                        break

                if content:
                    for unwanted in content.select('script, style, .ad, .related'):
                        unwanted.decompose()
                    full_text = content.text.strip()
                    full_text = re.sub(r'\s+', ' ', full_text)

                    if len(full_text) > 200:
                        article['full_content'] = full_text
                        article['word_count'] = len(full_text.split())
                        count += 1
                        print(f"      ✅ {len(full_text)} chars, {len(full_text.split())} words")
                    else:
                        print(f"      ⚠️ Too short ({len(full_text)} chars)")
                else:
                    print(f"      ❌ No content found")

            time.sleep(0.3)

        except Exception as e:
            print(f"      ❌ Error: {str(e)[:50]}")

    print(f"\n📊 Added full content to {count} articles")
    save_incremental()
    return count

# ============================================
# MAIN FUNCTION
# ============================================
def scrape_sciencedaily_complete(total_articles: int = 250) -> Dict[str, Any]:
    """Main function with 3-tier fallback chain"""
    global ALL_ARTICLES, SEEN_URLS

    print("="*80)
    print("📰 SCIENCEDAILY COMPLETE SCRAPER - TARGET 250")
    print("="*80)
    print(f"🎯 Target: {total_articles} articles")
    print("="*80)
    print("\nFallback Chain:")
    print("1️⃣ RSS Feeds - FREE, PUBLIC, NO BLOCKING (Fastest)")
    print("2️⃣ Selenium - If RSS doesn't get enough")
    print("3️⃣ Playwright - Last resort for stubborn content")
    print("="*80)

    start_time = time.time()
    methods_used = []

    # METHOD 1: RSS (Primary)
    print("\n🔍 METHOD 1: RSS SCRAPING...")
    print("   ℹ️  ScienceDaily RSS is free and publicly available")
    rss_count = scrape_with_rss()
    if rss_count > 0:
        methods_used.append('RSS')

    # METHOD 2: Selenium (if needed)
    if len(ALL_ARTICLES) < total_articles:
        needed = total_articles - len(ALL_ARTICLES)
        print(f"\n🔄 METHOD 2: SELENIUM FALLBACK...")

        selenium_count = scrape_with_selenium(needed)
        if selenium_count > 0:
            methods_used.append('Selenium')

    # METHOD 3: Playwright (if still needed)
    if len(ALL_ARTICLES) < total_articles:
        needed = total_articles - len(ALL_ARTICLES)
        print(f"\n🔄 METHOD 3: PLAYWRIGHT FALLBACK...")

        playwright_count = scrape_with_playwright(needed)
        if playwright_count > 0:
            methods_used.append('Playwright')

    # METHOD 4: Full Content
    if len(ALL_ARTICLES) > 0:
        print(f"\n📄 METHOD 4: FULL CONTENT...")
        full_count = scrape_full_content(max_articles=30)
        if full_count > 0:
            methods_used.append('Full Content')

    # Final save
    save_incremental()

    result = {
        'metadata': {
            'source': 'ScienceDaily',
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
    print("="*80)

    return result

# ============================================
def display_results(data: Dict):
    """Display results"""
    articles = data.get('articles', [])
    metadata = data.get('metadata', {})

    print("\n" + "="*80)
    print(f"📊 SCRAPED {len(articles)} ARTICLES FROM SCIENCEDAILY")
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
        if article.get('full_content'):
            print(f"📄 FULL CONTENT: {article['full_content'][:200]}...")
        print("-"*80)

# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    print("🚀 STARTING SCIENCEDAILY SCRAPER")
    print("="*80)
    print("💡 Files saved incrementally every 5-10 articles")
    print("💡 RSS feeds are FREE and publicly available")
    print("="*80)

    data = scrape_sciencedaily_complete(total_articles=250)

    if data['articles']:
        display_results(data)
        print("\n" + "="*80)
        print("✅ SUCCESS!")
        print("="*80)
        print(f"   ✅ Total: {len(data['articles'])} articles")
        print(f"   📁 JSON: {JSON_FILE}")
        print(f"   📁 CSV: {CSV_FILE}")
        print("="*80)
    else:
        print("\n❌ No articles scraped. Check your connection.")