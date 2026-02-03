# 🤖 AI-Powered Product Search and Price Comparison Tool
# Yapay Zeka Destekli Ürün Arama ve Fiyat Karşılaştırma Aracı

Bu araç, belirlenen bir ürünün isim, marka, model, boyut, ağırlık ve teknik özellikleri ile Google arama motoru üzerinden aratarak e-ticaret sitelerini listeleyip, ürün fiyatlarını çıkarır.

This tool searches for a specified product using its name, brand, model, size, weight, and technical specifications through Google, lists e-commerce sites, and extracts product prices.

## 🌟 Özellikler / Features

- **Google Arama Entegrasyonu / Google Search Integration**: SerpAPI kullanarak güvenilir arama
- **Fiyat Çıkarma / Price Extraction**: Regex ve AI destekli fiyat tespiti
- **AI Eşleştirme / AI Matching**: OpenAI ile akıllı ürün eşleştirme
- **Çoklu Site Desteği / Multi-Site Support**: Trendyol, Hepsiburada, N11, Amazon.com.tr vb.
- **Kolay Kullanım / Easy to Use**: CLI ve Python API

## 📋 Kurulum / Installation

```bash
# Clone the repository / Repoyu klonla
git clone https://github.com/YOUR_USERNAME/skills-introduction-to-github.git
cd skills-introduction-to-github

# Install dependencies / Bağımlılıkları kur
pip install -r product_scraper/requirements.txt
```

## 🔑 API Anahtarları / API Keys

