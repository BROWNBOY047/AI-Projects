"""
ULTIMATE 20-SOURCE SCRAPER - ALL ISSUES RESOLVED
20 Sources, 150 Articles Each
6-Method Fallback Chain
"""

import feedparser
import requests
import json
import csv
import time
import re
import os
import gc
import random
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Try cloudscraper
try:
    import cloudscraper
    CLOUDSCRAPER_AVAILABLE = True
except ImportError:
    CLOUDSCRAPER_AVAILABLE = False

# Try Playwright
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# =========================================================
# CONSTANTS
# =========================================================
ARTICLES_PER_SOURCE = 150
TIMEFRAME_YEARS = 2
BATCH_SAVE_INTERVAL = 25
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30
SELENIUM_TIMEOUT = 60
PLAYWRIGHT_TIMEOUT = 60000
DELAY_BETWEEN_REQUESTS = 0.3
MAX_WORKERS = 3

# =========================================================
# USER AGENT ROTATION
# =========================================================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

# =========================================================
# 20 SOURCES WITH MULTIPLE RSS QUERIES
# =========================================================
SOURCES = {
    # Original 10 Sources (with extra queries for problematic ones)
    "physorg": {
        "google_rss": "https://news.google.com/rss/search?q=phys.org&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=physics&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://phys.org/rss-feed/",
        "url": "https://phys.org/",
        "category": "Science"
    },
    "sciencedaily": {
        "google_rss": "https://news.google.com/rss/search?q=sciencedaily&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=science+daily&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://www.sciencedaily.com/rss/all.xml",
        "url": "https://www.sciencedaily.com/",
        "category": "Science"
    },
    "medicalxpress": {
        "google_rss": "https://news.google.com/rss/search?q=medicalxpress&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=medical+news&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://medicalxpress.com/rss-feed/",
        "url": "https://medicalxpress.com/",
        "category": "Health"
    },
    "earthsky": {
        "google_rss": "https://news.google.com/rss/search?q=earthsky&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=astronomy+news&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://earthsky.org/feed/",
        "url": "https://earthsky.org/",
        "category": "Science"
    },
    "betanews": {
        "google_rss": "https://news.google.com/rss/search?q=betanews&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=beta+news&hl=en-US&gl=US&ceid=US:en",
        "google_rss3": "https://news.google.com/rss/search?q=technology+news&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://betanews.com/feed/",
        "url": "https://betanews.com/",
        "category": "Technology"
    },
    "maritime_executive": {
        "google_rss": "https://news.google.com/rss/search?q=maritime-executive&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=maritime+executive&hl=en-US&gl=US&ceid=US:en",
        "google_rss3": "https://news.google.com/rss/search?q=shipping+news&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://maritime-executive.com/feed",
        "url": "https://maritime-executive.com/",
        "category": "Maritime"
    },
    "cleantechnica": {
        "google_rss": "https://news.google.com/rss/search?q=cleantechnica&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=clean+technica&hl=en-US&gl=US&ceid=US:en",
        "google_rss3": "https://news.google.com/rss/search?q=renewable+energy&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://cleantechnica.com/feed/",
        "url": "https://cleantechnica.com/",
        "category": "Clean Energy"
    },
    "linuxtoday": {
        "google_rss": "https://news.google.com/rss/search?q=linuxtoday&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=linux+today&hl=en-US&gl=US&ceid=US:en",
        "google_rss3": "https://news.google.com/rss/search?q=linux+news&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://www.linuxtoday.com/feed/",
        "url": "https://www.linuxtoday.com/",
        "category": "Technology"
    },
    "renewable_energy": {
        "google_rss": "https://news.google.com/rss/search?q=renewable+energy+magazine&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=renewable+energy&hl=en-US&gl=US&ceid=US:en",
        "google_rss3": "https://news.google.com/rss/search?q=green+energy&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://www.renewableenergymagazine.com/feed",
        "url": "https://www.renewableenergymagazine.com/",
        "category": "Energy"
    },
    "techxplore": {
        "google_rss": "https://news.google.com/rss/search?q=techxplore&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=tech+xplore&hl=en-US&gl=US&ceid=US:en",
        "google_rss3": "https://news.google.com/rss/search?q=technology+news&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://techxplore.com/rss-feed/",
        "url": "https://techxplore.com/",
        "category": "Technology"
    },
    # New 10 Sources
    "interesting_engineering": {
        "google_rss": "https://news.google.com/rss/search?q=interesting+engineering&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=engineering+news&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://interestingengineering.com/feed",
        "url": "https://interestingengineering.com/",
        "category": "Engineering"
    },
    "the_conversation": {
        "google_rss": "https://news.google.com/rss/search?q=the+conversation&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=conversation+news&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://theconversation.com/us/feed",
        "url": "https://theconversation.com/us",
        "category": "Academic"
    },
    "techrepublic": {
        "google_rss": "https://news.google.com/rss/search?q=techrepublic&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=tech+republic&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://www.techrepublic.com/rss.xml",
        "url": "https://www.techrepublic.com/",
        "category": "Technology"
    },
    "techspot": {
        "google_rss": "https://news.google.com/rss/search?q=techspot&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=tech+spot&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://www.techspot.com/rss/",
        "url": "https://www.techspot.com/",
        "category": "Technology"
    },
    "fossbytes": {
        "google_rss": "https://news.google.com/rss/search?q=fossbytes&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=foss+bytes&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://fossbytes.com/feed/",
        "url": "https://fossbytes.com/",
        "category": "Technology"
    },
    "geeky_gadgets": {
        "google_rss": "https://news.google.com/rss/search?q=geeky+gadgets&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=gadgets+news&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://www.geeky-gadgets.com/feed/",
        "url": "https://www.geeky-gadgets.com/",
        "category": "Technology"
    },
    "electronics_weekly": {
        "google_rss": "https://news.google.com/rss/search?q=electronics+weekly&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=electronics+news&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://www.electronicsweekly.com/feed/",
        "url": "https://www.electronicsweekly.com/",
        "category": "Electronics"
    },
    "open_access_government": {
        "google_rss": "https://news.google.com/rss/search?q=open+access+government&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=government+news&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://www.openaccessgovernment.org/feed/",
        "url": "https://www.openaccessgovernment.org/",
        "category": "Government"
    },
    "bioengineer": {
        "google_rss": "https://news.google.com/rss/search?q=bioengineer.org&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=bioengineering+news&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://bioengineer.org/feed/",
        "url": "https://bioengineer.org/",
        "category": "Science"
    },
    "scitechdaily": {
        "google_rss": "https://news.google.com/rss/search?q=scitechdaily&hl=en-US&gl=US&ceid=US:en",
        "google_rss2": "https://news.google.com/rss/search?q=science+daily&hl=en-US&gl=US&ceid=US:en",
        "direct_rss": "https://scitechdaily.com/feed/",
        "url": "https://scitechdaily.com/",
        "category": "Science"
    }
}

