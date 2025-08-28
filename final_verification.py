import requests
from bs4 import BeautifulSoup

def verify_final_urls():
    """Vérification finale des URLs trouvées"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # URLs qui ont fonctionné
    valid_urls = [
        ("adirondack", "https://www.canoediffusion.com/canoe-esquif-adirondack/"),
        ("echo", "https://www.canoediffusion.com/canoe-esquif-echo/"),
        ("scout", "https://www.canoediffusion.com/canoe-esquif-scout/"),
        ("prospecteur-15", "https://www.canoediffusion.com/canoe-esquif-prospecteur-15/"),
    ]
    
    print("=== Verification finale du contenu ===")
    
    verified_urls = []
    
    for model, url in valid_urls:
        print(f"\n{model.upper()}:")
        print(f"URL: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extraire titre
                title = soup.find('h1')
                title_text = title.get_text().strip() if title else "Titre non trouve"
                
                # Vérifier correspondance
                page_text = soup.get_text().lower()
                model_in_page = model.lower() in page_text
                
                # Chercher prix
                price_elem = soup.find(string=lambda text: text and '€' in text)
                has_price = price_elem is not None
                
                # Chercher specs
                has_specs = any(word in page_text for word in ['longueur', 'largeur', 'poids', 'profondeur'])
                
                print(f"  Titre: {title_text}")
                print(f"  Modele present: {model_in_page}")
                print(f"  Prix affiche: {has_price}")
                print(f"  Specifications: {has_specs}")
                
                if model_in_page:
                    print(f"  RESULTAT: VALIDE")
                    verified_urls.append((model, url, title_text))
                else:
                    print(f"  RESULTAT: CONTENU INCORRECT")
            
            elif response.status_code in [301, 302]:
                print(f"  Status: REDIRECTION ({response.status_code})")
                print(f"  RESULTAT: VALIDE (redirection)")
                verified_urls.append((model, url, f"Redirection vers {model}"))
            
            else:
                print(f"  Status: ERREUR {response.status_code}")
                
        except Exception as e:
            print(f"  ERREUR: {str(e)[:50]}")
    
    print(f"\n=== URLS DEFINITIVES VALIDEES ===")
    print(f"URLs verifiees: {len(verified_urls)}")
    
    for i, (model, url, title) in enumerate(verified_urls, 1):
        print(f"{i}. {model.upper()}")
        print(f"   URL: {url}")
        print(f"   Titre: {title}")
        print()
    
    return verified_urls

if __name__ == "__main__":
    verify_final_urls()