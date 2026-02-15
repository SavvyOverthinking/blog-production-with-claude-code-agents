"""
Blog scraper for voice extraction
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

class BlogScraper:
    """Scrape articles from a blog for voice analysis"""

    def __init__(self, base_url: str, max_articles: int = 10):
        self.base_url = base_url
        self.max_articles = max_articles

    def scrape(self):
        """Scrape articles and return list of article dictionaries"""
        article_urls = self._discover_articles()

        if not article_urls:
            return []

        articles = []
        for i, url in enumerate(article_urls[:self.max_articles], 1):
            print(f"  [{i}/{min(len(article_urls), self.max_articles)}] {url[:60]}...")
            article = self._scrape_article(url)
            if article:
                articles.append(article)
            time.sleep(0.5)  # Be polite to servers

        return articles

    def _discover_articles(self):
        """Find article URLs on the blog"""
        # Try HTML scraping first
        urls = self._discover_from_html()

        # If no URLs found, try RSS feed as fallback
        if not urls:
            print("  No links found in HTML, trying RSS feed...")
            urls = self._discover_from_rss()

        return urls[:self.max_articles * 2]

    def _discover_from_rss(self):
        """Try to find articles via RSS feed"""
        parsed = urlparse(self.base_url)
        feed_urls = [
            urljoin(self.base_url, '/feed'),
            urljoin(self.base_url, '/rss'),
            urljoin(self.base_url, '/feed.xml'),
            urljoin(self.base_url, '/rss.xml'),
            urljoin(self.base_url, '/atom.xml'),
        ]

        for feed_url in feed_urls:
            try:
                response = requests.get(feed_url, headers=HEADERS, timeout=10)
                if response.status_code == 200 and ('<rss' in response.text[:500] or '<feed' in response.text[:500] or '<item>' in response.text[:2000]):
                    soup = BeautifulSoup(response.content, 'xml')
                    urls = []
                    for item in soup.find_all('item'):
                        link = item.find('link')
                        if link:
                            url = link.get_text().strip()
                            if url:
                                urls.append(url)
                    if urls:
                        print(f"  Found {len(urls)} articles via RSS feed")
                        return urls
            except Exception:
                continue

        return []

    def _discover_from_html(self):
        """Find article URLs by scraping HTML links"""
        try:
            response = requests.get(self.base_url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            urls = []
            base_domain = urlparse(self.base_url).netloc

            # Find all links
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                abs_url = urljoin(self.base_url, href)

                # Filter: same domain, not the base URL, unique
                if (urlparse(abs_url).netloc == base_domain and
                    abs_url != self.base_url and
                    abs_url not in urls):
                    # Basic heuristic: looks like an article
                    if any(pattern in abs_url for pattern in ['/post/', '/blog/', '/article/', '/@', '/p/']):
                        urls.append(abs_url)
                    elif abs_url.count('/') >= 4:  # Likely content, not homepage
                        urls.append(abs_url)

            return urls

        except Exception as e:
            print(f"Error discovering articles: {e}")
            return []

    def _scrape_article(self, url: str):
        """Scrape single article content"""
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            title = soup.find('h1')
            title_text = title.get_text().strip() if title else "Untitled"

            # Extract paragraphs
            paragraphs = soup.find_all('p')
            text = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

            # Filter out very short content (likely not articles)
            if len(text) < 500:
                return None

            word_count = len(text.split())

            return {
                'url': url,
                'title': title_text,
                'content': text,
                'word_count': word_count
            }

        except Exception as e:
            print(f"    Error scraping {url}: {e}")
            return None

    def save_examples(self, articles, examples_dir):
        """Save articles as example files"""
        examples_dir = Path(examples_dir)
        examples_dir.mkdir(parents=True, exist_ok=True)

        for i, article in enumerate(articles, 1):
            # Create safe filename
            safe_title = "".join(c for c in article['title'][:50] if c.isalnum() or c in (' ', '-'))
            safe_title = safe_title.replace(' ', '-').lower()
            filename = f"{i:02d}-{safe_title}.md"

            filepath = examples_dir / filename

            # Write article with metadata
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {article['title']}\n\n")
                f.write(f"**Source**: {article['url']}\n")
                f.write(f"**Word Count**: {article['word_count']}\n\n")
                f.write("---\n\n")
                f.write(article['content'])
