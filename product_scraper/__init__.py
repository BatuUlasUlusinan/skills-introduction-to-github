"""
AI-Powered Product Search and Price Comparison Tool
Yapay Zeka Destekli Ürün Arama ve Fiyat Karşılaştırma Aracı
"""

__version__ = "1.0.0"
__author__ = "Product Scraper Team"

from .scraper import ProductScraper
from .models import Product, SearchResult

__all__ = ["ProductScraper", "Product", "SearchResult"]