### Gerekli / Required
- **SerpAPI**: Google arama sonuçları için (https://serpapi.com)

### Opsiyonel / Optional
- **OpenAI API**: AI destekli eşleştirme için (https://platform.openai.com)

```bash
# Set environment variables / Ortam değişkenlerini ayarla
export SERPAPI_KEY="your-serpapi-key"
export OPENAI_API_KEY="your-openai-key"  # Optional
```

## 🚀 Kullanım / Usage

### Komut Satırı / Command Line

```bash
# Basic search / Temel arama
python -m product_scraper.cli --name "iPhone 15" --brand "Apple" --model "Pro Max"

# With specifications / Özelliklerle
python -m product_scraper.cli --name "Laptop" --brand "Lenovo" \
    --specs '{"RAM": "16GB", "Storage": "512GB SSD"}'

# JSON output / JSON çıktı
python -m product_scraper.cli --name "AirPods Pro" --brand "Apple" --json

# With AI matching / AI eşleştirme ile
python -m product_scraper.cli --name "Samsung TV" --brand "Samsung" --use-ai

# Save to file / Dosyaya kaydet
python -m product_scraper.cli --name "iPad Pro" --brand "Apple" --output results.txt
```

### Python API

```python
from product_scraper import ProductScraper, Product
from product_scraper.ai_analyzer import AIAnalyzer

# Create a product / Ürün oluştur
product = Product(
    name="iPhone 15 Pro Max",
    brand="Apple",
    model="Pro Max",
    size="256GB",
    weight="221g",
    specifications={
        "Renk": "Titanium Black",
        "Ekran": "6.7 inch",
        "İşlemci": "A17 Pro",
    }
)

# Initialize scraper / Arama aracını başlat
scraper = ProductScraper()

# Search / Ara
results = scraper.search(product)

# Print results / Sonuçları yazdır
for result in results:
    print(f"{result.site_name}: {result.price} TL")
    print(f"  URL: {result.url}")
```

### AI Destekli Kullanım / AI-Enhanced Usage

```python
from product_scraper import ProductScraper, Product
from product_scraper.ai_analyzer import AIAnalyzer
from product_scraper.config import ScraperConfig

# Configure / Yapılandır
config = ScraperConfig.from_env()

# Create analyzer / Analizör oluştur
analyzer = AIAnalyzer(config)

# Generate search queries / Arama sorguları oluştur
product = Product(name="MacBook Pro", brand="Apple", model="M3 Pro")
queries = analyzer.generate_search_queries(product)

# Search and match / Ara ve eşleştir
scraper = ProductScraper(config)
results = scraper.search(product)

# Filter with AI / AI ile filtrele
for result in results:
    is_match, confidence = analyzer.match_product(product, result)
    if is_match and confidence > 0.8:
        print(f"✅ {result.site_name}: {result.price} TL (Güven: {confidence:.2%})")
```

## 📁 Proje Yapısı / Project Structure

```
product_scraper/
├── __init__.py        # Package initialization / Paket başlatma
├── models.py          # Data models / Veri modelleri
├── config.py          # Configuration / Yapılandırma
├── scraper.py         # Main scraper / Ana arama modülü
├── ai_analyzer.py     # AI features / AI özellikleri
├── cli.py             # Command-line interface / Komut satırı arayüzü
├── examples.py        # Usage examples / Kullanım örnekleri
└── requirements.txt   # Dependencies / Bağımlılıklar
```

## 🔧 Yapılandırma Seçenekleri / Configuration Options

| Ayar / Setting | Varsayılan / Default | Açıklama / Description |
|----------------|----------------------|------------------------|
| `max_pages` | 25 | Maximum search pages / Maksimum arama sayfası |
| `results_per_page` | 10 | Results per page / Sayfa başına sonuç |
| `search_region` | "tr" | Search region / Arama bölgesi |
| `search_language` | "tr" | Search language / Arama dili |
| `request_timeout` | 30 | Request timeout (seconds) / İstek zaman aşımı |
| `delay_between_requests` | 1.0 | Delay between requests / İstekler arası gecikme |

## 📊 Desteklenen E-Ticaret Siteleri / Supported E-Commerce Sites

- Trendyol
- Hepsiburada
- N11
- Amazon.com.tr
- GittiGidiyor
- Çiçeksepeti
- Morhipo
- Boyner
- MediaMarkt
- Teknosa
- Vatan Bilgisayar
- İncehesap
- Itopya
- Akakçe
- Cimri

## 🛠️ Geliştirme Adımları / Development Steps

### 1. Proje Yapısını Oluşturma / Create Project Structure
```bash
mkdir product_scraper
cd product_scraper
```

### 2. Veri Modellerini Tanımlama / Define Data Models
- `Product`: Aranacak ürün bilgileri
- `SearchResult`: Bulunan sonuç bilgileri

### 3. API Entegrasyonu / API Integration
- SerpAPI ile Google arama
- Requests ile HTTP istekleri
- BeautifulSoup ile HTML ayrıştırma

### 4. Fiyat Çıkarma / Price Extraction
- Regex desenleri ile fiyat tespiti
- Site-spesifik çıkarma mantığı

### 5. AI Özellikleri / AI Features
- OpenAI ile ürün eşleştirme
- Akıllı sorgu oluşturma
- Sonuç özetleme

## 📝 Örnek Çıktı / Example Output

```
🔍 Searching for: iPhone 15 Pro Max Apple 256GB

✅ 15 sonuç bulundu / 15 results found
============================================================

1. Trendyol
   📦 Apple iPhone 15 Pro Max 256GB Titanium Black
   💰 Fiyat: 74999.00 TL
   🔗 https://www.trendyol.com/apple/iphone-15-pro-max...

2. Hepsiburada
   📦 Apple iPhone 15 Pro Max 256 GB
   💰 Fiyat: 74990.00 TL
   🔗 https://www.hepsiburada.com/apple-iphone-15-pro-max...

3. N11
   📦 Apple iPhone 15 Pro Max 256GB
   💰 Fiyat: 75500.00 TL
   🔗 https://www.n11.com/urun/apple-iphone-15-pro-max...

============================================================
```

## ⚠️ Önemli Notlar / Important Notes

1. **Rate Limiting**: Aşırı istek yapmaktan kaçının / Avoid excessive requests
2. **ToS Compliance**: Site kullanım şartlarına uyun / Comply with site ToS
3. **API Keys**: API anahtarlarınızı gizli tutun / Keep API keys secret
4. **Legal Use**: Yasal amaçlar için kullanın / Use for legal purposes

## 📄 Lisans / License

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🤝 Katkıda Bulunma / Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Not / Note**: Bu araç eğitim amaçlıdır. Ticari kullanım için ilgili sitelerin API'lerini kullanın.
This tool is for educational purposes. For commercial use, utilize the official APIs of relevant sites.