# =========================================================
# STORAGE CLASS
# =========================================================
class ArticleStorage:
    def __init__(self):
        self.articles = {}
        self.seen_urls = set()
        self.seen_titles = set()
        self.save_counter = 0
        self.lock = threading.Lock()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.json_file = f"ultimate_20_sources_{self.timestamp}.json"
        self.csv_file = f"ultimate_20_sources_{self.timestamp}.csv"
        self.checkpoint_file = "ultimate_20_checkpoint.json"
        self._load_checkpoint()

    def _load_checkpoint(self):
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r') as f:
                    data = json.load(f)
                    self.articles = data.get('articles', {})
                    self.seen_urls = set(data.get('seen_urls', []))
                    self.seen_titles = set(data.get('seen_titles', []))
                    self.save_counter = data.get('save_counter', 0)
                print(f"✅ Loaded checkpoint: {self.get_total()} articles")
            except:
                pass

    def _save_checkpoint(self):
        try:
            with open(self.checkpoint_file, 'w') as f:
                json.dump({
                    'articles': self.articles,
                    'seen_urls': list(self.seen_urls),
                    'seen_titles': list(self.seen_titles),
                    'save_counter': self.save_counter
                }, f, indent=2)
        except:
            pass

    def add_article(self, source: str, article: Dict) -> bool:
        with self.lock:
            url = article.get('url', '')
            title = article.get('title', '')

            if url and url in self.seen_urls:
                return False
            if title and len(title) > 10 and title in self.seen_titles:
                return False

            if source not in self.articles:
                self.articles[source] = []

            if 'summary' in article and len(article['summary']) > 500:
                article['summary'] = article['summary'][:500] + '...'

            self.articles[source].append(article)
            self.seen_urls.add(url)
            self.seen_titles.add(title)
            self.save_counter += 1

            if self.save_counter % BATCH_SAVE_INTERVAL == 0:
                self._save_data()
                self._save_checkpoint()
                gc.collect()

            return True

    def _save_data(self):
        flat = []
        for source, articles in self.articles.items():
            for a in articles:
                a['source'] = a.get('source', source)
                flat.append(a)

        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'total': len(flat),
                    'sources': list(self.articles.keys()),
                    'last_update': datetime.now().isoformat()
                },
                'articles': flat
            }, f, ensure_ascii=False, indent=2)

        if flat:
            fields = ['title', 'url', 'summary', 'date', 'author', 'source', 'category', 'method']
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                for a in flat:
                    writer.writerow({
                        'title': a.get('title', ''),
                        'url': a.get('url', ''),
                        'summary': a.get('summary', ''),
                        'date': a.get('date', ''),
                        'author': a.get('author', 'Unknown'),
                        'source': a.get('source', ''),
                        'category': a.get('category', ''),
                        'method': a.get('method', 'Unknown')
                    })

        print(f"\n💾 Saved: {len(flat)} articles")

    def get_total(self) -> int:
        with self.lock:
            return sum(len(a) for a in self.articles.values())

    def get_remaining(self, source: str) -> int:
        with self.lock:
            current = len(self.articles.get(source, []))
            return max(0, ARTICLES_PER_SOURCE - current)

    def is_complete(self, source: str) -> bool:
        return self.get_remaining(source) <= 0

