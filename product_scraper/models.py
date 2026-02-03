"""
Data models for the product scraper.
Ürün arama için veri modelleri.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Product:
    """
    Represents a product to search for.
    Aranacak ürünü temsil eder.
    
    Attributes:
        name (str): Product name / Ürün adı
        brand (str): Brand name / Marka adı
        model (str): Model number/name / Model numarası/adı
        size (str): Product size / Ürün boyutu
        weight (str): Product weight / Ürün ağırlığı
        specifications (dict): Technical specifications / Teknik özellikler
    """
    name: str
    brand: str = ""
    model: str = ""
    size: str = ""
    weight: str = ""
    specifications: dict = field(default_factory=dict)
    
    def to_search_query(self) -> str:
        """
        Convert product details to a search query string.
        Ürün detaylarını arama sorgusu dizesine dönüştürür.
        """
        parts = [self.name]
        if self.brand:
            parts.append(self.brand)
        if self.model:
            parts.append(self.model)
        if self.size:
            parts.append(self.size)
        
        # Add key specifications to the search query
        for key, value in self.specifications.items():
            if value:
                parts.append(f"{value}")
        
        return " ".join(parts)


@dataclass
class SearchResult:
    """
    Represents a search result with product information.
    Ürün bilgisi ile arama sonucunu temsil eder.
    
    Attributes:
        site_name (str): Name of the selling site / Satış sitesinin adı
        url (str): Product URL / Ürün URL'i
        price (str): Product price / Ürün fiyatı
        currency (str): Currency code / Para birimi kodu
        title (str): Product title from the page / Sayfadaki ürün başlığı
        is_available (bool): Whether the product is available / Ürün mevcut mu
        scraped_at (datetime): When the data was scraped / Veri ne zaman çekildi
    """
    site_name: str
    url: str
    price: Optional[str] = None
    currency: str = "TRY"
    title: str = ""
    is_available: bool = True
    scraped_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convert to dictionary format."""
        return {
            "site_name": self.site_name,
            "url": self.url,
            "price": self.price,
            "currency": self.currency,
            "title": self.title,
            "is_available": self.is_available,
            "scraped_at": self.scraped_at.isoformat()
        }
    
    def __str__(self) -> str:
        """String representation for display."""
        price_str = f"{self.price} {self.currency}" if self.price else "Fiyat bulunamadı"
        return f"{self.site_name}: {price_str} - {self.url}"
