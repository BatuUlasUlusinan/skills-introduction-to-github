#!/usr/bin/env python3
"""
Example usage of the Product Scraper.
Ürün Arama Aracının örnek kullanımı.

Bu dosya, ürün arama aracının nasıl kullanılacağını gösterir.
This file demonstrates how to use the product scraper.
"""

from product_scraper import ProductScraper, Product
from product_scraper.ai_analyzer import AIAnalyzer
from product_scraper.config import ScraperConfig


def example_basic_search():
    """
    Basic product search example.
    Temel ürün arama örneği.
    """
    print("=" * 60)
    print("ÖRNEK 1: Temel Ürün Arama / Basic Product Search")
    print("=" * 60)
    
    # Create a product to search / Aranacak ürün oluştur
    product = Product(
        name="iPhone 15 Pro Max",
        brand="Apple",
        model="Pro Max",
        size="256GB",
        specifications={
            "Renk": "Titanium Black",
            "Ekran": "6.7 inch",
        }
    )
    
    # Initialize scraper / Arama aracını başlat
    scraper = ProductScraper()
    
    # Generate search query / Arama sorgusunu oluştur
    query = product.to_search_query()
    print(f"\n🔍 Arama sorgusu / Search query: {query}")
    
    # Note: Actual search requires SERPAPI_KEY
    # Not: Gerçek arama SERPAPI_KEY gerektirir
    print("\n⚠️ Gerçek arama için SERPAPI_KEY ortam değişkenini ayarlayın.")
    print("   Set SERPAPI_KEY environment variable for actual search.")
    
    # Perform search / Arama yap
    results = scraper.search(product)
    
    if results:
        print(f"\n✅ {len(results)} sonuç bulundu / results found")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result}")
    else:
        print("\n📝 Demo mode - Set SERPAPI_KEY for real results")


def example_with_specifications():
    """
    Search with detailed specifications.
    Detaylı özelliklerle arama.
    """
    print("\n" + "=" * 60)
    print("ÖRNEK 2: Detaylı Özelliklerle Arama / Search with Specifications")
    print("=" * 60)
    
    # Create a laptop product with detailed specs
    # Detaylı özelliklerle bir laptop ürünü oluştur
    product = Product(
        name="ThinkPad X1 Carbon",
        brand="Lenovo",
        model="Gen 11",
        weight="1.12 kg",
        specifications={
            "İşlemci": "Intel Core i7-1365U",
            "RAM": "16GB LPDDR5",
            "Depolama": "512GB SSD",
            "Ekran": "14 inch 2.8K OLED",
            "İşletim Sistemi": "Windows 11 Pro",
        }
    )
    
    config = ScraperConfig.from_env()
    config.max_pages = 5  # Limit pages for demo / Demo için sayfa sınırla
    
    scraper = ProductScraper(config)
    
    query = product.to_search_query()
    print(f"\n🔍 Arama sorgusu / Search query: {query}")
    
    # Formatted output / Biçimlendirilmiş çıktı
    output = scraper.search_and_format(product)
    print(output)


def example_ai_enhanced():
    """
    AI-enhanced product matching example.
    Yapay zeka destekli ürün eşleştirme örneği.
    """
    print("\n" + "=" * 60)
    print("ÖRNEK 3: AI Destekli Eşleştirme / AI-Enhanced Matching")
    print("=" * 60)
    
    product = Product(
        name="Galaxy S24 Ultra",
        brand="Samsung",
        model="Ultra",
        size="512GB",
        specifications={
            "RAM": "12GB",
            "Kamera": "200MP",
        }
    )
    
    config = ScraperConfig.from_env()
    
    # Check if OpenAI API key is set / OpenAI API anahtarı ayarlı mı kontrol et
    if config.openai_api_key:
        analyzer = AIAnalyzer(config)
        
        # Generate search queries using AI / AI kullanarak arama sorguları oluştur
        queries = analyzer.generate_search_queries(product)
        print("\n📝 AI tarafından oluşturulan sorgular / AI-generated queries:")
        for q in queries:
            print(f"   - {q}")
    else:
        print("\n⚠️ AI özellikleri için OPENAI_API_KEY ayarlayın.")
        print("   Set OPENAI_API_KEY for AI features.")
        
        # Fallback to basic query / Temel sorguya geri dön
        print(f"\n📝 Temel sorgu / Basic query: {product.to_search_query()}")


def example_configuration():
    """
    Configuration example.
    Yapılandırma örneği.
    """
    print("\n" + "=" * 60)
    print("ÖRNEK 4: Yapılandırma / Configuration")
    print("=" * 60)
    
    # Create custom configuration / Özel yapılandırma oluştur
    config = ScraperConfig(
        serpapi_key="YOUR_SERPAPI_KEY",  # Replace with actual key
        openai_api_key="YOUR_OPENAI_KEY",  # Replace with actual key
        max_pages=10,
        results_per_page=10,
        search_region="tr",
        search_language="tr",
        request_timeout=30,
        delay_between_requests=1.5,
    )
    
    print("\n📋 Yapılandırma Ayarları / Configuration Settings:")
    print(f"   - Maksimum sayfa / Max pages: {config.max_pages}")
    print(f"   - Sayfa başına sonuç / Results per page: {config.results_per_page}")
    print(f"   - Arama bölgesi / Search region: {config.search_region}")
    print(f"   - Arama dili / Search language: {config.search_language}")
    print(f"   - İstek zaman aşımı / Request timeout: {config.request_timeout}s")
    print(f"   - İstekler arası gecikme / Delay: {config.delay_between_requests}s")
    
    print("\n🔑 Ortam Değişkenleri / Environment Variables:")
    print("   export SERPAPI_KEY='your-serpapi-key'")
    print("   export OPENAI_API_KEY='your-openai-key'")


def main():
    """Run all examples."""
    print("\n" + "🚀" * 20)
    print("YAPAY ZEKA DESTEKLİ ÜRÜN ARAMA ARACI")
    print("AI-POWERED PRODUCT SEARCH TOOL")
    print("🚀" * 20 + "\n")
    
    example_basic_search()
    example_with_specifications()
    example_ai_enhanced()
    example_configuration()
    
    print("\n" + "=" * 60)
    print("✅ Örnekler tamamlandı / Examples completed")
    print("=" * 60)


if __name__ == "__main__":
    main()