# =========================================================
# UTILITY FUNCTIONS
# =========================================================
def clean_text(text: str, max_len: int = 500) -> str:
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_len] if len(text) > max_len else text

def is_within_timeframe(date_str: str) -> bool:
    if not date_str or date_str == "No date":
        return True
    try:
        date_str = date_str.replace(' 00:00:00', '').replace(' 00:00', '')
        for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S',
                    '%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S %Z']:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt >= datetime.now() - timedelta(days=TIMEFRAME_YEARS * 365)
            except:
                continue
    except:
        pass
    return True

def extract_date(entry) -> str:
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        try:
            return datetime(*entry.published_parsed[:6]).isoformat()
        except:
            pass
    return entry.get('pubDate', entry.get('updated', 'No date'))

def fetch_rss(feed_url: str) -> List:
    for attempt in range(MAX_RETRIES):
        try:
            feed = feedparser.parse(feed_url, agent=get_random_user_agent())
            if feed.entries:
                return feed.entries
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
        except:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
    return []

def fetch_google_rss_multi(config: Dict) -> List:
    all_entries = []
    seen_urls = set()

    for key, value in config.items():
        if key.startswith('google_rss') and value:
            entries = fetch_rss(value)
            for entry in entries:
                url = entry.get('link', '')
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    all_entries.append(entry)
    return all_entries

