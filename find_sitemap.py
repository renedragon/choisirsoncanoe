import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
import re

def find_sitemap():
    """Trouver le vrai sitemap du site avec toutes les URLs"""
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    print("=== RECHERCHE DU SITEMAP COMPLET ===")
    
    # URLs de sitemap possibles
    sitemap_urls = [
        "https://www.canoediffusion.com/sitemap.xml",
        "https://www.canoediffusion.com/sitemap_index.xml", 
        "https://www.canoediffusion.com/wp-sitemap.xml",
        "https://www.canoediffusion.com/wp-sitemap-posts-product-1.xml",
        "https://www.canoediffusion.com/product-sitemap.xml",
        "https://www.canoediffusion.com/woocommerce-sitemap.xml"
    ]
    
    # Vérifier robots.txt pour trouver le sitemap
    print("1. Verification robots.txt...")
    try:
        response = requests.get("https://www.canoediffusion.com/robots.txt", headers=headers, timeout=10)
        if response.status_code == 200:
            print("   robots.txt trouve")
            for line in response.text.split('\n'):
                if 'sitemap' in line.lower():
                    sitemap_url = line.split(': ')[-1].strip()
                    if sitemap_url not in sitemap_urls:
                        sitemap_urls.append(sitemap_url)
                        print(f"   Sitemap trouve dans robots.txt: {sitemap_url}")
    except:
        print("   robots.txt inaccessible")
    
    # Tester chaque URL de sitemap
    print(f"\n2. Test de {len(sitemap_urls)} URLs de sitemap...")
    
    valid_sitemaps = []
    
    for sitemap_url in sitemap_urls:
        try:
            response = requests.get(sitemap_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                size = len(response.text)
                print(f"   OK {sitemap_url} ({size} caracteres)")
                
                # Compter les URLs /produit/
                produit_count = response.text.count('/produit/')
                canoe_count = response.text.lower().count('canoe')
                
                print(f"      URLs /produit/: {produit_count}")  
                print(f"      Mentions 'canoe': {canoe_count}")
                
                if produit_count > 0:
                    valid_sitemaps.append((sitemap_url, response.text, produit_count))
                
            else:
                print(f"   ERREUR {sitemap_url} (Code {response.status_code})")
                
        except Exception as e:
            print(f"   ERREUR {sitemap_url} ({str(e)[:30]})")
    
    return valid_sitemaps

def extract_product_urls_from_sitemap(sitemap_content):
    """Extraire toutes les URLs /produit/ du sitemap XML"""
    
    print(f"\n=== EXTRACTION URLs PRODUIT DU SITEMAP ===")
    
    product_urls = []
    
    try:
        # Parser le XML
        root = ET.fromstring(sitemap_content)
        
        # Trouver le namespace
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Extraire les URLs
        for url_elem in root.findall('.//ns:url', namespaces):
            loc_elem = url_elem.find('ns:loc', namespaces)
            if loc_elem is not None:
                url = loc_elem.text
                if url and '/produit/' in url:
                    product_urls.append(url)
        
        print(f"URLs /produit/ extraites du XML: {len(product_urls)}")
        
    except ET.XMLParser.ParseError:
        print("   Erreur parsing XML, utilisation regex...")
        
        # Fallback avec regex si XML malformé
        url_pattern = r'<loc>(.*?/produit/.*?)</loc>'
        matches = re.findall(url_pattern, sitemap_content)
        product_urls = matches
        
        print(f"URLs /produit/ extraites par regex: {len(product_urls)}")
    
    # Filtrer pour les canoës seulement
    canoe_urls = []
    for url in product_urls:
        url_lower = url.lower()
        if any(keyword in url_lower for keyword in ['canoe', 'canoe', 'kayak']):
            canoe_urls.append(url)
    
    print(f"URLs de canoes filtrees: {len(canoe_urls)}")
    
    return canoe_urls

def analyze_canoe_urls(canoe_urls):
    """Analyser les URLs de canoës trouvées"""
    
    print(f"\n=== ANALYSE DES URLs DE CANOES ===")
    
    # Extraire les slugs/noms
    canoe_info = []
    
    for url in canoe_urls:
        # Extraire le slug
        slug_match = re.search(r'/produit/([^/?]+)', url)
        if slug_match:
            slug = slug_match.group(1)
            
            # Nettoyer le nom pour l'analyse
            clean_name = slug.replace('canoe-', '').replace('-', ' ')
            
            canoe_info.append({
                'url': url,
                'slug': slug,
                'clean_name': clean_name
            })
    
    print(f"Total canoes analyses: {len(canoe_info)}")
    print(f"\nPremiers 20 canoes trouves:")
    
    for i, info in enumerate(canoe_info[:20], 1):
        print(f"  {i:2}. {info['clean_name']:<25} -> /produit/{info['slug']}")
    
    if len(canoe_info) > 20:
        print(f"  ... et {len(canoe_info) - 20} autres")
    
    return canoe_info

def match_with_our_models(canoe_info):
    """Matcher les URLs trouvées avec nos 43 modèles"""
    
    print(f"\n=== MATCHING AVEC NOS 43 MODELES ===")
    
    # Charger nos modèles
    try:
        with open('canoes_data_final.json', 'r', encoding='utf-8') as f:
            import json
            our_canoes = json.load(f)
    except:
        # Fallback avec liste manuelle
        our_models = [
            'Adirondack', 'Echo', 'Ontario 13', 'Scout', 'Ontario 15', 'Ontario 16',
            'Huron 15', 'Huron 16', 'Triton 16', 'Ranger 16', 'Ranger 17', 'Huron 17',
            'Vertige aventure', 'Vertige X avent.', 'Pocket Canyon', 'Prospecteur 15',
            'PakCanoe 15', 'PakCanoe 16', 'Prospecteur 16', 'Presage', 'Prospecteur Sport',
            'Canyon', 'Prospecteur 17', 'PakCanoe 17', 'Miramichi 18', 'Miramichi 20',
            'Excite', 'Extasy', "L'Edge L & SL", 'Ocoee', 'Vertige', 'Raven', 'Zephyr 2.0',
            'Spark', 'Vertige X', 'Heron', 'Mallard XL', 'Cargo 17', 'Rangeley 15',
            'Rangeley 17', 'Palava', 'Scout River', 'Baraka'
        ]
        our_canoes = [{'modele': model} for model in our_models]
    
    print(f"Nos modeles: {len(our_canoes)}")
    print(f"URLs site trouvees: {len(canoe_info)}")
    
    matches = []
    
    for canoe in our_canoes:
        model_name = canoe['modele'].lower()
        best_match = None
        best_score = 0
        
        # Nettoyer le nom de notre modèle
        model_words = re.findall(r'\w+', model_name)
        
        for site_canoe in canoe_info:
            site_name = site_canoe['clean_name'].lower()
            site_slug = site_canoe['slug'].lower()
            
            # Compter les correspondances de mots
            matches_count = 0
            for word in model_words:
                if len(word) > 1:  # Ignorer les mots trop courts
                    if word in site_name or word in site_slug:
                        matches_count += 1
            
            # Score de correspondance
            if model_words:
                score = matches_count / len(model_words)
                if score > best_score and score >= 0.5:  # Au moins 50% de correspondance
                    best_score = score
                    best_match = site_canoe
        
        if best_match:
            matches.append({
                'our_model': canoe['modele'],
                'matched_url': best_match['url'],
                'matched_name': best_match['clean_name'],
                'score': best_score
            })
            print(f"  OK {canoe['modele']:<20} -> {best_match['clean_name']:<25} ({best_score*100:.0f}%)")
        else:
            print(f"  XX {canoe['modele']:<20} -> Pas de correspondance")
    
    print(f"\nRESULTAT: {len(matches)}/{len(our_canoes)} modeles matches")
    return matches

if __name__ == "__main__":
    # 1. Trouver les sitemaps
    sitemaps = find_sitemap()
    
    if not sitemaps:
        print("Aucun sitemap avec URLs /produit/ trouve")
        exit()
    
    # 2. Utiliser le sitemap avec le plus d'URLs produit
    best_sitemap = max(sitemaps, key=lambda x: x[2])  # x[2] = produit_count
    print(f"\nUtilisation du meilleur sitemap: {best_sitemap[0]}")
    
    # 3. Extraire les URLs de canoës
    canoe_urls = extract_product_urls_from_sitemap(best_sitemap[1])
    
    if canoe_urls:
        # 4. Analyser les URLs
        canoe_info = analyze_canoe_urls(canoe_urls)
        
        # 5. Matcher avec nos modèles
        matches = match_with_our_models(canoe_info)
        
        # 6. Sauvegarder les résultats
        if matches:
            import json
            with open('sitemap_matches.json', 'w', encoding='utf-8') as f:
                json.dump(matches, f, ensure_ascii=False, indent=2)
            print(f"\nResultats sauvegardes dans sitemap_matches.json")
    else:
        print("Aucune URL de canoe trouvee dans les sitemaps")