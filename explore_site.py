import requests
from bs4 import BeautifulSoup
import re

def explore_site_structure():
    """Explorer la vraie structure du site canoediffusion.com"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("=== Exploration de la structure du site ===")
    
    # 1. Explorer la page principale des canoës
    main_url = "https://www.canoediffusion.com/canoes/"
    print(f"1. Page principale: {main_url}")
    
    try:
        response = requests.get(main_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Chercher tous les liens vers des produits
        all_links = soup.find_all('a', href=True)
        product_links = []
        
        for link in all_links:
            href = link.get('href')
            text = link.text.strip()
            
            if href and text and len(text) < 100:
                # Chercher des patterns de produits
                if any(pattern in href.lower() for pattern in ['/produit/', 'canoe-', 'kayak-']) and len(text) > 3:
                    full_url = href if href.startswith('http') else f"https://www.canoediffusion.com{href}"
                    product_links.append({'url': full_url, 'text': text})
        
        print(f"   Trouve {len(product_links)} liens potentiels")
        
        # Afficher les premiers liens trouvés
        for i, link in enumerate(product_links[:10], 1):
            print(f"   {i:2}. {link['text'][:30]:<30} -> {link['url']}")
        
    except Exception as e:
        print(f"   Erreur: {e}")
    
    # 2. Tester quelques URLs de base communes
    print(f"\n2. Test d'URLs communes WooCommerce")
    
    test_patterns = [
        "https://www.canoediffusion.com/boutique/",
        "https://www.canoediffusion.com/shop/", 
        "https://www.canoediffusion.com/produits/",
        "https://www.canoediffusion.com/product/",
        "https://www.canoediffusion.com/canoe/adirondack/",
        "https://www.canoediffusion.com/adirondack/",
    ]
    
    for url in test_patterns:
        try:
            response = requests.head(url, headers=headers, timeout=5)
            status = "OK" if response.status_code == 200 else f"Code {response.status_code}"
            print(f"   {status:<10} {url}")
        except:
            print(f"   ERREUR     {url}")
    
    # 3. Rechercher via leur moteur de recherche
    print(f"\n3. Test du moteur de recherche interne")
    
    search_url = "https://www.canoediffusion.com/"
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Chercher un champ de recherche
        search_forms = soup.find_all('form')
        search_inputs = soup.find_all('input', {'type': 'search'})
        
        print(f"   Formulaires trouves: {len(search_forms)}")
        print(f"   Champs de recherche: {len(search_inputs)}")
        
        if search_inputs:
            for inp in search_inputs[:2]:
                name = inp.get('name', 'inconnu')
                placeholder = inp.get('placeholder', '')
                print(f"     Champ: name='{name}', placeholder='{placeholder}'")
        
    except Exception as e:
        print(f"   Erreur: {e}")
    
    # 4. Examiner une page de catégorie spécifique
    print(f"\n4. Examen d'une page de categorie")
    
    category_url = "https://www.canoediffusion.com/canoes/canoe-loisirs/"
    try:
        response = requests.get(category_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Chercher des éléments de produits WooCommerce
        woo_selectors = [
            '.woocommerce-loop-product__link',
            '.product-item',
            '.product',
            'h2.woocommerce-loop-product__title',
            '.wc-block-grid__product'
        ]
        
        found_products = []
        
        for selector in woo_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"   Selector '{selector}': {len(elements)} elements")
                for elem in elements[:3]:
                    text = elem.get_text().strip()[:50] if elem.get_text() else "Pas de texte"
                    href = elem.get('href', '') if elem.name == 'a' else ''
                    if href or text:
                        found_products.append({'text': text, 'href': href})
        
        if found_products:
            print(f"   Produits trouves dans la categorie:")
            for i, prod in enumerate(found_products[:5], 1):
                print(f"     {i}. {prod['text']}")
                if prod['href']:
                    print(f"        -> {prod['href']}")
        
    except Exception as e:
        print(f"   Erreur: {e}")

def test_search_functionality():
    """Tester la fonctionnalité de recherche du site"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"\n=== Test de recherche sur le site ===")
    
    # URLs de recherche possibles
    search_patterns = [
        "https://www.canoediffusion.com/?s=adirondack",
        "https://www.canoediffusion.com/search/?q=adirondack", 
        "https://www.canoediffusion.com/?post_type=product&s=adirondack",
    ]
    
    for pattern in search_patterns:
        print(f"Test: {pattern}")
        try:
            response = requests.get(pattern, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Chercher des résultats de recherche
                results = soup.find_all(['h2', 'h3'], string=re.compile(r'adirondack', re.IGNORECASE))
                links = soup.find_all('a', string=re.compile(r'adirondack', re.IGNORECASE))
                
                print(f"   Status: 200, Resultats: {len(results)}, Liens: {len(links)}")
                
                if links:
                    for link in links[:2]:
                        href = link.get('href', '')
                        text = link.get_text().strip()
                        print(f"     -> {text} : {href}")
            else:
                print(f"   Status: {response.status_code}")
        except Exception as e:
            print(f"   Erreur: {str(e)[:50]}")

if __name__ == "__main__":
    explore_site_structure()
    test_search_functionality()