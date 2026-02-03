"""
Configuration settings for the product scraper.
Ürün arama aracı için yapılandırma ayarları.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ScraperConfig:
    """
    Configuration class for the scraper.
    Arama aracı için yapılandırma sınıfı.
    """
    # API Keys - Set these as environment variables
    # API Anahtarları - Bunları ortam değişkenleri olarak ayarlayın
    serpapi_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    # Search settings / Arama ayarları
    max_pages: int = 25  # Maximum pages to search / Aranacak maksimum sayfa sayısı
    results_per_page: int = 10  # Results per page / Sayfa başına sonuç
    search_region: str = "tr"  # Search region (tr for Turkey) / Arama bölgesi
    search_language: str = "tr"  # Search language / Arama dili
    
    # Request settings / İstek ayarları
    request_timeout: int = 30  # Request timeout in seconds / İstek zaman aşımı (saniye)
    delay_between_requests: float = 1.0  # Delay between requests / İstekler arası gecikme
    max_retries: int = 3  # Maximum retry attempts / Maksimum yeniden deneme
    
    # User agent for web requests / Web istekleri için user agent
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    # Price extraction patterns / Fiyat çıkarma desenleri
    price_patterns: tuple = (
        r"(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)\s*(?:TL|₺|TRY)",
        r"(?:TL|₺|TRY)\s*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)",
        r"(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)\s*(?:USD|\$|EUR|€)",
    )
    
    # E-commerce site patterns to identify selling sites
    # Satış sitelerini tanımlamak için e-ticaret site desenleri
    ecommerce_patterns: tuple = (
        "trendyol.com",
        "hepsiburada.com",
        "n11.com",
        "gittigidiyor.com",
        "amazon.com.tr",
        "ciceksepeti.com",
        "morhipo.com",
        "boyner.com.tr",
        "mediamarkt.com.tr",
        "teknosa.com",
        "vatanbilgisayar.com",
        "incehesap.com",
        "itopya.com",
        "akakce.com",
        "cimri.com",
    )
    
    @classmethod
    def from_env(cls) -> "ScraperConfig":
        """
        Create configuration from environment variables.
        Ortam değişkenlerinden yapılandırma oluşturur.
        """
        return cls(
            serpapi_key=os.getenv("SERPAPI_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            max_pages=int(os.getenv("MAX_PAGES", "25")),
            results_per_page=int(os.getenv("RESULTS_PER_PAGE", "10")),
            search_region=os.getenv("SEARCH_REGION", "tr"),
            search_language=os.getenv("SEARCH_LANGUAGE", "tr"),
            request_timeout=int(os.getenv("REQUEST_TIMEOUT", "30")),
            delay_between_requests=float(os.getenv("DELAY_BETWEEN_REQUESTS", "1.0")),
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
        )