# =========================================================
# METHOD 1: CLOUDSCRAPER
# =========================================================
def scrape_cloudscraper(source_name: str, config: Dict, storage: ArticleStorage) -> int:
    print(f"\n   ☁️ Cloudscraper: {source_name}")

    if not CLOUDSCRAPER_AVAILABLE:
        return 0

    url = config.get('url', '')
    if not url:
        return 0

    count = 0

    try:
        scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
        )

        headers = {'User-Agent': get_random_user_agent()}
        response = scraper.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

        if response.status_code != 200:
            return 0

        soup = BeautifulSoup(response.text, 'html.parser')
        selectors = ['article', '.post', '.entry', '.story', '.story-card', '.news-item', '.card', 'h2 a', '.teaser']
        elements = []
        for selector in selectors:
            found = soup.select(selector)
            if found and len(found) > len(elements):
                elements = found

        if not elements:
            return 0

        for el in elements:
            if storage.is_complete(source_name):
                break

            try:
                t_el = el.select_one('h1, h2, h3, .title, .headline, a')
                title = clean_text(t_el.text) if t_el else ""
                if not title or len(title) < 5:
                    continue

                l_el = el.select_one('a') or el.find('a')
                url_link = l_el.get('href') if l_el else ""
                if url_link and url_link.startswith('/'):
                    base = url.split('/')[0] + '//' + url.split('/')[2]
                    url_link = base + url_link
                elif url_link and not url_link.startswith('http'):
                    base = url.split('/')[0] + '//' + url.split('/')[2]
                    url_link = base + '/' + url_link.lstrip('/')

                if not url_link:
                    continue

                s_el = el.select_one('p, .summary, .description, .excerpt')
                summary = clean_text(s_el.text) if s_el else "No summary"

                d_el = el.select_one('time, .date, .datetime')
                date = d_el.get('datetime') if d_el else ""
                if not date and d_el:
                    date = clean_text(d_el.text)
                if not date:
                    date = "No date"

                if not is_within_timeframe(date):
                    continue

                article = {
                    'title': title,
                    'url': url_link,
                    'summary': summary,
                    'date': date,
                    'author': "Unknown",
                    'category': config.get('category', 'General'),
                    'method': 'Cloudscraper'
                }

                if storage.add_article(source_name, article):
                    count += 1
                    print(f"      ✅ {count}/{ARTICLES_PER_SOURCE} - {title[:40]}...")
                    time.sleep(DELAY_BETWEEN_REQUESTS)

            except Exception:
                continue

    except Exception:
        pass

    print(f"      📊 Cloudscraper: {count} articles")
    return count

# =========================================================
# METHOD 2: BEAUTIFULSOUP
# =========================================================
def scrape_bs4(source_name: str, config: Dict, storage: ArticleStorage) -> int:
    print(f"\n   🔍 BS4: {source_name}")

    url = config.get('url', '')
    if not url:
        return 0

    count = 0

    try:
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

        if response.status_code != 200:
            return 0

        soup = BeautifulSoup(response.text, 'html.parser')
        selectors = ['article', '.post', '.entry', '.story', '.story-card', '.news-item', '.card', 'h2 a']
        elements = []
        for selector in selectors:
            found = soup.select(selector)
            if found and len(found) > len(elements):
                elements = found

        if not elements:
            return 0

        for el in elements:
            if storage.is_complete(source_name):
                break

            try:
                t_el = el.select_one('h1, h2, h3, .title, .headline, a')
                title = clean_text(t_el.text) if t_el else ""
                if not title or len(title) < 5:
                    continue

                l_el = el.select_one('a') or el.find('a')
                url_link = l_el.get('href') if l_el else ""
                if url_link and url_link.startswith('/'):
                    base = url.split('/')[0] + '//' + url.split('/')[2]
                    url_link = base + url_link
                elif url_link and not url_link.startswith('http'):
                    base = url.split('/')[0] + '//' + url.split('/')[2]
                    url_link = base + '/' + url_link.lstrip('/')

                if not url_link:
                    continue

                s_el = el.select_one('p, .summary, .description, .excerpt')
                summary = clean_text(s_el.text) if s_el else "No summary"

                d_el = el.select_one('time, .date, .datetime')
                date = d_el.get('datetime') if d_el else ""
                if not date and d_el:
                    date = clean_text(d_el.text)
                if not date:
                    date = "No date"

                if not is_within_timeframe(date):
                    continue

                article = {
                    'title': title,
                    'url': url_link,
                    'summary': summary,
                    'date': date,
                    'author': "Unknown",
                    'category': config.get('category', 'General'),
                    'method': 'BS4'
                }

                if storage.add_article(source_name, article):
                    count += 1
                    print(f"      ✅ {count}/{ARTICLES_PER_SOURCE} - {title[:40]}...")
                    time.sleep(DELAY_BETWEEN_REQUESTS)

            except Exception:
                continue

    except Exception:
        pass

    print(f"      📊 BS4: {count} articles")
    return count

