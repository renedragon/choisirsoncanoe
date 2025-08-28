import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

def scrape_category_for_products(category_url, headers):
    """Scraper une catégorie pour trouver les produits individuels"""
    
    print(f"\n--- Scraping category: {category_url.split('/')[-2]} ---")
    
    try:
        response = requests.get(category_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        products = []
        
        # Chercher les liens de produits avec différents sélecteurs
        selectors = [
            'h3 a',  # Titres de produits
            'h2 a',  # Titres alternatifs
            '.product-item a',  # Cartes produits
            'a[href*="canoe-"]',  # Liens contenant "canoe-"
            '.woocommerce-loop-product__link',  # WooCommerce
            'a[title*="canoe" i]',  # Liens avec title contenant canoe
        ]
        
        for selector in selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                title = link.get('title', '') or link.text.strip()
                
                if href and title and len(title) > 3:
                    # Filtrer pour avoir des noms de modèles réels
                    title_lower = title.lower()
                    href_lower = href.lower()
                    
                    # Exclure les termes génériques
                    exclude = ['voir tous', 'categories', 'page', 'suivant', 'precedent']
                    if not any(term in title_lower for term in exclude):
                        # Inclure si ça ressemble à un nom de modèle
                        if (('canoe-' in href_lower and len(title) < 50) or 
                            (any(char.isdigit() for char in title) and 'canoe' not in title_lower)):
                            
                            full_url = urljoin("https://www.canoediffusion.com", href)
                            products.append({
                                'url': full_url,
                                'title': title.strip(),
                                'category': category_url.split('/')[-2]
                            })
        
        # Supprimer les doublons
        unique_products = []
        seen_urls = set()
        for product in products:
            if product['url'] not in seen_urls:
                seen_urls.add(product['url'])
                unique_products.append(product)
        
        print(f"  Trouve {len(unique_products)} produits dans cette categorie")
        for product in unique_products[:5]:  # Afficher les 5 premiers
            print(f"    - {product['title']}")
        
        return unique_products
        
    except Exception as e:
        print(f"  Erreur: {e}")
        return []

def find_10_canoe_urls():
    """Trouver 10 URLs de canoës individuels et vérifier leur validité"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Catégories à explorer
    categories = [
        "https://www.canoediffusion.com/canoes/canoe-loisirs/",
        "https://www.canoediffusion.com/canoes/canoe-riviere/",
        "https://www.canoediffusion.com/canoes/canoe-rigide/",
    ]
    
    all_products = []
    
    print("=== Recherche de produits dans les categories ===")
    
    for category_url in categories:
        products = scrape_category_for_products(category_url, headers)
        all_products.extend(products)
        time.sleep(1)  # Pause entre catégories
        
        # Arrêter si on a assez de produits
        if len(all_products) >= 10:
            break
    
    # Prendre les 10 premiers
    test_products = all_products[:10]
    
    print(f"\n=== Test de validite de {len(test_products)} URLs ===")
    
    valid_products = []
    
    for i, product in enumerate(test_products, 1):
        print(f"\n{i:2}. Test: {product['title']}")
        print(f"    URL: {product['url']}")
        
        try:
            # Test HEAD request pour vérifier si l'URL existe
            response = requests.head(product['url'], headers=headers, timeout=10, allow_redirects=True)
            
            status = response.status_code
            if status == 200:
                print(f"    OK - VALIDE (200)")
                valid_products.append(product)
            elif status in [301, 302, 308]:
                final_url = response.url if hasattr(response, 'url') else product['url']
                print(f"    OK - REDIRECTION ({status}) -> {final_url}")
                product['final_url'] = final_url
                valid_products.append(product)
            else:
                print(f"    ERREUR - Code {status}")
                
        except requests.exceptions.RequestException as e:
            print(f"    ERREUR - {str(e)[:50]}...")
        
        time.sleep(0.5)  # Pause entre requêtes
    
    print(f"\n=== RESULTATS FINAUX ===")
    print(f"URLs testees: {len(test_products)}")
    print(f"URLs valides: {len(valid_products)}")
    if len(test_products) > 0:
        print(f"Taux de succes: {len(valid_products)/len(test_products)*100:.1f}%")
    
    if valid_products:
        print(f"\nURLs valides trouvees:")
        for i, product in enumerate(valid_products, 1):
            url = product.get('final_url', product['url'])
            print(f"  {i}. {product['title']} ({product['category']})")
            print(f"     {url}")
    
    return valid_products

if __name__ == "__main__":
    find_10_canoe_urls()