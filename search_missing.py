import json
import re

def search_missing_canoes():
    """Chercher les 5 canoës manquants avec des patterns alternatifs"""
    
    # Charger les correspondances trouvées
    with open('sitemap_matches.json', 'r', encoding='utf-8') as f:
        sitemap_matches = json.load(f)
    
    # Charger toutes les URLs du sitemap
    # On va relire le fichier pour avoir toutes les URLs
    found_models = [match['our_model'] for match in sitemap_matches]
    
    # Nos 43 modèles complets
    all_models = [
        'Adirondack', 'Echo', 'Ontario 13', 'Scout', 'Ontario 15', 'Ontario 16',
        'Huron 15', 'Huron 16', 'Triton 16', 'Ranger 16', 'Ranger 17', 'Huron 17',
        'Vertige aventure', 'Vertige X avent.', 'Pocket Canyon', 'Prospecteur 15',
        'PakCanoe 15', 'PakCanoe 16', 'Prospecteur 16', 'Présage', 'Prospecteur Sport',
        'Canyon', 'Prospecteur 17', 'PakCanoe 17', 'Miramichi 18', 'Miramichi 20',
        'Excite', 'Extasy', "L'Edge L & SL", 'Ocoee', 'Vertige', 'Raven', 'Zéphyr 2.0',
        'Spark', 'Vertige X', 'Héron', 'Mallard XL', 'Cargo 17', 'Rangeley 15',
        'Rangeley 17', 'Palava', 'Scout River', 'Baraka'
    ]
    
    # Trouver les manquants
    missing = []
    for model in all_models:
        if model not in found_models:
            missing.append(model)
    
    print("=== LES 5 CANOES MANQUANTS ===")
    for i, model in enumerate(missing, 1):
        print(f"{i}. {model}")
    
    # Maintenant, cherchons ces modèles avec des patterns alternatifs dans le sitemap
    print(f"\n=== RECHERCHE ALTERNATIVE DANS LE SITEMAP ===")
    
    # Charger le contenu du sitemap
    import requests
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get("https://www.canoediffusion.com/wp-sitemap-posts-product-1.xml", 
                               headers=headers, timeout=10)
        sitemap_content = response.text.lower()
        
        for model in missing:
            print(f"\nRecherche pour {model}:")
            
            # Patterns de recherche alternatifs
            search_patterns = [
                model.lower().replace(' ', '-'),
                model.lower().replace(' ', ''),
                model.lower().replace("'", ''),
                model.lower().replace('é', 'e').replace('è', 'e'),
                'presage' if model == 'Présage' else '',
                'zephyr' if model == 'Zéphyr 2.0' else '',
                'heron' if model == 'Héron' else '',
                'edge' if "L'Edge" in model else '',
                'ledge' if "L'Edge" in model else ''
            ]
            
            found_urls = []
            for pattern in search_patterns:
                if pattern and len(pattern) > 2:
                    # Chercher dans le sitemap
                    lines = sitemap_content.split('\n')
                    for line in lines:
                        if pattern in line and '/produit/' in line:
                            # Extraire l'URL
                            start = line.find('<loc>') + 5
                            end = line.find('</loc>')
                            if start > 4 and end > start:
                                url = line[start:end]
                                if url not in found_urls:
                                    found_urls.append(url)
            
            if found_urls:
                print(f"  TROUVE {len(found_urls)} correspondance(s):")
                for url in found_urls[:3]:  # Limiter à 3
                    slug = url.split('/produit/')[-1].replace('/', '')
                    print(f"    - {slug}")
                    print(f"      {url}")
            else:
                print(f"  AUCUNE correspondance trouvée")
    
    except Exception as e:
        print(f"Erreur lors de la recherche: {e}")

if __name__ == "__main__":
    search_missing_canoes()