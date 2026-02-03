"""
AI-enhanced price analysis module.
Yapay zeka destekli fiyat analiz modülü.
"""

import os
import json
import logging
from typing import Optional

from .models import Product, SearchResult
from .config import ScraperConfig


logger = logging.getLogger(__name__)


class AIAnalyzer:
    """
    AI-powered analyzer for product matching and price extraction.
    Ürün eşleştirme ve fiyat çıkarma için yapay zeka destekli analizör.
    
    Uses OpenAI API for intelligent product matching and data extraction.
    Akıllı ürün eşleştirme ve veri çıkarma için OpenAI API kullanır.
    """
    
    def __init__(self, config: Optional[ScraperConfig] = None):
        """
        Initialize the AI analyzer.
        Yapay zeka analizörünü başlatır.
        """
        self.config = config or ScraperConfig.from_env()
        self._client = None
    
    @property
    def client(self):
        """Lazy load OpenAI client."""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.config.openai_api_key)
            except ImportError:
                logger.error("OpenAI package not installed. Run: pip install openai")
                raise
        return self._client
    
    def match_product(
        self, 
        product: Product, 
        result: SearchResult
    ) -> tuple[bool, float]:
        """
        Use AI to determine if a search result matches the product.
        Arama sonucunun ürünle eşleşip eşleşmediğini belirlemek için yapay zeka kullanır.
        
        Args:
            product: The product being searched / Aranan ürün
            result: The search result to check / Kontrol edilecek arama sonucu
        
        Returns:
            Tuple of (is_match, confidence_score)
            (eşleşme_var_mı, güven_puanı) tuple'ı
        """
        if not self.config.openai_api_key:
            logger.warning("OpenAI API key not set. Skipping AI matching.")
            return True, 0.5  # Default to True with low confidence
        
        try:
            prompt = self._create_matching_prompt(product, result)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a product matching assistant. Your task is to determine "
                            "if a search result matches the product being searched for. "
                            "Respond with JSON containing 'is_match' (boolean) and "
                            "'confidence' (float 0-1)."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=100
            )
            
            result_text = response.choices[0].message.content
            data = json.loads(result_text)
            
            return data.get("is_match", False), data.get("confidence", 0.0)
            
        except Exception as e:
            logger.error(f"AI matching error: {e}")
            return True, 0.5
    
    def _create_matching_prompt(self, product: Product, result: SearchResult) -> str:
        """Create a prompt for product matching."""
        return f"""
Aranan Ürün / Product Searched:
- İsim / Name: {product.name}
- Marka / Brand: {product.brand}
- Model: {product.model}
- Boyut / Size: {product.size}
- Ağırlık / Weight: {product.weight}
- Özellikler / Specifications: {json.dumps(product.specifications, ensure_ascii=False)}

Bulunan Sonuç / Found Result:
- Başlık / Title: {result.title}
- Site: {result.site_name}
- URL: {result.url}

Bu sonuç aranan ürünle eşleşiyor mu? JSON olarak yanıt verin.
Does this result match the searched product? Respond in JSON.
"""
    
    def extract_structured_price(self, html_content: str, product: Product) -> dict:
        """
        Use AI to extract structured price information from HTML.
        HTML'den yapılandırılmış fiyat bilgisi çıkarmak için yapay zeka kullanır.
        
        Args:
            html_content: The HTML content to analyze / Analiz edilecek HTML içeriği
            product: The product being searched / Aranan ürün
        
        Returns:
            Dictionary with price information / Fiyat bilgisi içeren sözlük
        """
        if not self.config.openai_api_key:
            logger.warning("OpenAI API key not set. Skipping AI price extraction.")
            return {}
        
        try:
            # Limit HTML content to prevent token overflow
            limited_html = html_content[:4000]
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a price extraction assistant. Extract price "
                            "information from HTML content. Respond with JSON containing: "
                            "'price' (number), 'currency' (string), 'original_price' "
                            "(number, if discounted), 'in_stock' (boolean)."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Extract price for '{product.name} {product.brand} {product.model}' from:\n{limited_html}"
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=150
            )
            
            result_text = response.choices[0].message.content
            return json.loads(result_text)
            
        except Exception as e:
            logger.error(f"AI price extraction error: {e}")
            return {}
    
    def generate_search_queries(self, product: Product) -> list[str]:
        """
        Use AI to generate multiple search query variations.
        Birden fazla arama sorgusu varyasyonu oluşturmak için yapay zeka kullanır.
        
        Args:
            product: The product to search for / Aranacak ürün
        
        Returns:
            List of search query strings / Arama sorgusu dizeleri listesi
        """
        # Default queries without AI
        queries = [
            product.to_search_query(),
            f"{product.brand} {product.name} {product.model} fiyat",
            f"{product.name} {product.model} satın al",
        ]
        
        if not self.config.openai_api_key:
            return queries
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Generate 5 search queries in Turkish to find this product "
                            "for sale online. Return as JSON with 'queries' array."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"""
Ürün / Product:
- İsim / Name: {product.name}
- Marka / Brand: {product.brand}
- Model: {product.model}
- Boyut / Size: {product.size}
- Özellikler / Specs: {json.dumps(product.specifications, ensure_ascii=False)}
"""
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=200
            )
            
            result_text = response.choices[0].message.content
            data = json.loads(result_text)
            ai_queries = data.get("queries", [])
            
            # Combine default and AI queries
            return list(set(queries + ai_queries))
            
        except Exception as e:
            logger.error(f"AI query generation error: {e}")
            return queries
    
    def summarize_results(self, results: list[SearchResult]) -> str:
        """
        Generate an AI summary of search results.
        Arama sonuçlarının yapay zeka özetini oluşturur.
        
        Args:
            results: List of search results / Arama sonuçları listesi
        
        Returns:
            Summary string / Özet metni
        """
        if not results:
            return "Sonuç bulunamadı. / No results found."
        
        # Basic summary without AI
        prices = [
            float(r.price) for r in results 
            if r.price and r.price.replace(".", "").replace(",", "").isdigit()
        ]
        
        if prices:
            min_price = min(prices)
            max_price = max(prices)
            avg_price = sum(prices) / len(prices)
            
            summary = f"""
📊 Fiyat Özeti / Price Summary:
- En düşük / Lowest: {min_price:.2f} TL
- En yüksek / Highest: {max_price:.2f} TL
- Ortalama / Average: {avg_price:.2f} TL
- Toplam sonuç / Total results: {len(results)}
"""
        else:
            summary = f"Toplam {len(results)} sonuç bulundu. / Found {len(results)} results."
        
        return summary
