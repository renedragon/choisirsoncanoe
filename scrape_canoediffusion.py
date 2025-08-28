import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin

def scrape_canoes_page():
    """Scraper la page principale des canoës sur canoediffusion.com"""
    
    base_url = "https://www.canoediffusion.com"
    canoes_url = "https://www.canoediffusion.com/canoes/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"Scraping {canoes_url}...")
    
    try:
        response = requests.get(canoes_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Chercher les liens vers les canoës individuels
        canoe_links = []
        
        # Différents sélecteurs possibles pour les produits
        selectors = [
            'a[href*="/canoe"]',
            'a[href*="/produit"]',
            '.product-item a',
            '.product-link',
            'a[href*="canoe"]',
        ]
        
        for selector in selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href:
                    full_url = urljoin(base_url, href)
                    title = link.get('title', '') or link.text.strip()
                    
                    # Filtrer pour ne garder que les vraies pages de canoës
                    if ('canoe' in href.lower() or 'produit' in href.lower()) and title:
                        canoe_links.append({
                            'url': full_url,
                            'title': title.strip(),
                            'slug': href
                        })
        
        # Supprimer les doublons
        unique_links = []
        seen_urls = set()
        for link in canoe_links:
            if link['url'] not in seen_urls:
                seen_urls.add(link['url'])
                unique_links.append(link)
        
        print(f"Trouve {len(unique_links)} liens de canoes potentiels")
        
        # Afficher quelques exemples
        for i, link in enumerate(unique_links[:10]):
            print(f"  {i+1}. {link['title']} -> {link['url']}")
        
        return unique_links
        
    except Exception as e:
        print(f"Erreur lors du scraping: {e}")
        return []

def match_canoes_with_links():
    """Matcher nos canoës avec les liens trouvés sur canoediffusion.com"""
    
    # Charger nos données de canoës
    with open('canoes_data_verified.json', 'r', encoding='utf-8') as f:
        our_canoes = json.load(f)
    
    # Scraper les liens du site
    scraped_links = scrape_canoes_page()
    
    if not scraped_links:
        print("Aucun lien trouve, abandon...")
        return
    
    # Matcher les canoës
    updated_canoes = []
    
    for canoe in our_canoes:
        model_name = canoe['modele'].lower()
        best_match = None
        best_score = 0
        
        # Nettoyer le nom pour la comparaison
        model_words = re.findall(r'\w+', model_name)
        
        for link in scraped_links:
            title_lower = link['title'].lower()
            url_lower = link['url'].lower()
            
            # Compter les mots qui matchent
            matches = 0
            for word in model_words:
                if len(word) > 2:  # Ignorer les mots très courts
                    if word in title_lower or word in url_lower:
                        matches += 1
            
            # Score de correspondance
            if model_words:
                match_score = matches / len(model_words)
                if match_score > best_score and match_score >= 0.5:
                    best_score = match_score
                    best_match = link
        
        # Mettre à jour le canoë avec le meilleur match
        if best_match:
            canoe['verified_url'] = best_match['url']
            canoe['verification_score'] = best_score
            canoe['matched_title'] = best_match['title']
            print(f"OK {canoe['modele']} -> {best_match['title']} (score: {best_score:.2f})")
        else:
            print(f"X {canoe['modele']} -> Aucun match trouve")
        
        updated_canoes.append(canoe)
    
    # Sauvegarder les résultats
    with open('canoes_data_scraped.json', 'w', encoding='utf-8') as f:
        json.dump(updated_canoes, f, ensure_ascii=False, indent=2)
    
    # Statistiques
    matched = sum(1 for c in updated_canoes if c.get('verified_url') and c.get('verification_score', 0) >= 0.5)
    print(f"\nResultats du matching:")
    print(f"  Matches trouves: {matched}/{len(updated_canoes)}")
    print(f"  Pourcentage: {(matched/len(updated_canoes))*100:.1f}%")
    
    return updated_canoes

if __name__ == "__main__":
    print("=== Scraping de canoediffusion.com ===")
    match_canoes_with_links()