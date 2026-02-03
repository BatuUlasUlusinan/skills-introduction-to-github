"""
Main scraper module for product search and price extraction.
Ürün arama ve fiyat çıkarma için ana modül.
"""

import re
import time
import logging
from typing import Generator, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from .models import Product, SearchResult
from .config import ScraperConfig


# Configure logging / Günlük kaydını yapılandır
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ProductScraper:
    """
    Main class for searching products and extracting prices.
    Ürün arama ve fiyat çıkarma için ana sınıf.
    
    Kullanım / Usage:
        scraper = ProductScraper()
        product = Product(
            name="iPhone 15",
            brand="Apple",
            model="Pro Max",
            size="256GB"
        )
        results = scraper.search(product)
        for result in results:
            print(result)
    """
    
    def __init__(self, config: Optional[ScraperConfig] = None):
        """
        Initialize the scraper with configuration.
        Yapılandırma ile arama aracını başlatır.
        
        Args:
            config: Scraper configuration. If None, uses default config.
                   Arama yapılandırması. None ise varsayılan yapılandırma kullanılır.
        """
        self.config = config or ScraperConfig.from_env()
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create a configured requests session."""
        session = requests.Session()
        session.headers.update({
            "User-Agent": self.config.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": f"{self.config.search_language},en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        })
        return session
    
    def search(self, product: Product, use_api: bool = True) -> list[SearchResult]:
        """
        Search for a product and return results.
        Ürün arar ve sonuçları döndürür.
        
        Args:
            product: The product to search for / Aranacak ürün
            use_api: Whether to use SerpAPI (recommended) / SerpAPI kullanılsın mı
        
        Returns:
            List of search results with prices / Fiyatlı arama sonuçları listesi
        """
        if use_api and self.config.serpapi_key:
            return self._search_with_serpapi(product)
        else:
            logger.warning(
                "SerpAPI key not found. Using direct scraping (rate limited)."
                " / SerpAPI anahtarı bulunamadı. Doğrudan arama kullanılıyor."
            )
            return self._search_direct(product)
    
    def _search_with_serpapi(self, product: Product) -> list[SearchResult]:
        """
        Search using SerpAPI service.
        SerpAPI servisi kullanarak arama yapar.
        """
        results = []
        query = product.to_search_query() + " fiyat satın al"  # Add "price buy" in Turkish
        
        logger.info(f"Searching for: {query}")
        
        for page in range(self.config.max_pages):
            try:
                params = {
                    "api_key": self.config.serpapi_key,
                    "engine": "google",
                    "q": query,
                    "google_domain": "google.com.tr",
                    "gl": self.config.search_region,
                    "hl": self.config.search_language,
                    "start": page * self.config.results_per_page,
                    "num": self.config.results_per_page,
                }
                
                response = self.session.get(
                    "https://serpapi.com/search",
                    params=params,
                    timeout=self.config.request_timeout
                )
                response.raise_for_status()
                data = response.json()
                
                organic_results = data.get("organic_results", [])
                if not organic_results:
                    logger.info(f"No more results at page {page + 1}")
                    break
                
                for item in organic_results:
                    url = item.get("link", "")
                    if self._is_ecommerce_site(url):
                        result = self._extract_result_info(
                            url=url,
                            title=item.get("title", ""),
                            snippet=item.get("snippet", "")
                        )
                        if result:
                            results.append(result)
                
                # Delay between requests / İstekler arası gecikme
                time.sleep(self.config.delay_between_requests)
                
            except requests.RequestException as e:
                logger.error(f"Request error on page {page + 1}: {e}")
                continue
            except Exception as e:
                logger.error(f"Error on page {page + 1}: {e}")
                continue
        
        # Try to get prices from individual pages
        results = self._enrich_with_prices(results)
        
        return results
    
    def _search_direct(self, product: Product) -> list[SearchResult]:
        """
        Direct Google search (for demonstration/fallback).
        Doğrudan Google araması (gösterim/yedek için).
        
        Note: Direct Google scraping may be blocked. Use SerpAPI for production.
        Not: Doğrudan Google taraması engellenebilir. Üretim için SerpAPI kullanın.
        """
        results = []
        query = product.to_search_query() + " fiyat satın al"
        
        logger.warning(
            "Direct scraping is not recommended for production use. "
            "Please use SerpAPI or similar service."
        )
        
        # For demonstration only - returns empty as direct Google scraping 
        # requires handling CAPTCHAs and may violate ToS
        logger.info(f"Query prepared: {query}")
        logger.info("Please set SERPAPI_KEY environment variable for actual searching.")
        
        return results
    
    def _is_ecommerce_site(self, url: str) -> bool:
        """
        Check if URL belongs to a known e-commerce site.
        URL'nin bilinen bir e-ticaret sitesine ait olup olmadığını kontrol eder.
        """
        try:
            domain = urlparse(url).netloc.lower()
            return any(pattern in domain for pattern in self.config.ecommerce_patterns)
        except Exception:
            return False
    
    def _extract_result_info(
        self, 
        url: str, 
        title: str, 
        snippet: str
    ) -> Optional[SearchResult]:
        """
        Extract search result information.
        Arama sonucu bilgilerini çıkarır.
        """
        try:
            domain = urlparse(url).netloc
            site_name = domain.replace("www.", "").split(".")[0].capitalize()
            
            # Try to extract price from snippet
            price = self._extract_price(snippet)
            
            return SearchResult(
                site_name=site_name,
                url=url,
                price=price,
                title=title,
                is_available=True
            )
        except Exception as e:
            logger.debug(f"Error extracting result info: {e}")
            return None
    
    def _extract_price(self, text: str) -> Optional[str]:
        """
        Extract price from text using regex patterns.
        Regex desenleri kullanarak metinden fiyat çıkarır.
        """
        if not text:
            return None
        
        for pattern in self.config.price_patterns:
            match = re.search(pattern, text)
            if match:
                price = match.group(1)
                # Normalize price format
                price = price.replace(".", "").replace(",", ".")
                try:
                    float(price)
                    return price
                except ValueError:
                    continue
        
        return None
    
    def _enrich_with_prices(self, results: list[SearchResult]) -> list[SearchResult]:
        """
        Enrich results by fetching prices from individual pages.
        Bireysel sayfalardan fiyat alarak sonuçları zenginleştirir.
        """
        enriched = []
        
        for result in results:
            if result.price is None:
                try:
                    price = self._fetch_price_from_page(result.url)
                    result.price = price
                except Exception as e:
                    logger.debug(f"Could not fetch price from {result.url}: {e}")
            
            enriched.append(result)
            time.sleep(self.config.delay_between_requests)
        
        return enriched
    
    def _fetch_price_from_page(self, url: str) -> Optional[str]:
        """
        Fetch price from a product page.
        Ürün sayfasından fiyat alır.
        """
        try:
            response = self.session.get(
                url, 
                timeout=self.config.request_timeout
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Common price element patterns
            price_selectors = [
                {"class": re.compile(r"price|fiyat", re.I)},
                {"itemprop": "price"},
                {"data-price": True},
                {"class": re.compile(r"product.*price", re.I)},
            ]
            
            for selector in price_selectors:
                elements = soup.find_all(attrs=selector)
                for elem in elements:
                    text = elem.get_text(strip=True)
                    price = self._extract_price(text)
                    if price:
                        return price
            
            # Try extracting from full page text
            page_text = soup.get_text()
            return self._extract_price(page_text)
            
        except Exception as e:
            logger.debug(f"Error fetching page {url}: {e}")
            return None
    
    def search_and_format(self, product: Product) -> str:
        """
        Search and return formatted results as a string.
        Arar ve sonuçları biçimlendirilmiş bir dize olarak döndürür.
        """
        results = self.search(product)
        
        if not results:
            return "Sonuç bulunamadı. / No results found."
        
        lines = [
            f"Bulunan {len(results)} sonuç / {len(results)} results found:",
            "-" * 60
        ]
        
        for i, result in enumerate(results, 1):
            price_str = f"{result.price} {result.currency}" if result.price else "Fiyat bilinmiyor"
            lines.extend([
                f"\n{i}. {result.site_name}",
                f"   Başlık / Title: {result.title}",
                f"   Fiyat / Price: {price_str}",
                f"   Link: {result.url}",
            ])
        
        return "\n".join(lines)
