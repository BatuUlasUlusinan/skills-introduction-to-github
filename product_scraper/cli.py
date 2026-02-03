#!/usr/bin/env python3
"""
Command-line interface for the product scraper.
Ürün arama aracı için komut satırı arayüzü.

Usage / Kullanım:
    python -m product_scraper.cli --name "iPhone 15" --brand "Apple" --model "Pro Max"
"""

import argparse
import json
import sys
from typing import Optional

from .models import Product, SearchResult
from .scraper import ProductScraper
from .ai_analyzer import AIAnalyzer
from .config import ScraperConfig


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description="AI-Powered Product Search and Price Comparison Tool / "
                    "Yapay Zeka Destekli Ürün Arama ve Fiyat Karşılaştırma Aracı",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples / Örnekler:
  # Search for an iPhone
  python -m product_scraper.cli --name "iPhone 15" --brand "Apple" --model "Pro Max"
  
  # Search with specifications
  python -m product_scraper.cli --name "Laptop" --brand "Lenovo" \\
      --specs '{"RAM": "16GB", "Storage": "512GB SSD"}'
  
  # Output as JSON
  python -m product_scraper.cli --name "AirPods Pro" --brand "Apple" --json
"""
    )
    
    # Required arguments / Zorunlu argümanlar
    parser.add_argument(
        "--name", "-n",
        required=True,
        help="Product name / Ürün adı"
    )
    
    # Optional arguments / Opsiyonel argümanlar
    parser.add_argument(
        "--brand", "-b",
        default="",
        help="Brand name / Marka adı"
    )
    parser.add_argument(
        "--model", "-m",
        default="",
        help="Model number or name / Model numarası veya adı"
    )
    parser.add_argument(
        "--size", "-s",
        default="",
        help="Product size / Ürün boyutu"
    )
    parser.add_argument(
        "--weight", "-w",
        default="",
        help="Product weight / Ürün ağırlığı"
    )
    parser.add_argument(
        "--specs",
        default="{}",
        help="Technical specifications as JSON / JSON olarak teknik özellikler"
    )
    
    # Output options / Çıktı seçenekleri
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output results as JSON / Sonuçları JSON olarak çıkar"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path / Çıktı dosya yolu"
    )
    
    # Search options / Arama seçenekleri
    parser.add_argument(
        "--max-pages",
        type=int,
        default=25,
        help="Maximum pages to search (default: 25) / Aranacak maksimum sayfa (varsayılan: 25)"
    )
    parser.add_argument(
        "--use-ai",
        action="store_true",
        help="Use AI for enhanced matching / Gelişmiş eşleştirme için AI kullan"
    )
    
    return parser


def main(args: Optional[list[str]] = None) -> int:
    """
    Main entry point for the CLI.
    CLI için ana giriş noktası.
    """
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    try:
        # Parse specifications JSON / Özellikler JSON'ını ayrıştır
        specs = json.loads(parsed_args.specs)
    except json.JSONDecodeError as e:
        print(f"Error parsing specifications JSON: {e}", file=sys.stderr)
        return 1
    
    # Create product / Ürün oluştur
    product = Product(
        name=parsed_args.name,
        brand=parsed_args.brand,
        model=parsed_args.model,
        size=parsed_args.size,
        weight=parsed_args.weight,
        specifications=specs
    )
    
    # Create scraper with configuration / Yapılandırma ile arama aracı oluştur
    config = ScraperConfig.from_env()
    config.max_pages = parsed_args.max_pages
    
    scraper = ProductScraper(config)
    
    # Perform search / Arama yap
    print(f"\n🔍 Searching for: {product.to_search_query()}")
    print("-" * 60)
    
    results = scraper.search(product)
    
    # Apply AI matching if requested / İstenirse AI eşleştirme uygula
    if parsed_args.use_ai and results:
        print("\n🤖 Applying AI matching...")
        analyzer = AIAnalyzer(config)
        filtered_results = []
        
        for result in results:
            is_match, confidence = analyzer.match_product(product, result)
            if is_match and confidence > 0.7:
                filtered_results.append(result)
        
        results = filtered_results
        print(f"   Filtered to {len(results)} matching results")
    
    # Output results / Sonuçları çıkar
    if parsed_args.json:
        output = json.dumps(
            [r.to_dict() for r in results],
            ensure_ascii=False,
            indent=2
        )
    else:
        output = format_results(results)
    
    # Write to file or stdout / Dosyaya veya stdout'a yaz
    if parsed_args.output:
        with open(parsed_args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n✅ Results saved to: {parsed_args.output}")
    else:
        print(output)
    
    return 0


def format_results(results: list[SearchResult]) -> str:
    """
    Format results for display.
    Sonuçları görüntüleme için biçimlendirir.
    """
    if not results:
        return "\n❌ Sonuç bulunamadı. / No results found.\n"
    
    lines = [
        f"\n✅ {len(results)} sonuç bulundu / {len(results)} results found\n",
        "=" * 60
    ]
    
    for i, result in enumerate(results, 1):
        price_str = f"{result.price} {result.currency}" if result.price else "Fiyat bilinmiyor"
        lines.extend([
            f"\n{i}. {result.site_name}",
            f"   📦 {result.title}",
            f"   💰 Fiyat: {price_str}",
            f"   🔗 {result.url}",
        ])
    
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
