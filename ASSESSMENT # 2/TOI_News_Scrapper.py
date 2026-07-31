"""
CNN NEWS SCRAPER - FIXED VERSION
==================================
Resolved all parsing errors using alternative data sources
"""

import requests
import xml.etree.ElementTree as ET
import csv
import json
from datetime import datetime, timedelta
import re
import time
import random
import logging
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ==================== CONFIGURATION ====================

class Config:
    """Configuration settings for the CNN scraper"""

    # Scraping settings
    TARGET_ARTICLES = 150
    DAYS_BACK = 30

    # Request settings
    REQUEST_TIMEOUT = 20
    RETRY_ATTEMPTS = 2
    RETRY_DELAY = 1
    REQUEST_DELAY = 0.5

    # File settings
    CSV_FILENAME = 'cnn_news_articles.csv'
    JSON_FILENAME = 'TOI_News_Scrapper.json'

    # Logging
    LOG_LEVEL = logging.INFO

# ==================== LOGGING ====================

logging.basicConfig(
    level=Config.LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ==================== CNN SCRAPER - FIXED ====================

class CNNNewsScraper:
    """
    Fixed CNN News Scraper - Uses alternative methods when direct RSS fails
    """

    def __init__(self):
        """Initialize the CNN scraper"""
        self.articles = []
        self.session = requests.Session()

        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

        logger.info("CNNNewsScraper initialized")

    # ==================== ALTERNATIVE METHODS ====================

    def fetch_cnn_google_news(self) -> Optional[bytes]:
        """
        Fetch CNN news from Google News RSS (MOST RELIABLE)
        """
        try:
            logger.info("Fetching CNN news from Google News RSS...")

            # Multiple search queries to get more articles
            queries = [
                "cnn",
                "cnn+news",
                "cnn+breaking",
                "cnn+politics",
                "cnn+world",
                "cnn+business"
            ]

            all_content = []

            for query in queries:
                try:
                    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

                    response = self.session.get(
                        url,
                        timeout=Config.REQUEST_TIMEOUT,
                        allow_redirects=True
                    )

                    if response.status_code == 200:
                        logger.info(f"✅ Google News CNN feed fetched (query: {query})")
                        all_content.append(response.content)
                    else:
                        logger.warning(f"Google News CNN failed for {query}")

                    time.sleep(0.3)

                except Exception as e:
                    logger.warning(f"Error with query {query}: {e}")
                    continue

            if all_content:
                logger.info(f"✅ Fetched {len(all_content)} Google News CNN feeds")
                return all_content
            else:
                return None

        except Exception as e:
            logger.error(f"Error fetching Google News CNN: {e}")
            return None

    def fetch_cnn_web_scrape(self) -> List[Dict]:
        """
        Direct web scraping from CNN homepage
        """
        try:
            logger.info("Scraping CNN homepage directly...")

            url = "https://www.cnn.com/"

            response = self.session.get(
                url,
                timeout=Config.REQUEST_TIMEOUT,
                allow_redirects=True
            )

            if response.status_code != 200:
                logger.warning(f"CNN homepage failed: {response.status_code}")
                return []

            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []

            # Find all article links on homepage
            article_selectors = [
                '.container__headline a',
                '.card__headline a',
                '.cd__headline a',
                '.container__title a',
                '.card__title a',
                'a[data-analytics*="article"]',
                '.cd__title a'
            ]

            headlines = []
            for selector in article_selectors:
                try:
                    elements = soup.select(selector)
                    for elem in elements:
                        title = elem.get_text(strip=True)
                        link = elem.get('href')

                        if title and link and len(title) > 20:
                            # Make absolute URL
                            if link.startswith('/'):
                                link = 'https://www.cnn.com' + link

                            headlines.append({
                                'title': title,
                                'link': link
                            })
                except:
                    continue

            # Remove duplicates
            seen_titles = set()
            unique_articles = []
            for article in headlines:
                if article['title'] not in seen_titles:
                    seen_titles.add(article['title'])
                    unique_articles.append(article)

            logger.info(f"✅ Found {len(unique_articles)} articles from CNN homepage")
            return unique_articles[:Config.TARGET_ARTICLES]

        except Exception as e:
            logger.error(f"Error scraping CNN homepage: {e}")
            return []

    def fetch_bbc_alternative(self) -> Optional[bytes]:
        """
        Alternative source: BBC RSS (if CNN fails)
        """
        try:
            logger.info("Fetching from BBC RSS (alternative)...")

            url = "http://feeds.bbci.co.uk/news/rss.xml"

            response = self.session.get(
                url,
                timeout=Config.REQUEST_TIMEOUT,
                allow_redirects=True
            )

            if response.status_code == 200:
                logger.info("✅ BBC RSS fetched successfully")
                return response.content
            else:
                logger.warning(f"BBC RSS failed: {response.status_code}")
                return None

        except Exception as e:
            logger.warning(f"BBC RSS error: {e}")
            return None

    # ==================== PARSING METHODS - FIXED ====================

    def parse_google_news_feed(self, xml_content: bytes, source: str = "Google News") -> int:
        """
        Parse Google News RSS feed - FIXED with proper namespace handling
        """
        try:
            # Register namespaces to handle media: prefix
            ET.register_namespace('media', 'http://search.yahoo.com/mrss/')

            root = ET.fromstring(xml_content)
            items = root.findall('.//item')

            if not items:
                logger.warning(f"No items found in {source} feed")
                return 0

            parsed_count = 0

            for item in items:
                try:
                    # Extract title
                    title_elem = item.find('title')
                    title = title_elem.text if title_elem is not None else 'No Title'
                    title = ' '.join(title.split())

                    # Clean title - remove extra text
                    title = re.sub(r'\s*[-–]\s*(CNN|Breaking|News|Video).*$', '', title)
                    title = title.strip()

                    # Extract link
                    link_elem = item.find('link')
                    link = link_elem.text if link_elem is not None else ''

                    # Extract publication date
                    pub_date_elem = item.find('pubDate')
                    pub_date = pub_date_elem.text if pub_date_elem is not None else ''

                    # Extract description
                    desc_elem = item.find('description')
                    desc = desc_elem.text if desc_elem is not None else ''
                    if desc:
                        desc = re.sub(r'<[^>]+>', '', desc)
                        desc = ' '.join(desc.split())

                    # Extract source
                    source_elem = item.find('source')
                    item_source = source_elem.text if source_elem is not None else 'CNN'

                    # Extract image - FIXED namespace handling
                    image_url = ''
                    try:
                        media_content = item.find('{http://search.yahoo.com/mrss/}content')
                        if media_content is not None:
                            image_url = media_content.get('url', '')
                    except:
                        pass

                    # Try alternative image extraction
                    if not image_url:
                        # Look for img in description
                        if desc_elem is not None and desc_elem.text:
                            img_match = re.search(r'<img[^>]+src="([^"]+)"', desc_elem.text)
                            if img_match:
                                image_url = img_match.group(1)

                    # Parse date
                    try:
                        if pub_date:
                            date_formats = [
                                '%a, %d %b %Y %H:%M:%S %Z',
                                '%a, %d %b %Y %H:%M:%S %z',
                                '%Y-%m-%dT%H:%M:%S%z',
                                '%a, %d %b %Y %H:%M:%S GMT'
                            ]
                            for fmt in date_formats:
                                try:
                                    date_obj = datetime.strptime(pub_date, fmt)
                                    date_str = date_obj.strftime('%Y-%m-%d')
                                    time_str = date_obj.strftime('%H:%M:%S')
                                    datetime_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                                    break
                                except:
                                    continue
                            else:
                                date_str = ''
                                time_str = ''
                                datetime_str = ''
                        else:
                            date_str = ''
                            time_str = ''
                            datetime_str = ''
                    except:
                        date_str = ''
                        time_str = ''
                        datetime_str = ''

                    # Create article
                    article = {
                        'id': len(self.articles) + 1,
                        'title': title,
                        'link': link,
                        'published_date': date_str,
                        'published_time': time_str,
                        'published_datetime': datetime_str,
                        'summary': desc[:500] if desc else '',
                        'source': item_source,
                        'source_feed': source,
                        'image_url': image_url,
                        'full_content': '',
                        'content_fetched': False,
                        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }

                    # Avoid duplicates
                    existing_titles = [a['title'] for a in self.articles]
                    if title not in existing_titles and len(title) > 10:
                        self.articles.append(article)
                        parsed_count += 1

                except Exception as e:
                    logger.debug(f"Error parsing item: {e}")
                    continue

            logger.info(f"Parsed {parsed_count} articles from {source}")
            return parsed_count

        except ET.ParseError as e:
            logger.error(f"XML parsing error: {e}")
            return 0
        except Exception as e:
            logger.error(f"Error parsing feed: {e}")
            return 0

    def parse_web_articles(self, web_articles: List[Dict]) -> int:
        """
        Parse articles scraped from web
        """
        if not web_articles:
            return 0

        parsed_count = 0

        for article_data in web_articles:
            try:
                article = {
                    'id': len(self.articles) + 1,
                    'title': article_data.get('title', 'No Title'),
                    'link': article_data.get('link', ''),
                    'published_date': datetime.now().strftime('%Y-%m-%d'),
                    'published_time': datetime.now().strftime('%H:%M:%S'),
                    'published_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'summary': '',
                    'source': 'CNN',
                    'source_feed': 'CNN Web Scrape',
                    'image_url': '',
                    'full_content': '',
                    'content_fetched': False,
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                # Avoid duplicates
                existing_titles = [a['title'] for a in self.articles]
                if article['title'] not in existing_titles:
                    self.articles.append(article)
                    parsed_count += 1

            except Exception as e:
                logger.debug(f"Error parsing web article: {e}")
                continue

        logger.info(f"Parsed {parsed_count} articles from web scrape")
        return parsed_count

    def fetch_and_parse_all(self) -> int:
        """
        Fetch from all sources and parse
        """
        total_parsed = 0

        # Method 1: Google News CNN
        logger.info("\n📥 Method 1: Google News CNN RSS")
        google_feeds = self.fetch_cnn_google_news()

        if google_feeds:
            if isinstance(google_feeds, list):
                for i, feed in enumerate(google_feeds):
                    parsed = self.parse_google_news_feed(feed, f"Google News {i+1}")
                    total_parsed += parsed
                    if len(self.articles) >= Config.TARGET_ARTICLES:
                        logger.info(f"✅ Reached target of {Config.TARGET_ARTICLES} articles")
                        return total_parsed
            else:
                parsed = self.parse_google_news_feed(google_feeds, "Google News")
                total_parsed += parsed

        # Method 2: Web Scraping
        if len(self.articles) < Config.TARGET_ARTICLES:
            logger.info("\n📥 Method 2: CNN Web Scraping")
            web_articles = self.fetch_cnn_web_scrape()
            if web_articles:
                parsed = self.parse_web_articles(web_articles)
                total_parsed += parsed

        # Method 3: BBC Alternative
        if len(self.articles) < Config.TARGET_ARTICLES:
            logger.info("\n📥 Method 3: BBC RSS (Alternative)")
            bbc_feed = self.fetch_bbc_alternative()
            if bbc_feed:
                parsed = self.parse_google_news_feed(bbc_feed, "BBC News")
                total_parsed += parsed

        return total_parsed

    # ==================== CONTENT FETCHING ====================

    def fetch_article_content_and_image(self, article: Dict) -> tuple:
        """
        Fetch full content and image for a single article
        """
        try:
            link = article.get('link', '')
            if not link or 'news.google.com' in link:
                return article.get('summary', ''), article.get('image_url', '')

            try:
                response = requests.get(
                    link,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                    timeout=15,
                    allow_redirects=True
                )

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Extract image
                    image_url = article.get('image_url', '')
                    if not image_url:
                        for selector in ['meta[property="og:image"]', 'meta[name="twitter:image"]']:
                            meta = soup.select_one(selector)
                            if meta:
                                image_url = meta.get('content', '')
                                if image_url:
                                    break

                        if not image_url:
                            img = soup.select_one('img[data-src*="media.cnn.com"], img[src*="media.cnn.com"]')
                            if img:
                                image_url = img.get('src') or img.get('data-src', '')

                    # Extract content
                    content_parts = []
                    for selector in ['.article__content', '.article-body', '.content', '.story-content']:
                        elements = soup.select(selector)
                        for elem in elements:
                            text = elem.get_text(strip=True)
                            if len(text) > 50:
                                content_parts.append(text)

                    if content_parts:
                        full_content = ' '.join(content_parts)
                        full_content = re.sub(r'\s+', ' ', full_content)
                        return full_content[:5000], image_url

                    # Fallback to paragraphs
                    paragraphs = soup.find_all('p')
                    if paragraphs:
                        text = ' '.join(p.get_text(strip=True) for p in paragraphs[:15])
                        if len(text) > 100:
                            return text[:5000], image_url

                    return article.get('summary', ''), image_url

            except Exception as e:
                logger.debug(f"Content fetch failed: {e}")
                return article.get('summary', ''), article.get('image_url', '')

            return article.get('summary', ''), article.get('image_url', '')

        except Exception as e:
            logger.warning(f"Error fetching content: {e}")
            return article.get('summary', ''), article.get('image_url', '')

    def fetch_all_content(self) -> int:
        """
        Fetch content for all articles
        """
        if not self.articles:
            return 0

        logger.info(f"Fetching content for {len(self.articles)} articles...")
        fetched = 0

        for i, article in enumerate(self.articles, 1):
            try:
                if not article.get('full_content'):
                    content, image = self.fetch_article_content_and_image(article)
                    if content and len(content) > 50:
                        article['full_content'] = content
                        article['content_fetched'] = True
                        fetched += 1
                    if image:
                        article['image_url'] = image

                if i % 10 == 0:
                    logger.info(f"Progress: {i}/{len(self.articles)}")

            except Exception as e:
                logger.warning(f"Error processing article {i}: {e}")

            time.sleep(random.uniform(0.3, 0.7))

        logger.info(f"Fetched content for {fetched}/{len(self.articles)} articles")
        return fetched

    # ==================== SAVE METHODS ====================

    def save_to_csv(self, filename: str = Config.CSV_FILENAME) -> bool:
        """Save articles to CSV"""
        try:
            if not self.articles:
                logger.warning("No articles to save")
                return False

            logger.info(f"Saving {len(self.articles)} articles to {filename}")

            fieldnames = [
                'id', 'title', 'source', 'source_feed',
                'published_date', 'published_time',
                'summary', 'full_content',
                'image_url', 'link', 'scraped_at'
            ]

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for article in self.articles:
                    row = {field: article.get(field, '') for field in fieldnames}
                    if len(row['full_content']) > 1000:
                        row['full_content'] = row['full_content'][:1000] + '...'
                    writer.writerow(row)

            logger.info(f"✅ Saved to {filename}")
            return True

        except Exception as e:
            logger.error(f"Error saving CSV: {e}")
            return False

    def save_to_json(self, filename: str = Config.JSON_FILENAME) -> bool:
        """Save articles to JSON"""
        try:
            if not self.articles:
                logger.warning("No articles to save")
                return False

            logger.info(f"Saving {len(self.articles)} articles to {filename}")

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.articles, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Saved to {filename}")
            return True

        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
            return False

    # ==================== DISPLAY METHODS ====================

    def display_summary(self):
        """Display summary of scraped data"""
        if not self.articles:
            print("\n⚠️ No articles to display")
            return

        print("\n" + "="*80)
        print("📊 CNN NEWS SCRAPING SUMMARY")
        print("="*80)

        print(f"\n📰 Total Articles: {len(self.articles)}")

        # Count by source
        sources = {}
        for article in self.articles:
            source = article.get('source_feed', 'Unknown')
            sources[source] = sources.get(source, 0) + 1

        print(f"📡 Unique Sources: {len(sources)}")

        with_content = len([a for a in self.articles if a.get('content_fetched', False)])
        with_images = len([a for a in self.articles if a.get('image_url')])

        print(f"📖 Full Content: {with_content}/{len(self.articles)}")
        print(f"🖼️  Articles with Images: {with_images}/{len(self.articles)}")

        print("\n📂 Articles by Source:")
        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:10]:
            bar = "█" * int((count / max(sources.values())) * 20) if sources else ""
            print(f"  • {source[:25]:25} : {count:3} articles {bar}")

        print("\n" + "="*80)
        print("📰 SAMPLE ARTICLES (First 3)")
        print("="*80)

        for i, article in enumerate(self.articles[:3], 1):
            print(f"\n{'─'*80}")
            print(f"📌 Article #{i}")
            print(f"{'─'*80}")
            print(f"📰 Title: {article.get('title', 'No Title')[:80]}")
            print(f"📅 Date: {article.get('published_date', 'N/A')} {article.get('published_time', '')}")
            print(f"🏷️  Source: {article.get('source_feed', 'Unknown')}")

            image_url = article.get('image_url', '')
            if image_url:
                print(f"🖼️  Image: {image_url[:60]}...")

            print(f"📝 Summary: {article.get('summary', '')[:150]}...")
            print(f"🔗 Link: {article.get('link', '')[:80]}...")

    # ==================== MAIN RUN METHOD ====================

    def run(self, fetch_content: bool = False) -> List[Dict]:
        """
        Main execution method
        """
        print("\n" + "="*80)
        print("📰 CNN NEWS SCRAPER - FIXED VERSION")
        print("="*80)
        print(f"🎯 Target: {Config.TARGET_ARTICLES} articles")
        print(f"📡 Sources: Google News CNN, CNN Web Scrape, BBC (Alternative)")
        print("="*80)

        # Step 1: Fetch and parse from all sources
        print("\n📥 Fetching from multiple sources...")
        parsed_count = self.fetch_and_parse_all()

        if not self.articles:
            print("\n❌ No articles could be fetched.")
            print("\nTroubleshooting tips:")
            print("1. Check your internet connection")
            print("2. Try using a VPN if Google News is blocked")
            print("3. Wait a few minutes and try again")
            return []

        print(f"\n✅ Found {len(self.articles)} unique articles")

        # Step 2: Fetch full content (optional)
        if fetch_content:
            print("\n📖 Fetching full article content and images...")
            self.fetch_all_content()

        # Step 3: Display summary
        self.display_summary()

        # Step 4: Save data
        print("\n" + "="*80)
        print("💾 Saving data...")
        print("="*80)

        csv_saved = self.save_to_csv()
        json_saved = self.save_to_json()

        # Final report
        print("\n" + "="*80)
        print("✅ SCRAPING COMPLETE!")
        print("="*80)

        if csv_saved:
            print(f"📁 CSV saved: {Config.CSV_FILENAME}")
        if json_saved:
            print(f"📁 JSON saved: {Config.JSON_FILENAME}")

        with_images = len([a for a in self.articles if a.get('image_url')])
        print(f"\n📊 Total: {len(self.articles)} CNN news articles")
        print(f"🖼️  Articles with images: {with_images}/{len(self.articles)}")

        return self.articles

# ==================== MAIN FUNCTION ====================

def main():
    """
    Main function with menu
    """
    print("\n" + "="*80)
    print("📰 CNN NEWS SCRAPER")
    print("="*80)

    print("\nChoose an option:")
    print("1. 📰 Quick Scrape (Articles + Summaries + Images) - Recommended")
    print("2. 📖 Full Scrape (Articles + Full Content + Images)")
    print("3. ❌ Exit")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice == '1':
        scraper = CNNNewsScraper()
        articles = scraper.run(fetch_content=False)

        if articles:
            print(f"\n✅ Successfully scraped {len(articles)} CNN articles!")
        else:
            print("\n⚠️ No articles scraped. Please try again.")

    elif choice == '2':
        scraper = CNNNewsScraper()
        articles = scraper.run(fetch_content=True)

        if articles:
            print(f"\n✅ Successfully scraped {len(articles)} CNN articles with full content!")
        else:
            print("\n⚠️ No articles scraped. Please try again.")

    else:
        print("\nExiting. Goodbye!")

# ==================== RUN ====================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please try again.")