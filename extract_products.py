import requests
from bs4 import BeautifulSoup
import re

def extract_product_urls():
    """Extraire les URLs /produit/ sans problème d'encodage"""
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    category_url = "https://www.canoediffusion.com/canoes/canoe-loisirs/"
    
    try:
        response = requests.get(category_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraire tous les liens
            links = soup.find_all('a', href=True)
            
            product_urls = []
            
            for link in links:
                href = link.get('href')
                if href and '/produit/' in href:
                    # Nettoyer l'URL
                    if href.startswith('http'):
                        full_url = href
                    else:
                        full_url = f"https://www.canoediffusion.com{href}"
                    
                    product_urls.append(full_url)
            
            # Supprimer doublons
            unique_urls = list(set(product_urls))
            
            print(f"URLs /produit/ trouvees: {len(unique_urls)}")
            
            # Extraire les slugs
            slugs = []
            for url in unique_urls:
                # Extraire le slug entre /produit/ et le prochain /
                match = re.search(r'/produit/([^/?]+)', url)
                if match:
                    slug = match.group(1)
                    slugs.append(slug)
                    print(f"  {slug}")
            
            return slugs
            
    except Exception as e:
        print(f"Erreur: {e}")
        return []

def test_our_models_with_slugs():
    """Tester nos modèles avec les patterns de slugs trouvés"""
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # Nos modèles
    our_models = [
        "adirondack", "echo", "ontario-13", "scout", "ontario-15", 
        "prospecteur-15", "huron-15", "ranger-16", "triton-16", "prospecteur-16"
    ]
    
    print(f"\nTest de nos modeles avec /produit/:")
    
    valid_urls = []
    
    for model in our_models:
        # Tester différents patterns
        test_patterns = [
            model,
            f"canoe-{model}",
            f"esquif-{model}",
            f"canoe-esquif-{model}",
            model.replace('-', ''),
        ]
        
        found = False
        
        for pattern in test_patterns:
            if found:
                break
                
            url = f"https://www.canoediffusion.com/produit/{pattern}/"
            
            try:
                response = requests.head(url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    print(f"  {model:<15} -> TROUVE: /produit/{pattern}/")
                    valid_urls.append((model, url))
                    found = True
                    
            except:
                pass
        
        if not found:
            print(f"  {model:<15} -> PAS TROUVE")
    
    return valid_urls

def verify_found_products(valid_urls):
    """Vérifier le contenu des URLs trouvées"""
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    print(f"\nVerification du contenu:")
    
    verified_urls = []
    
    for model, url in valid_urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Vérifier si c'est bien une page de canoë
                content = response.text.lower()
                
                # Tests de base
                is_product = 'product' in content or 'produit' in content
                is_canoe = 'canoe' in content or 'canoe' in content
                has_model = model.replace('-', '') in content
                
                print(f"  {model}: Produit={is_product}, Canoe={is_canoe}, Modele={has_model}")
                
                if is_product and is_canoe:
                    verified_urls.append((model, url))
                    print(f"    -> VALIDE: {url}")
                    
        except Exception as e:
            print(f"  {model}: ERREUR - {str(e)[:30]}")
    
    return verified_urls

if __name__ == "__main__":
    # 1. Extraire les URLs /produit/ de la page catégorie
    slugs = extract_product_urls()
    
    # 2. Tester nos modèles
    valid_urls = test_our_models_with_slugs()
    
    # 3. Vérifier le contenu
    if valid_urls:
        verified_urls = verify_found_products(valid_urls)
        
        print(f"\n=== RESULTATS FINAUX ===")
        print(f"URLs /produit/ verifiees: {len(verified_urls)}")
        
        for model, url in verified_urls:
            print(f"  {model.upper()}: {url}")
    else:
        print(f"\nAucune URL /produit/ valide trouvee pour nos modeles")