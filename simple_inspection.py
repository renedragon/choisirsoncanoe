import requests
from bs4 import BeautifulSoup

def check_sitemap():
    """Vérifier le sitemap pour trouver les URLs /produit/"""
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    print("=== VERIFICATION SITEMAP ===")
    
    sitemap_url = "https://www.canoediffusion.com/sitemap.xml"
    
    try:
        response = requests.get(sitemap_url, headers=headers, timeout=10)
        print(f"Sitemap status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            print(f"Taille du sitemap: {len(content)} caracteres")
            
            # Chercher les URLs /produit/
            lines = content.split('\n')
            product_urls = []
            
            for line in lines:
                if '/produit/' in line and 'canoe' in line.lower():
                    # Extraire l'URL
                    start = line.find('<loc>') + 5
                    end = line.find('</loc>')
                    if start > 4 and end > start:
                        url = line[start:end]
                        product_urls.append(url)
            
            print(f"URLs /produit/ avec 'canoe' trouvees: {len(product_urls)}")
            
            for i, url in enumerate(product_urls[:10], 1):
                # Extraire le nom du produit
                product_name = url.split('/produit/')[-1].replace('/', '')
                print(f"  {i:2}. {product_name} -> {url}")
            
            return product_urls
        
    except Exception as e:
        print(f"Erreur sitemap: {e}")
    
    return []

def explore_category_products():
    """Explorer une page catégorie pour trouver les vrais liens produit"""
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    print(f"\n=== EXPLORATION PAGE CATEGORIE ===")
    
    category_url = "https://www.canoediffusion.com/canoes/canoe-loisirs/"
    
    try:
        response = requests.get(category_url, headers=headers, timeout=15)
        print(f"Page categorie status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Chercher tous les liens
            all_links = soup.find_all('a', href=True)
            product_links = []
            
            for link in all_links:
                href = link.get('href')
                text = link.get_text().strip()
                
                # Filtrer pour les liens /produit/
                if href and '/produit/' in href:
                    if text and len(text) < 100 and len(text) > 3:
                        product_links.append((text, href))
            
            # Supprimer doublons
            unique_products = list(set(product_links))
            print(f"Produits /produit/ trouves: {len(unique_products)}")
            
            for i, (title, url) in enumerate(unique_products[:15], 1):
                product_slug = url.split('/produit/')[-1].replace('/', '')
                print(f"  {i:2}. {title[:35]:<35} -> /produit/{product_slug}")
            
            return unique_products
            
    except Exception as e:
        print(f"Erreur exploration: {e}")
    
    return []

def test_specific_products(product_slugs):
    """Tester des URLs /produit/ spécifiques"""
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    print(f"\n=== TEST URLS /PRODUIT/ SPECIFIQUES ===")
    
    valid_products = []
    
    for slug in product_slugs[:10]:  # Tester seulement les 10 premiers
        url = f"https://www.canoediffusion.com/produit/{slug}/"
        
        try:
            response = requests.head(url, headers=headers, timeout=8)
            status = response.status_code
            
            result = "OK" if status == 200 else f"Code {status}"
            print(f"  {slug:<25} -> {result}")
            
            if status == 200:
                valid_products.append((slug, url))
                
        except Exception as e:
            print(f"  {slug:<25} -> ERREUR")
    
    print(f"\nURLs valides trouvees: {len(valid_products)}")
    return valid_products

def verify_product_content(valid_products):
    """Vérifier que le contenu des pages correspond aux canoës"""
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    print(f"\n=== VERIFICATION CONTENU PRODUITS ===")
    
    for slug, url in valid_products[:3]:  # Vérifier seulement les 3 premiers
        print(f"\nVerification: {slug}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Titre produit
                title_elem = soup.find('h1')
                title = title_elem.get_text().strip() if title_elem else "Titre non trouve"
                
                # Vérifier si c'est bien un canoë
                page_text = soup.get_text().lower()
                is_canoe = 'canoe' in page_text or 'canoe' in page_text
                
                # Chercher des specs
                has_specs = any(word in page_text for word in ['longueur', 'largeur', 'poids', 'places'])
                
                # Chercher prix
                has_price = '$' in page_text or 'prix' in page_text or 'cout' in page_text
                
                print(f"  Titre: {title}")
                print(f"  Est un canoe: {is_canoe}")
                print(f"  A des specs: {has_specs}")
                print(f"  A un prix: {has_price}")
                
        except Exception as e:
            print(f"  Erreur verification: {str(e)[:50]}")

if __name__ == "__main__":
    # 1. Vérifier sitemap
    sitemap_products = check_sitemap()
    
    # 2. Explorer catégorie
    category_products = explore_category_products()
    
    # 3. Extraire les slugs de produits
    all_slugs = []
    
    if sitemap_products:
        for url in sitemap_products:
            slug = url.split('/produit/')[-1].replace('/', '')
            if slug:
                all_slugs.append(slug)
    
    if category_products:
        for title, url in category_products:
            slug = url.split('/produit/')[-1].replace('/', '')
            if slug and slug not in all_slugs:
                all_slugs.append(slug)
    
    print(f"\nSlugs uniques collectes: {len(all_slugs)}")
    
    # 4. Tester les URLs
    if all_slugs:
        valid_products = test_specific_products(all_slugs)
        
        # 5. Vérifier le contenu
        if valid_products:
            verify_product_content(valid_products)