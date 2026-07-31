"""
TESLA NEWS SCRAPER - DIRECT RSS WITH VPN SUPPORT
=================================================
Optimized for VPN connections with direct RSS feed access
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

# ==================== CONFIGURATION ====================

class Config:
    """Configuration settings for the scraper"""

    # Scraping settings
    TARGET_ARTICLES = 150
    DAYS_BACK = 30

    # Request settings - OPTIMIZED for VPN
    REQUEST_TIMEOUT = 20
    RETRY_ATTEMPTS = 2
    RETRY_DELAY = 1
    REQUEST_DELAY = 0.5

    # File settings
    CSV_FILENAME = 'tesla_news_articles.csv'
    JSON_FILENAME = 'Tesla_News_Scrapper.json'

    # Logging
    LOG_LEVEL = logging.INFO

# ==================== LOGGING ====================

logging.basicConfig(
    level=Config.LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ==================== TESLA SCRAPER ====================

class TeslaNewsScraper:
    """
    Optimized Tesla News Scraper for VPN connections
    """

    def __init__(self):
        """Initialize the scraper"""
        self.articles = []
        self.session = requests.Session()

        # Updated headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

        logger.info("TeslaNewsScraper initialized with VPN support")

    # ==================== DIRECT RSS FEED METHODS ====================

    def fetch_direct_rss_google(self) -> Optional[bytes]:
        """
        Fetch from Google News RSS - DIRECT METHOD
        """
        try:
            logger.info("Fetching from Google News RSS (Direct)...")

            # Simple, clean URL for VPN connections
            url = "https://news.google.com/rss/search?q=tesla&hl=en-US&gl=US&ceid=US:en"

            response = self.session.get(
                url,
                timeout=Config.REQUEST_TIMEOUT,
                allow_redirects=True
            )

            if response.status_code == 200:
                logger.info("✅ Google News RSS fetched successfully")
                return response.content
            else:
                logger.warning(f"Google News RSS failed: {response.status_code}")
                return None

        except Exception as e:
            logger.warning(f"Google News RSS error: {e}")
            return None

    def fetch_direct_rss_feedburner(self) -> Optional[bytes]:
        """
        Fetch from FeedBurner RSS (Alternative source)
        """
        try:
            logger.info("Fetching from FeedBurner RSS...")

            # FeedBurner RSS for Tesla news
            url = "https://feeds.feedburner.com/TeslaNews"

            response = self.session.get(
                url,
                timeout=Config.REQUEST_TIMEOUT,
                allow_redirects=True
            )

            if response.status_code == 200:
                logger.info("✅ FeedBurner RSS fetched successfully")
                return response.content
            else:
                logger.warning(f"FeedBurner RSS failed: {response.status_code}")
                return None

        except Exception as e:
            logger.warning(f"FeedBurner RSS error: {e}")
            return None

    def fetch_direct_rss_teslarati(self) -> Optional[bytes]:
        """
        Fetch from Teslarati RSS (Tesla-specific news)
        """
        try:
            logger.info("Fetching from Teslarati RSS...")

            url = "https://www.teslarati.com/feed/"

            response = self.session.get(
                url,
                timeout=Config.REQUEST_TIMEOUT,
                allow_redirects=True
            )

            if response.status_code == 200:
                logger.info("✅ Teslarati RSS fetched successfully")
                return response.content
            else:
                logger.warning(f"Teslarati RSS failed: {response.status_code}")
                return None

        except Exception as e:
            logger.warning(f"Teslarati RSS error: {e}")
            return None

    def fetch_direct_rss_electrek(self) -> Optional[bytes]:
        """
        Fetch from Electrek RSS (EV-focused news)
        """
        try:
            logger.info("Fetching from Electrek RSS...")

            url = "https://electrek.co/feed/"

            response = self.session.get(
                url,
                timeout=Config.REQUEST_TIMEOUT,
                allow_redirects=True
            )

            if response.status_code == 200:
                logger.info("✅ Electrek RSS fetched successfully")
                return response.content
            else:
                logger.warning(f"Electrek RSS failed: {response.status_code}")
                return None

        except Exception as e:
            logger.warning(f"Electrek RSS error: {e}")
            return None

    def fetch_direct_rss_insideevs(self) -> Optional[bytes]:
        """
        Fetch from InsideEVs RSS (EV news)
        """
        try:
            logger.info("Fetching from InsideEVs RSS...")

            url = "https://insideevs.com/rss/tesla/"

            response = self.session.get(
                url,
                timeout=Config.REQUEST_TIMEOUT,
                allow_redirects=True
            )

            if response.status_code == 200:
                logger.info("✅ InsideEVs RSS fetched successfully")
                return response.content
            else:
                logger.warning(f"InsideEVs RSS failed: {response.status_code}")
                return None

        except Exception as e:
            logger.warning(f"InsideEVs RSS error: {e}")
            return None

    def fetch_direct_rss_cleantechnica(self) -> Optional[bytes]:
        """
        Fetch from CleanTechnica RSS (Clean energy news)
        """
        try:
            logger.info("Fetching from CleanTechnica RSS...")

            url = "https://cleantechnica.com/feed/?post_type=post&category_name=tesla"

            response = self.session.get(
                url,
                timeout=Config.REQUEST_TIMEOUT,
                allow_redirects=True
            )

            if response.status_code == 200:
                logger.info("✅ CleanTechnica RSS fetched successfully")
                return response.content
            else:
                logger.warning(f"CleanTechnica RSS failed: {response.status_code}")
                return None

        except Exception as e:
            logger.warning(f"CleanTechnica RSS error: {e}")
            return None

    def fetch_all_feeds(self) -> List[bytes]:
        """
        Fetch from all available RSS feeds
        """
        feeds = []

        # List of all RSS feed methods
        feed_methods = [
            self.fetch_direct_rss_google,
            self.fetch_direct_rss_feedburner,
            self.fetch_direct_rss_teslarati,
            self.fetch_direct_rss_electrek,
            self.fetch_direct_rss_insideevs,
            self.fetch_direct_rss_cleantechnica,
        ]

        for method in feed_methods:
            try:
                content = method()
                if content:
                    feeds.append(content)
                time.sleep(0.5)  # Small delay between requests
            except Exception as e:
                logger.warning(f"Feed method failed: {e}")
                continue

        logger.info(f"Fetched {len(feeds)} feeds successfully")
        return feeds

    # ==================== PARSING METHODS ====================

    def parse_rss_feed(self, xml_content: bytes, source: str = "Unknown") -> int:
        """
        Parse RSS feed and extract articles
        """
        try:
            root = ET.fromstring(xml_content)

            # Find items in the feed
            items = root.findall('.//item')
            if not items:
                items = root.findall('.//entry')

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

                    # Extract link
                    link_elem = item.find('link')
                    link = link_elem.text if link_elem is not None else ''

                    # Extract publication date
                    pub_date_elem = item.find('pubDate')
                    pub_date = pub_date_elem.text if pub_date_elem is not None else ''

                    # Extract description/summary
                    desc_elem = item.find('description')
                    desc = desc_elem.text if desc_elem is not None else ''
                    if desc:
                        desc = re.sub(r'<[^>]+>', '', desc)
                        desc = ' '.join(desc.split())

                    # Extract source
                    source_elem = item.find('source')
                    item_source = source_elem.text if source_elem is not None else source

                    # Parse date
                    try:
                        if pub_date:
                            # Try different date formats
                            for fmt in ['%a, %d %b %Y %H:%M:%S %Z', '%a, %d %b %Y %H:%M:%S %z', '%Y-%m-%dT%H:%M:%S%z']:
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

                    # Create article dictionary
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
                        'full_content': '',
                        'content_fetched': False,
                        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }

                    # Avoid duplicates (check by title)
                    existing_titles = [a['title'] for a in self.articles]
                    if title not in existing_titles:
                        self.articles.append(article)
                        parsed_count += 1

                except Exception as e:
                    logger.warning(f"Error parsing item in {source}: {e}")
                    continue

            logger.info(f"Parsed {parsed_count} new articles from {source}")
            return parsed_count

        except ET.ParseError as e:
            logger.error(f"XML parsing error in {source}: {e}")
            return 0
        except Exception as e:
            logger.error(f"Error parsing {source} feed: {e}")
            return 0

    def parse_all_feeds(self, feeds: List[bytes]) -> int:
        """
        Parse all fetched feeds
        """
        total_parsed = 0
        feed_names = ['Google News', 'FeedBurner', 'Teslarati', 'Electrek', 'InsideEVs', 'CleanTechnica']

        for i, feed_content in enumerate(feeds):
            source_name = feed_names[i] if i < len(feed_names) else f'Feed_{i}'
            parsed = self.parse_rss_feed(feed_content, source_name)
            total_parsed += parsed

            # Stop if we have enough articles
            if len(self.articles) >= Config.TARGET_ARTICLES:
                logger.info(f"Reached target of {Config.TARGET_ARTICLES} articles")
                break

        logger.info(f"Total parsed: {total_parsed} articles")
        return total_parsed

    # ==================== CONTENT FETCHING ====================

    def fetch_article_content(self, article: Dict) -> str:
        """
        Fetch full content for a single article
        """
        try:
            link = article.get('link', '')

            if not link:
                return article.get('summary', '')

            # Skip if it's a Google News link (redirect)
            if 'news.google.com' in link:
                return article.get('summary', '')

            try:
                response = requests.get(
                    link,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                    timeout=10,
                    allow_redirects=True
                )

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Try to extract content
                    content_selectors = [
                        'article', '.content', '.article-content',
                        '.post-content', 'main', '.entry-content'
                    ]

                    content_parts = []

                    for selector in content_selectors:
                        try:
                            elements = soup.select(selector)
                            for elem in elements:
                                text = elem.get_text(strip=True)
                                if len(text) > 100:
                                    content_parts.append(text)
                        except:
                            continue

                    if content_parts:
                        return ' '.join(content_parts)[:5000]

                    # Fallback to paragraphs
                    paragraphs = soup.find_all('p')
                    if paragraphs:
                        text = ' '.join(p.get_text(strip=True) for p in paragraphs[:15])
                        if len(text) > 100:
                            return text[:5000]

                    return article.get('summary', '')

            except Exception as e:
                logger.debug(f"Content fetch failed: {e}")
                return article.get('summary', '')

            return article.get('summary', '')

        except Exception as e:
            logger.warning(f"Error fetching content: {e}")
            return article.get('summary', '')

    def fetch_all_content(self) -> int:
        """
        Fetch content for all articles
        """
        if not self.articles:
            return 0

        logger.info(f"Fetching content for {len(self.articles)} articles...")

        fetched = 0
        total = len(self.articles)

        for i, article in enumerate(self.articles, 1):
            try:
                # Only fetch if we don't have content yet
                if not article.get('full_content'):
                    content = self.fetch_article_content(article)
                    if content and len(content) > 50:
                        article['full_content'] = content
                        article['content_fetched'] = True
                        fetched += 1

                if i % 10 == 0:
                    logger.info(f"Progress: {i}/{total}")

            except Exception as e:
                logger.warning(f"Error processing article {i}: {e}")

            time.sleep(random.uniform(0.3, 0.7))

        logger.info(f"Fetched content for {fetched}/{total} articles")
        return fetched

    # ==================== SAVE METHODS ====================

    def save_to_csv(self, filename: str = Config.CSV_FILENAME) -> bool:
        """
        Save articles to CSV
        """
        try:
            if not self.articles:
                logger.warning("No articles to save")
                return False

            logger.info(f"Saving {len(self.articles)} articles to {filename}")

            fieldnames = ['id', 'title', 'source', 'source_feed', 'published_date',
                         'published_time', 'summary', 'full_content', 'link', 'scraped_at']

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
        """
        Save articles to JSON
        """
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
        """
        Display summary of scraped data
        """
        if not self.articles:
            print("\n⚠️ No articles to display")
            return

        print("\n" + "="*80)
        print("📊 TESLA NEWS SCRAPING SUMMARY")
        print("="*80)

        print(f"\n📰 Total Articles: {len(self.articles)}")

        # Count by source
        sources = {}
        for article in self.articles:
            source = article.get('source_feed', 'Unknown')
            sources[source] = sources.get(source, 0) + 1

        print(f"📡 Unique Sources: {len(sources)}")

        # Articles with content
        with_content = len([a for a in self.articles if a.get('content_fetched', False)])
        print(f"📖 Full Content: {with_content}/{len(self.articles)}")

        # Show source breakdown
        print("\n📂 Articles by Source:")
        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int((count / max(sources.values())) * 20)
            print(f"  • {source[:25]:25} : {count:3} articles {bar}")

        # Show sample articles
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
            print(f"📝 Summary: {article.get('summary', '')[:150]}...")
            print(f"🔗 Link: {article.get('link', '')[:80]}...")

    # ==================== MAIN RUN METHOD ====================

    def run(self, fetch_content: bool = False) -> List[Dict]:
        """
        Main execution method
        """
        print("\n" + "="*80)
        print("🚗 TESLA NEWS SCRAPER - VPN OPTIMIZED")
        print("="*80)
        print(f"🎯 Target: {Config.TARGET_ARTICLES} articles")
        print(f"📡 Sources: Google News, FeedBurner, Teslarati, Electrek, InsideEVs, CleanTechnica")
        print("="*80)

        # Step 1: Fetch all RSS feeds
        print("\n📥 Fetching from multiple RSS feeds...")
        feeds = self.fetch_all_feeds()

        if not feeds:
            print("\n❌ No feeds could be fetched. Please check:")
            print("1. Your VPN connection is active")
            print("2. You have internet access")
            print("3. The RSS URLs are accessible")
            return []

        print(f"\n✅ Fetched {len(feeds)} RSS feeds")

        # Step 2: Parse all feeds
        print("\n🔍 Parsing articles from feeds...")
        parsed_count = self.parse_all_feeds(feeds)

        if not self.articles:
            print("\n❌ No articles could be parsed.")
            return []

        print(f"\n✅ Found {len(self.articles)} unique articles")

        # Step 3: Fetch full content (optional)
        if fetch_content:
            print("\n📖 Fetching full article content...")
            self.fetch_all_content()

        # Step 4: Display summary
        self.display_summary()

        # Step 5: Save data
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

        print(f"\n📊 Total: {len(self.articles)} Tesla news articles")
        print(f"📡 From: {len(feeds)} different RSS feeds")

        return self.articles

# ==================== MAIN FUNCTION ====================

def main():
    """
    Main function with menu
    """
    print("\n" + "="*80)
    print("🚗 TESLA NEWS SCRAPER - VPN OPTIMIZED")
    print("="*80)

    print("\nChoose an option:")
    print("1. 📰 Quick Scrape (Articles + Summaries) - Recommended")
    print("2. 📖 Full Scrape (Articles + Full Content) - Takes longer")
    print("3. ❌ Exit")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice == '1':
        scraper = TeslaNewsScraper()
        articles = scraper.run(fetch_content=False)

        if articles:
            print(f"\n✅ Successfully scraped {len(articles)} articles with summaries!")
        else:
            print("\n⚠️ No articles scraped. Please try again.")

    elif choice == '2':
        scraper = TeslaNewsScraper()
        articles = scraper.run(fetch_content=True)

        if articles:
            print(f"\n✅ Successfully scraped {len(articles)} articles with full content!")
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