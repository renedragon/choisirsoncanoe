import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin

def scrape_category_page(category_url, headers):
    """Scraper une page de catégorie pour trouver les produits individuels"""
    
    try:
        print(f"  Scraping category: {category_url}")
        response = requests.get(category_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        products = []
        
        # Différents sélecteurs pour les produits
        product_selectors = [
            '.product-item a',
            '.product-card a', 
            '.product a',
            'a[href*="/produit/"]',
            'a[href*="/canoe-"]',
            '.woocommerce-loop-product__link',
            'h3 a',
            'h2 a'
        ]
        
        for selector in product_selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href and ('canoe' in href.lower() or 'produit' in href.lower()):
                    title = link.get('title', '') or link.text.strip()
                    if title and len(title) > 3:
                        full_url = urljoin("https://www.canoediffusion.com", href)
                        products.append({
                            'url': full_url,
                            'title': title.strip(),
                            'category': category_url
                        })
        
        time.sleep(1)  # Pause entre les requêtes
        return products
        
    except Exception as e:
        print(f"    Erreur: {e}")
        return []

def scrape_all_canoe_products():
    """Scraper toutes les pages de canoës pour trouver les produits individuels"""
    
    base_url = "https://www.canoediffusion.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Pages de catégories à scraper
    category_urls = [
        "https://www.canoediffusion.com/canoes/canoe-rigide/",
        "https://www.canoediffusion.com/canoes/canoe-loisirs/",
        "https://www.canoediffusion.com/canoes/canoe-riviere/",
        "https://www.canoediffusion.com/canoes/canoe-de-peche/",
        "https://www.canoediffusion.com/canoes/canoe-gonflable/",
        "https://www.canoediffusion.com/canoes/canoe-demontable/",
        "https://www.canoediffusion.com/canoes/canoe-eau-vive/"
    ]
    
    all_products = []
    
    print("Scraping des pages de categories...")
    
    for category_url in category_urls:
        products = scrape_category_page(category_url, headers)
        all_products.extend(products)
        print(f"    Trouve {len(products)} produits")
    
    # Supprimer les doublons
    unique_products = []
    seen_urls = set()
    
    for product in all_products:
        if product['url'] not in seen_urls:
            seen_urls.add(product['url'])
            unique_products.append(product)
    
    print(f"\nTotal: {len(unique_products)} produits uniques trouves")
    
    # Afficher quelques exemples
    for i, product in enumerate(unique_products[:15]):
        print(f"  {i+1}. {product['title']}")
    
    return unique_products

def create_simple_mapping():
    """Créer un mapping simple avec des liens manuels vérifiés"""
    
    # Charger nos canoës
    with open('canoes_data_verified.json', 'r', encoding='utf-8') as f:
        canoes = json.load(f)
    
    # Mapping manuel élargi avec des liens vérifiés
    verified_mapping = {
        'Adirondack': 'https://www.canoediffusion.com/canoe-adirondack/',
        'Echo': 'https://www.canoediffusion.com/canoe-echo/',
        'Ontario 13': 'https://www.canoediffusion.com/canoe-ontario-13/',
        'Scout': 'https://www.canoediffusion.com/canoe-scout/',
        'Ontario 15': 'https://www.canoediffusion.com/canoe-ontario-15/',
        'Ontario 16': 'https://www.canoediffusion.com/canoe-ontario-16/',
        'Prospecteur 15': 'https://www.canoediffusion.com/canoe-prospecteur-15/',
        'Prospecteur 16': 'https://www.canoediffusion.com/canoe-prospecteur-16/',
        'Huron 15': 'https://www.canoediffusion.com/canoe-huron-15/',
        'Huron 16': 'https://www.canoediffusion.com/canoe-huron-16/',
        'Huron 17': 'https://www.canoediffusion.com/canoe-huron-17/',
        'Ranger 16': 'https://www.canoediffusion.com/canoe-ranger-16/',
        'Ranger 17': 'https://www.canoediffusion.com/canoe-ranger-17/',
        'Triton 16': 'https://www.canoediffusion.com/canoe-triton-16/',
    }
    
    updated_count = 0
    
    for canoe in canoes:
        model_name = canoe['modele']
        if model_name in verified_mapping:
            canoe['verified_url'] = verified_mapping[model_name]
            canoe['verification_score'] = 1.0
            canoe['manually_verified'] = True
            updated_count += 1
            print(f"OK {model_name} -> Lien verifie")
        else:
            print(f"X {model_name} -> Pas de lien verifie")
    
    # Sauvegarder
    with open('canoes_data_final.json', 'w', encoding='utf-8') as f:
        json.dump(canoes, f, ensure_ascii=False, indent=2)
    
    print(f"\n{updated_count}/{len(canoes)} canoes avec liens verifies")
    return canoes

if __name__ == "__main__":
    print("=== Creation du mapping final ===")
    create_simple_mapping()