# =========================================================
# METHOD 3: DIRECT RSS
# =========================================================
def scrape_direct_rss(source_name: str, config: Dict, storage: ArticleStorage) -> int:
    print(f"\n   📡 Direct RSS: {source_name}")

    feed_url = config.get('direct_rss')
    if not feed_url:
        return 0

    count = 0
    entries = fetch_rss(feed_url)

    if not entries:
        return 0

    for entry in entries:
        if storage.is_complete(source_name):
            break

        title = clean_text(entry.get('title', ''))
        if not title or len(title) < 5:
            continue

        url = entry.get('link', '') or entry.get('guid', '')
        if not url:
            continue

        summary = clean_text(entry.get('description', '') or entry.get('summary', ''))
        if not summary or len(summary) < 10:
            summary = "No summary available"

        date = extract_date(entry)
        if not is_within_timeframe(date):
            continue

        author = entry.get('author', 'Unknown')
        if hasattr(entry, 'authors') and entry.authors:
            author = entry.authors[0].get('name', 'Unknown')

        article = {
            'title': title,
            'url': url,
            'summary': summary,
            'date': date,
            'author': author,
            'category': config.get('category', 'General'),
            'method': 'Direct RSS'
        }

        if storage.add_article(source_name, article):
            count += 1
            print(f"      ✅ {count}/{ARTICLES_PER_SOURCE} - {title[:40]}...")
            time.sleep(DELAY_BETWEEN_REQUESTS)

    print(f"      📊 Direct RSS: {count} articles")
    return count

# =========================================================
# METHOD 4: GOOGLE RSS
# =========================================================
def scrape_google_rss(source_name: str, config: Dict, storage: ArticleStorage) -> int:
    print(f"\n   📡 Google RSS: {source_name}")

    entries = fetch_google_rss_multi(config)

    if not entries:
        return 0

    count = 0
    for entry in entries:
        if storage.is_complete(source_name):
            break

        title = clean_text(entry.get('title', ''))
        if not title or len(title) < 5:
            continue

        url = entry.get('link', '')
        if not url:
            continue

        summary = clean_text(entry.get('description', ''))
        if not summary or len(summary) < 10:
            summary = "No summary available"

        date = extract_date(entry)
        if not is_within_timeframe(date):
            continue

        article = {
            'title': title,
            'url': url,
            'summary': summary,
            'date': date,
            'author': "Unknown",
            'category': config.get('category', 'General'),
            'method': 'Google RSS'
        }

        if storage.add_article(source_name, article):
            count += 1
            print(f"      ✅ {count}/{ARTICLES_PER_SOURCE} - {title[:40]}...")
            time.sleep(DELAY_BETWEEN_REQUESTS)

    print(f"      📊 Google RSS: {count} articles")
    return count

