"""
BLOOMBERG NEWS SCRAPER - LATEST 10 (MINIMAL)
=============================================
Best approach with minimal code (250 lines)
Uses Google News RSS as primary method with fallbacks
"""

import requests
import xml.etree.ElementTree as ET
import csv
import json
from datetime import datetime, timedelta
import re
import time
import logging
from typing import List, Dict, Optional
from bs4 import BeautifulSoup

# ==================== CONFIG ====================

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


class Config:
    TARGET = 10
    TIMEOUT = 20
    CSV_FILE = 'bloomberg_latest_news_Data.csv'
    JSON_FILE = 'bloomberg_latest_10.json'


# ==================== MAIN SCRAPER ====================

class BloombergScraper:
    """Minimal Bloomberg scraper - latest 10 articles"""

    def __init__(self):
        self.articles = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.bloomberg.com/',
        })

    def scrape(self, fetch_full=False) -> List[Dict]:
        """Main scraping method"""
        print("\n" + "=" * 60)
        print("📰 BLOOMBERG - LATEST 10 NEWS")
        print("=" * 60)

        # Try methods in order of reliability
        methods = [
            self._google_news_rss,
            self._bloomberg_rss,
            self._web_scrape,
            self._json_api
        ]

        for method in methods:
            if len(self.articles) >= Config.TARGET:
                break
            method()

        # Fetch full content if requested
        if fetch_full and self.articles:
            self._fetch_full_content()

        # Save and display
        self._save_data()
        self._display()

        return self.articles

    # ========== METHOD 1: GOOGLE NEWS RSS (BEST) ==========

    def _google_news_rss(self):
        """Fetch from Google News RSS - Most reliable"""
        try:
            logger.info("📌 Google News RSS...")
            url = "https://news.google.com/rss/search?q=bloomberg&hl=en-US&gl=US&ceid=US:en"

            resp = self.session.get(url, timeout=Config.TIMEOUT)
            if resp.status_code != 200:
                return

            root = ET.fromstring(resp.content)
            items = root.findall('.//item')[:Config.TARGET]

            for item in items:
                title = self._clean(item.find('title').text if item.find('title') is not None else '')
                link = item.find('link').text if item.find('link') is not None else ''
                pub = item.find('pubDate').text if item.find('pubDate') is not None else ''
                desc = self._clean(item.find('description').text if item.find('description') is not None else '')

                # Extract image
                image = ''
                media = item.find('{http://search.yahoo.com/mrss/}content')
                if media is not None:
                    image = media.get('url', '')

                date = self._parse_date(pub)

                self.articles.append({
                    'title': title,
                    'link': link,
                    'published_date': date['date'],
                    'published_time': date['time'],
                    'summary': desc[:300],
                    'image_url': image,
                    'source': 'Bloomberg',
                    'source_feed': 'Google News RSS',
                    'full_content': '',
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })

            logger.info(f"  ✅ Found {len(self.articles)} articles")

        except Exception as e:
            logger.warning(f"  ⚠️ Failed: {e}")

    # ========== METHOD 2: DIRECT BLOOMBERG RSS ==========

    def _bloomberg_rss(self):
        """Direct Bloomberg RSS feeds"""
        try:
            logger.info("📌 Direct Bloomberg RSS...")

            rss_urls = [
                "https://www.bloomberg.com/feed/news",
                "https://www.bloomberg.com/feed/markets",
                "https://www.bloomberg.com/feed/technology",
                "https://www.bloomberg.com/feed/politics"
            ]

            for rss_url in rss_urls:
                if len(self.articles) >= Config.TARGET:
                    break

                try:
                    resp = self.session.get(rss_url, timeout=Config.TIMEOUT)
                    if resp.status_code != 200:
                        continue

                    root = ET.fromstring(resp.content)
                    items = root.findall('.//item')[:Config.TARGET]

                    for item in items:
                        title = self._clean(item.find('title').text if item.find('title') is not None else '')
                        link = item.find('link').text if item.find('link') is not None else ''
                        pub = item.find('pubDate').text if item.find('pubDate') is not None else ''
                        desc = self._clean(
                            item.find('description').text if item.find('description') is not None else '')

                        # Image from enclosure
                        image = ''
                        enc = item.find('enclosure')
                        if enc is not None:
                            image = enc.get('url', '')

                        date = self._parse_date(pub)

                        # Avoid duplicates
                        if not any(a['title'] == title for a in self.articles):
                            self.articles.append({
                                'title': title,
                                'link': link,
                                'published_date': date['date'],
                                'published_time': date['time'],
                                'summary': desc[:300],
                                'image_url': image,
                                'source': 'Bloomberg',
                                'source_feed': 'Bloomberg RSS',
                                'full_content': '',
                                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })

                    logger.info(f"  ✅ Found {len(self.articles)} articles")

                except Exception as e:
                    continue

        except Exception as e:
            logger.warning(f"  ⚠️ Failed: {e}")

    # ========== METHOD 3: WEB SCRAPING ==========

    def _web_scrape(self):
        """Direct web scraping from Bloomberg homepage"""
        try:
            logger.info("📌 Web Scraping...")
            url = "https://www.bloomberg.com/"

            resp = self.session.get(url, timeout=Config.TIMEOUT)
            if resp.status_code != 200:
                return

            soup = BeautifulSoup(resp.content, 'html.parser')

            # Bloomberg article selectors
            selectors = [
                'a[data-component="headline"]',
                '.story-package__headline a',
                '.feature-story__headline a',
                '.article-card__headline a',
                '.story-card__headline a',
                'h2 a',
                'h3 a'
            ]

            for selector in selectors:
                elements = soup.select(selector)
                for elem in elements[:Config.TARGET]:
                    title = elem.get_text(strip=True)
                    link = elem.get('href')

                    if title and link and len(title) > 15:
                        if link.startswith('/'):
                            link = 'https://www.bloomberg.com' + link
                        elif not link.startswith('http'):
                            continue

                        # Skip video/audio links
                        if '/video/' in link or '/audio/' in link:
                            continue

                        if not any(a['link'] == link for a in self.articles):
                            self.articles.append({
                                'title': title,
                                'link': link,
                                'published_date': datetime.now().strftime('%Y-%m-%d'),
                                'published_time': datetime.now().strftime('%H:%M:%S'),
                                'summary': '',
                                'image_url': '',
                                'source': 'Bloomberg',
                                'source_feed': 'Web Scrape',
                                'full_content': '',
                                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })

                if len(self.articles) >= Config.TARGET:
                    break

            logger.info(f"  ✅ Found {len(self.articles)} articles")

        except Exception as e:
            logger.warning(f"  ⚠️ Failed: {e}")

    # ========== METHOD 4: JSON API ==========

    def _json_api(self):
        """Try to find Bloomberg API/JSON endpoint"""
        try:
            logger.info("📌 JSON API...")

            api_urls = [
                "https://www.bloomberg.com/api/v2/stories?limit=10",
                "https://www.bloomberg.com/feed/api/v1/stories",
                "https://www.bloomberg.com/featured-stories?format=json"
            ]

            for api_url in api_urls:
                if len(self.articles) >= Config.TARGET:
                    break

                try:
                    resp = self.session.get(api_url, timeout=Config.TIMEOUT)
                    if resp.status_code != 200:
                        continue

                    data = resp.json()

                    # Try different JSON structures
                    stories = []
                    if 'stories' in data:
                        stories = data['stories']
                    elif 'data' in data and 'stories' in data['data']:
                        stories = data['data']['stories']
                    elif 'items' in data:
                        stories = data['items']

                    for story in stories[:Config.TARGET]:
                        title = story.get('title') or story.get('headline') or ''
                        link = story.get('url') or story.get('canonical_url') or story.get('permalink') or ''

                        if title and link:
                            if not link.startswith('http'):
                                link = 'https://www.bloomberg.com' + link

                            if not any(a['link'] == link for a in self.articles):
                                self.articles.append({
                                    'title': title,
                                    'link': link,
                                    'published_date': datetime.now().strftime('%Y-%m-%d'),
                                    'published_time': datetime.now().strftime('%H:%M:%S'),
                                    'summary': '',
                                    'image_url': '',
                                    'source': 'Bloomberg',
                                    'source_feed': 'JSON API',
                                    'full_content': '',
                                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                })

                    logger.info(f"  ✅ Found {len(self.articles)} articles")

                except:
                    continue

        except Exception as e:
            logger.warning(f"  ⚠️ Failed: {e}")

    # ========== HELPER METHODS ==========

    def _clean(self, text):
        """Clean text"""
        if not text:
            return ''
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _parse_date(self, date_str):
        """Parse date string"""
        result = {'date': '', 'time': ''}
        if not date_str:
            return result

        try:
            formats = [
                '%a, %d %b %Y %H:%M:%S %Z',
                '%a, %d %b %Y %H:%M:%S %z',
                '%Y-%m-%dT%H:%M:%S%z',
                '%a, %d %b %Y %H:%M:%S GMT'
            ]
            for fmt in formats:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    result['date'] = dt.strftime('%Y-%m-%d')
                    result['time'] = dt.strftime('%H:%M:%S')
                    break
                except:
                    continue
        except:
            pass
        return result

    def _parse_relative_time(self, time_str):
        """Parse relative time like '7 min ago' to actual datetime"""
        try:
            now = datetime.now()
            time_str = time_str.lower()

            if 'min' in time_str:
                minutes = int(re.search(r'(\d+)', time_str).group(1))
                dt = now - timedelta(minutes=minutes)
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif 'hour' in time_str or 'hr' in time_str:
                hours = int(re.search(r'(\d+)', time_str).group(1))
                dt = now - timedelta(hours=hours)
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif 'day' in time_str:
                days = int(re.search(r'(\d+)', time_str).group(1))
                dt = now - timedelta(days=days)
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif 'just now' in time_str or 'now' in time_str:
                return now.strftime('%Y-%m-%d %H:%M:%S')

            return time_str

        except:
            return time_str

    def _fetch_full_content(self):
        """Fetch full article content"""
        logger.info("\n📖 Fetching full content...")

        for i, article in enumerate(self.articles, 1):
            try:
                link = article.get('link')
                if not link or 'news.google.com' in link:
                    continue

                # Bloomberg specific headers
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Referer': 'https://www.bloomberg.com/',
                }

                resp = requests.get(link, timeout=15, headers=headers)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.content, 'html.parser')

                    # Extract content - Bloomberg specific selectors
                    content_parts = []
                    selectors = [
                        '.article-body__content',
                        '.body-content',
                        '.article-content',
                        '[data-component="article-body"]',
                        '.content-well',
                        '.story-content',
                        '.article-body'
                    ]

                    for selector in selectors:
                        for elem in soup.select(selector):
                            text = elem.get_text(strip=True)
                            if len(text) > 50:
                                content_parts.append(text)

                    if content_parts:
                        article['full_content'] = ' '.join(content_parts)[:3000]
                    else:
                        # Fallback to paragraphs
                        paragraphs = soup.find_all('p')
                        if paragraphs:
                            text = ' '.join(p.get_text(strip=True) for p in paragraphs[:15])
                            if len(text) > 100:
                                article['full_content'] = text[:3000]

                    # Try to get image if missing
                    if not article.get('image_url'):
                        for selector in ['meta[property="og:image"]', 'meta[name="twitter:image"]']:
                            meta = soup.select_one(selector)
                            if meta:
                                article['image_url'] = meta.get('content', '')
                                break

                logger.info(f"  Progress: {i}/{len(self.articles)}")
                time.sleep(0.5)

            except Exception as e:
                logger.warning(f"  ⚠️ Failed article {i}: {e}")

    def _save_data(self):
        """Save to CSV and JSON"""
        if not self.articles:
            return

        # CSV
        try:
            fields = ['id', 'title', 'published_date', 'published_time', 'summary',
                      'full_content', 'image_url', 'link', 'source_feed', 'scraped_at']

            with open(Config.CSV_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                for i, art in enumerate(self.articles, 1):
                    art['id'] = i
                    row = {k: art.get(k, '') for k in fields}
                    if len(row['full_content']) > 500:
                        row['full_content'] = row['full_content'][:500] + '...'
                    writer.writerow(row)
            logger.info(f"💾 Saved: {Config.CSV_FILE}")
        except Exception as e:
            logger.error(f"CSV error: {e}")

        # JSON
        try:
            with open(Config.JSON_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.articles, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 Saved: {Config.JSON_FILE}")
        except Exception as e:
            logger.error(f"JSON error: {e}")

    def _display(self):
        """Display results"""
        if not self.articles:
            print("\n❌ No articles found")
            return

        print("\n" + "=" * 60)
        print(f"📊 LATEST {len(self.articles)} BLOOMBERG ARTICLES")
        print("=" * 60)

        for i, art in enumerate(self.articles, 1):
            print(f"\n{i}. {art.get('title', 'No Title')}")
            print(f"   📅 {art.get('published_date', 'N/A')} {art.get('published_time', '')}")
            print(f"   🏷️  {art.get('source_feed', 'Unknown')}")
            if art.get('image_url'):
                print(f"   🖼️  Image available")
            if art.get('summary'):
                print(f"   📝 {art.get('summary', '')[:100]}...")
            print(f"   🔗 {art.get('link', '')[:60]}...")


# ==================== RUN ====================

def main():
    print("\n" + "=" * 60)
    print("📰 BLOOMBERG SCRAPER - LATEST 10")
    print("=" * 60)
    print("\n1. Quick (Headlines + Summaries)")
    print("2. Full (With Full Content)")

    choice = input("\nChoice (1-2): ").strip()

    scraper = BloombergScraper()
    articles = scraper.scrape(fetch_full=(choice == '2'))

    if articles:
        print(f"\n✅ Done! {len(articles)} articles saved.")
        print(f"📁 Files: {Config.CSV_FILE}, {Config.JSON_FILE}")
    else:
        print("\n⚠️ Try again or check internet.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Stopped by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")