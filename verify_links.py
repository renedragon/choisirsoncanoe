import requests
from bs4 import BeautifulSoup
import json
import time
import re

def verify_canoe_links():
    """Vérifier les liens vers canoediffusion.com en scrapant les pages"""
    
    # Charger les données avec liens
    with open('canoes_data_with_links.json', 'r', encoding='utf-8') as f:
        canoes = json.load(f)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    verified_canoes = []
    
    for i, canoe in enumerate(canoes):
        print(f"Verification {i+1}/{len(canoes)}: {canoe['modele']}")
        
        model_name = canoe['modele'].lower()
        found_valid_link = False
        
        # URLs à tester
        urls_to_test = [canoe['canoe_diffusion_url']] + canoe.get('alternative_urls', [])
        
        for url in urls_to_test:
            try:
                print(f"  Test: {url}")
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Chercher le titre de la page
                    title = soup.find('title')
                    page_title = title.text.lower() if title else ""
                    
                    # Chercher les éléments h1, h2 qui peuvent contenir le nom du produit
                    headings = soup.find_all(['h1', 'h2', 'h3'])
                    page_content = ' '.join([h.text.lower() for h in headings])
                    
                    # Vérifier si le nom du modèle apparaît dans le contenu
                    model_words = re.findall(r'\w+', model_name)
                    matches = 0
                    
                    for word in model_words:
                        if len(word) > 2 and (word in page_title or word in page_content):
                            matches += 1
                    
                    # Si au moins la moitié des mots du modèle sont trouvés
                    match_ratio = matches / len(model_words) if model_words else 0
                    
                    if match_ratio >= 0.5:
                        print(f"  ✓ Lien valide trouvé: {url}")
                        canoe['verified_url'] = url
                        canoe['verification_score'] = match_ratio
                        found_valid_link = True
                        break
                    else:
                        print(f"  × Pas de correspondance (score: {match_ratio:.2f})")
                
                time.sleep(1)  # Pause pour ne pas surcharger le serveur
                
            except Exception as e:
                print(f"  × Erreur: {e}")
                continue
        
        if not found_valid_link:
            print(f"  ! Aucun lien valide trouvé pour {canoe['modele']}")
            # Essayer de trouver sur la page de recherche
            search_url = f"https://www.canoediffusion.com/search?q={canoe['modele'].replace(' ', '+')}"
            try:
                response = requests.get(search_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Chercher les liens de produits dans les résultats
                    product_links = soup.find_all('a', href=re.compile(r'/canoe|/kayak|/produit'))
                    
                    for link in product_links[:3]:  # Tester les 3 premiers résultats
                        href = link.get('href')
                        if href and not href.startswith('http'):
                            href = 'https://www.canoediffusion.com' + href
                        
                        link_text = link.text.lower()
                        if any(word in link_text for word in model_words if len(word) > 2):
                            canoe['verified_url'] = href
                            canoe['verification_score'] = 0.8
                            print(f"  ✓ Trouvé via recherche: {href}")
                            found_valid_link = True
                            break
            except:
                pass
        
        if not found_valid_link:
            canoe['verified_url'] = None
            canoe['verification_score'] = 0
        
        verified_canoes.append(canoe)
    
    # Sauvegarder les données vérifiées
    with open('canoes_data_verified.json', 'w', encoding='utf-8') as f:
        json.dump(verified_canoes, f, ensure_ascii=False, indent=2)
    
    # Statistiques
    valid_links = sum(1 for c in verified_canoes if c.get('verified_url'))
    print(f"\nVerification terminee:")
    print(f"  Liens valides: {valid_links}/{len(verified_canoes)}")
    print(f"  Pourcentage: {(valid_links/len(verified_canoes))*100:.1f}%")
    
    return verified_canoes

if __name__ == "__main__":
    # Pour des tests rapides, on va d'abord tester seulement quelques canoës
    print("Verification des liens canoediffusion.com...")
    print("ATTENTION: Ceci va prendre du temps pour eviter de surcharger le serveur")
    
    response = input("Voulez-vous continuer? (y/n): ")
    if response.lower() == 'y':
        verify_canoe_links()
    else:
        print("Verification annulee")