# =========================================================
# METHOD 5: SELENIUM STEALTH
# =========================================================
def create_selenium_stealth_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-web-security")
    options.add_argument(f"user-agent={get_random_user_agent()}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(SELENIUM_TIMEOUT)

        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                window.chrome = { runtime: {} };
            '''
        })

        return driver
    except Exception:
        return None

def scrape_selenium_stealth(source_name: str, config: Dict, storage: ArticleStorage) -> int:
    print(f"\n   🌐 Selenium Stealth: {source_name}")

    if storage.is_complete(source_name):
        return 0

    url = config.get('url', '')
    if not url:
        return 0

    driver = create_selenium_stealth_driver()
    if not driver:
        return 0

    count = 0

    try:
        print(f"      Loading: {url}")
        driver.get(url)
        time.sleep(random.uniform(4, 6))

        selectors = ['article', '.post', '.entry', '.story', '.story-card', '.news-item', '.card', 'h2 a', '.teaser']
        content_found = False
        for selector in selectors:
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                content_found = True
                break
            except TimeoutException:
                continue

        if not content_found:
            driver.quit()
            return 0

        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        elements = []
        for selector in selectors:
            found = soup.select(selector)
            if found and len(found) > len(elements):
                elements = found

        if not elements:
            driver.quit()
            return 0

        for el in elements:
            if storage.is_complete(source_name):
                break

            try:
                t_el = el.select_one('h1, h2, h3, .title, .headline, a')
                title = clean_text(t_el.text) if t_el else ""
                if not title or len(title) < 5:
                    continue

                l_el = el.select_one('a') or el.find('a')
                url_link = l_el.get('href') if l_el else ""
                if url_link and url_link.startswith('/'):
                    base = url.split('/')[0] + '//' + url.split('/')[2]
                    url_link = base + url_link
                elif url_link and not url_link.startswith('http'):
                    base = url.split('/')[0] + '//' + url.split('/')[2]
                    url_link = base + '/' + url_link.lstrip('/')

                if not url_link:
                    continue

                s_el = el.select_one('p, .summary, .description, .excerpt')
                summary = clean_text(s_el.text) if s_el else "No summary"

                d_el = el.select_one('time, .date, .datetime')
                date = d_el.get('datetime') if d_el else ""
                if not date and d_el:
                    date = clean_text(d_el.text)
                if not date:
                    date = "No date"

                if not is_within_timeframe(date):
                    continue

                a_el = el.select_one('.author, .byline, .credit')
                author = clean_text(a_el.text) if a_el else "Unknown"

                article = {
                    'title': title,
                    'url': url_link,
                    'summary': summary,
                    'date': date,
                    'author': author,
                    'category': config.get('category', 'General'),
                    'method': 'Selenium Stealth'
                }

                if storage.add_article(source_name, article):
                    count += 1
                    print(f"      ✅ {count}/{ARTICLES_PER_SOURCE} - {title[:40]}...")
                    time.sleep(DELAY_BETWEEN_REQUESTS)

            except Exception:
                continue

    except Exception:
        pass

    finally:
        driver.quit()

    print(f"      📊 Selenium Stealth: {count} articles")
    return count

# =========================================================
# METHOD 6: PLAYWRIGHT STEALTH
# =========================================================
def scrape_playwright_stealth(source_name: str, config: Dict, storage: ArticleStorage) -> int:
    if not PLAYWRIGHT_AVAILABLE:
        return 0

    print(f"\n   🛡️ Playwright Stealth: {source_name}")

    if storage.is_complete(source_name):
        return 0

    url = config.get('url', '')
    if not url:
        return 0

    count = 0

    for attempt in range(2):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
                )

                context = browser.new_context(
                    user_agent=get_random_user_agent(),
                    viewport={'width': 1920, 'height': 1080},
                    locale='en-US',
                    timezone_id='America/New_York'
                )

                page = context.new_page()

                page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                    window.chrome = { runtime: {} };
                """)

                print(f"      Loading: {url}")

                try:
                    page.goto(url, timeout=PLAYWRIGHT_TIMEOUT)
                    page.wait_for_load_state('networkidle', timeout=20000)
                except Exception:
                    browser.close()
                    continue

                for _ in range(5):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(1500)

                content = page.content()
                soup = BeautifulSoup(content, 'html.parser')

                selectors = ['article', '.post', '.entry', '.story', '.story-card', '.news-item', '.card', 'h2 a', '.teaser']
                elements = []
                for selector in selectors:
                    found = soup.select(selector)
                    if found and len(found) > len(elements):
                        elements = found

                if not elements:
                    print("      ⚠️ No articles found")
                    browser.close()
                    continue

                for el in elements:
                    if storage.is_complete(source_name):
                        break

                    try:
                        t_el = el.select_one('h1, h2, h3, .title, .headline, a')
                        title = clean_text(t_el.text) if t_el else ""
                        if not title or len(title) < 5:
                            continue

                        l_el = el.select_one('a') or el.find('a')
                        url_link = l_el.get('href') if l_el else ""
                        if url_link and url_link.startswith('/'):
                            base = url.split('/')[0] + '//' + url.split('/')[2]
                            url_link = base + url_link
                        elif url_link and not url_link.startswith('http'):
                            base = url.split('/')[0] + '//' + url.split('/')[2]
                            url_link = base + '/' + url_link.lstrip('/')

                        if not url_link:
                            continue

                        s_el = el.select_one('p, .summary, .description, .excerpt')
                        summary = clean_text(s_el.text) if s_el else "No summary"

                        d_el = el.select_one('time, .date, .datetime')
                        date = d_el.get('datetime') if d_el else ""
                        if not date and d_el:
                            date = clean_text(d_el.text)
                        if not date:
                            date = "No date"

                        if not is_within_timeframe(date):
                            continue

                        a_el = el.select_one('.author, .byline, .credit')
                        author = clean_text(a_el.text) if a_el else "Unknown"

                        article = {
                            'title': title,
                            'url': url_link,
                            'summary': summary,
                            'date': date,
                            'author': author,
                            'category': config.get('category', 'General'),
                            'method': 'Playwright Stealth'
                        }

                        if storage.add_article(source_name, article):
                            count += 1
                            print(f"      ✅ {count}/{ARTICLES_PER_SOURCE} - {title[:40]}...")
                            time.sleep(DELAY_BETWEEN_REQUESTS)

                    except Exception:
                        continue

                browser.close()
                break

        except Exception:
            if attempt == 0:
                time.sleep(3)

    print(f"      📊 Playwright Stealth: {count} articles")
    return count

# =========================================================
# SOURCE SCRAPER - ONE SOURCE AT A TIME
# =========================================================
def scrape_source(source_name: str, config: Dict, storage: ArticleStorage) -> int:
    print("\n" + "="*80)
    print(f"📰 {source_name.upper()}")
    print("="*80)

    methods = [
        ("Cloudscraper", scrape_cloudscraper),
        ("BS4", scrape_bs4),
        ("Direct RSS", scrape_direct_rss),
        ("Google RSS", scrape_google_rss),
        ("Selenium Stealth", scrape_selenium_stealth),
        ("Playwright Stealth", scrape_playwright_stealth),
    ]

    for method_name, method_func in methods:
        if storage.is_complete(source_name):
            print(f"\n   ✅ Already completed {ARTICLES_PER_SOURCE} articles!")
            break

        print(f"\n   🔄 Trying {method_name}...")
        method_func(source_name, config, storage)

        if storage.is_complete(source_name):
            print(f"\n   ✅ Reached {ARTICLES_PER_SOURCE} articles using {method_name}!")
            break

    count = len(storage.articles.get(source_name, []))
    print(f"\n📊 {source_name}: {count}/{ARTICLES_PER_SOURCE} articles")
    return count

# =========================================================
# MAIN FUNCTION
# =========================================================
def main():
    print("="*80)
    print("🚀 ULTIMATE 20-SOURCE SCRAPER")
    print("="*80)
    print(f"📌 Sources: {len(SOURCES)}")
    print(f"📌 Target: {ARTICLES_PER_SOURCE} per source")
    print(f"📌 Total: {len(SOURCES) * ARTICLES_PER_SOURCE} articles")
    print("="*80)
    print("\n6-Method Fallback Chain per source:")
    print("1️⃣ Cloudscraper (Bypasses Cloudflare)")
    print("2️⃣ BeautifulSoup (Direct HTML)")
    print("3️⃣ Direct RSS (Feedparser)")
    print("4️⃣ Google RSS (Google News)")
    print("5️⃣ Selenium Stealth (Headless + Stealth)")
    print("6️⃣ Playwright Stealth (Best Anti-Detection)")
    print("="*80)

    storage = ArticleStorage()
    start_time = time.time()

    print("\n🚀 Processing ONE source at a time with all 6 methods...\n")

    for source_name, config in SOURCES.items():
        try:
            count = scrape_source(source_name, config, storage)
            print(f"\n✅ Completed: {source_name} - {count} articles")
        except Exception as e:
            print(f"\n❌ Failed: {source_name} - {str(e)[:100]}")

    elapsed = round(time.time() - start_time, 2)
    total = storage.get_total()

    print("\n" + "="*80)
    print("📊 SCRAPING COMPLETE!")
    print("="*80)
    print(f"   ✅ Total: {total} articles")
    print(f"   ⏱️  Duration: {elapsed} seconds")
    print(f"   📁 JSON: {storage.json_file}")
    print(f"   📁 CSV: {storage.csv_file}")
    print("="*80)

    print("\n📊 Per Source Summary:")
    for source_name in SOURCES:
        count = len(storage.articles.get(source_name, []))
        methods = [a.get('method', 'Unknown') for a in storage.articles.get(source_name, [])]
        method_counts = {}
        for m in methods:
            method_counts[m] = method_counts.get(m, 0) + 1
        method_str = ', '.join([f"{m}:{c}" for m, c in method_counts.items()]) if method_counts else "None"
        status = "✅" if count >= ARTICLES_PER_SOURCE else f"⚠️ {count}/{ARTICLES_PER_SOURCE}"
        print(f"   {status} {source_name}: {count} articles ({method_str})")

if __name__ == "__main__":
    main()