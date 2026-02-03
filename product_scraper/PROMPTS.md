# 🤖 AI-Powered Web Scraping - Prompt Templates
# Yapay Zeka Destekli Web Scraping - Prompt Şablonları

Bu dosya, AI destekli ürün arama ve fiyat karşılaştırma sistemi geliştirmek için kullanılabilecek prompt şablonlarını içerir.

---

## 1. Ürün Eşleştirme Prompt'u / Product Matching Prompt

```
Sen bir ürün eşleştirme asistanısın. Görevin, bir arama sonucunun aranan ürünle eşleşip eşleşmediğini belirlemek.

Aranan Ürün:
- İsim: {product_name}
- Marka: {brand}
- Model: {model}
- Boyut: {size}
- Ağırlık: {weight}
- Teknik Özellikler: {specifications}

Bulunan Sonuç:
- Başlık: {result_title}
- Site: {site_name}
- URL: {url}
- Fiyat: {price}

Bu sonuç aranan ürünle eşleşiyor mu? 
Yanıtını JSON formatında ver:
{
    "is_match": true/false,
    "confidence": 0.0-1.0,
    "reason": "Eşleşme/eşleşmeme nedeni"
}
```

---

## 2. Fiyat Çıkarma Prompt'u / Price Extraction Prompt

```
Sen bir fiyat çıkarma uzmanısın. Verilen HTML içeriğinden ürün fiyatını çıkar.

Aranan Ürün: {product_name} {brand} {model}

HTML İçeriği:
{html_content}

Fiyat bilgisini JSON formatında çıkar:
{
    "price": sayısal_değer,
    "currency": "TRY/USD/EUR",
    "original_price": indirimsiz_fiyat_varsa,
    "discount_percentage": indirim_yüzdesi_varsa,
    "in_stock": true/false
}
```

---

## 3. Arama Sorgusu Oluşturma Prompt'u / Search Query Generation Prompt

```
Sen bir e-ticaret arama uzmanısın. Verilen ürün bilgilerine göre en etkili arama sorgularını oluştur.

Ürün Bilgileri:
- İsim: {product_name}
- Marka: {brand}
- Model: {model}
- Özellikler: {specifications}

Türkçe e-ticaret sitelerinde bu ürünü bulmak için 5 farklı arama sorgusu oluştur.
Her sorgu farklı bir arama stratejisi kullanmalı:
1. Tam eşleşme
2. Marka odaklı
3. Model odaklı
4. Özellik odaklı
5. Genel arama

JSON formatında yanıt ver:
{
    "queries": [
        "sorgu1",
        "sorgu2",
        "sorgu3",
        "sorgu4",
        "sorgu5"
    ]
}
```

---

## 4. Site Analizi Prompt'u / Site Analysis Prompt

```
Sen bir e-ticaret site analisti. Verilen HTML yapısını analiz ederek fiyat ve stok bilgilerini çıkarmak için gerekli CSS seçicileri belirle.

Site: {site_name}
URL Örneği: {sample_url}

HTML Yapısı:
{html_structure}

Aşağıdaki bilgileri içeren JSON yanıtı ver:
{
    "price_selectors": ["CSS seçici1", "CSS seçici2"],
    "original_price_selectors": ["CSS seçici1"],
    "stock_selectors": ["CSS seçici1"],
    "title_selectors": ["CSS seçici1"],
    "image_selectors": ["CSS seçici1"]
}
```

---

## 5. Sonuç Özetleme Prompt'u / Result Summarization Prompt

```
Sen bir fiyat karşılaştırma uzmanısın. Aşağıdaki arama sonuçlarını analiz et ve kullanıcıya yardımcı bir özet sun.

Aranan Ürün: {product_name} {brand} {model}

Bulunan Sonuçlar:
{results_json}

Aşağıdakileri içeren bir özet hazırla:
1. En düşük fiyat ve hangi sitede
2. En yüksek fiyat ve hangi sitede
3. Ortalama fiyat
4. Fiyat aralığı
5. Öneriler (en iyi fırsat, güvenilir satıcı vb.)

Türkçe ve kullanıcı dostu bir dilde yanıt ver.
```

---

## 6. Ürün Doğrulama Prompt'u / Product Validation Prompt

```
Sen bir ürün doğrulama uzmanısın. Bulunan ürünün aranan ürünle aynı olup olmadığını doğrula.

Aranan Ürün Özellikleri:
{original_product}

Bulunan Ürün Bilgileri:
{found_product}

Kontrol edilmesi gerekenler:
1. Marka eşleşmesi
2. Model eşleşmesi
3. Depolama kapasitesi (varsa)
4. Renk (varsa)
5. Diğer kritik özellikler

JSON yanıtı:
{
    "is_exact_match": true/false,
    "is_similar": true/false,
    "matching_features": ["özellik1", "özellik2"],
    "mismatched_features": ["özellik1"],
    "confidence_score": 0.0-1.0,
    "recommendation": "Bu ürünü öneririm/önermiyorum çünkü..."
}
```

---

## 7. Hata Ayıklama Prompt'u / Debugging Prompt

```
Sen bir web scraping uzmanısın. Aşağıdaki hata durumunu analiz et ve çözüm öner.

Hata Mesajı: {error_message}
Hedef URL: {url}
HTTP Durum Kodu: {status_code}
İstek Başlıkları: {headers}

Olası nedenler ve çözümler:
1. ...
2. ...
3. ...

Önerilen kod değişiklikleri:
```python
# Önerilen düzeltme
```
```

---

## 8. Kod Geliştirme Prompt'u / Code Development Prompt

Bu prompt, AI'dan kod yazmasını istemek için kullanılır:

```
Web scraping ve fiyat karşılaştırma için bir Python modülü geliştir.

Gereksinimler:
1. Google arama sonuçlarını SerpAPI ile çek
2. E-ticaret sitelerini tespit et
3. Ürün sayfalarından fiyat çıkar
4. Sonuçları yapılandırılmış formatta döndür

Teknik Özellikler:
- Python 3.10+
- requests kütüphanesi
- BeautifulSoup4 HTML ayrıştırma
- Regex ile fiyat çıkarma
- Type hints kullan
- Docstrings ekle (Türkçe ve İngilizce)
- Hata yönetimi

Beklenen Çıktı:
- models.py: Veri modelleri
- scraper.py: Ana arama modülü
- config.py: Yapılandırma
- cli.py: Komut satırı arayüzü

Her modül için temiz, okunabilir ve bakımı kolay kod yaz.
```

---

## 📝 Kullanım Önerileri / Usage Tips

1. **Bağlam Sağlama**: Prompt'lara her zaman yeterli bağlam bilgisi ekleyin
2. **Yapılandırılmış Çıktı**: JSON formatında yanıt isteyin
3. **Örnekler Verin**: Beklenen çıktı örnekleri ekleyin
4. **İteratif Geliştirme**: Prompt'ları test edip geliştirin
5. **Hata Yönetimi**: Olası hata durumlarını ele alın

---

## 🔗 İlgili Kaynaklar / Related Resources

- [OpenAI API Dokümantasyonu](https://platform.openai.com/docs)
- [SerpAPI Dokümantasyonu](https://serpapi.com/docs)
- [BeautifulSoup4 Dokümantasyonu](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Kütüphanesi](https://docs.python-requests.org/)
