import requests
from bs4 import BeautifulSoup
import time

def inspect_site_properly():
    """Inspecter le site correctement - menu, sitemap, structure WooCommerce"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("=== INSPECTION METHODIQUE DU SITE ===")
    
    # 1. VÉRIFIER LE SITEMAP
    print("\n1. VÉRIFICATION DU SITEMAP")
    sitemap_urls = [
        "https://www.canoediffusion.com/sitemap.xml",
        "https://www.canoediffusion.com/sitemap_index.xml",
        "https://www.canoediffusion.com/wp-sitemap.xml",
        "https://www.canoediffusion.com/robots.txt"
    ]
    
    for url in sitemap_urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"   ✓ {url} - TROUVÉ ({len(response.text)} caractères)")
                
                if 'sitemap' in url and '.xml' in url:
                    # Analyser le sitemap XML
                    if 'produit' in response.text.lower():
                        print("   → Contient des URLs /produit/")
                        
                        # Extraire quelques URLs produit
                        lines = response.text.split('\n')
                        product_urls = [line.strip() for line in lines if '/produit/' in line and 'canoe' in line.lower()]
                        
                        if product_urls:
                            print("   → URLs produit trouvées dans sitemap:")
                            for i, url_line in enumerate(product_urls[:5]):
                                # Extraire l'URL entre les balises
                                start = url_line.find('<loc>') + 5
                                end = url_line.find('</loc>')
                                if start > 4 and end > start:
                                    clean_url = url_line[start:end]
                                    print(f"      {i+1}. {clean_url}")
                
                elif 'robots.txt' in url:
                    print(f"   Contenu robots.txt:")
                    for line in response.text.split('\n')[:10]:
                        if line.strip():
                            print(f"      {line}")
                            
            else:
                print(f"   ✗ {url} - Code {response.status_code}")
        except Exception as e:
            print(f"   ✗ {url} - Erreur: {str(e)[:30]}")
    
    # 2. INSPECTER LA NAVIGATION/MENU
    print(f"\n2. INSPECTION DU MENU PRINCIPAL")
    
    try:
        response = requests.get("https://www.canoediffusion.com/canoes/", headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Chercher les éléments de navigation
        nav_selectors = ['nav', '.menu', '.navigation', '#menu', '.main-menu']
        
        for selector in nav_selectors:
            nav_elements = soup.select(selector)
            if nav_elements:
                print(f"   Navigation trouvée ({selector}): {len(nav_elements)} éléments")
                
                for nav in nav_elements[:2]:  # Analyser les 2 premiers
                    links = nav.find_all('a', href=True)
                    print(f"   → {len(links)} liens dans la navigation")
                    
                    product_links = [link for link in links if '/produit/' in link.get('href', '')]
                    if product_links:
                        print(f"   → {len(product_links)} liens /produit/ trouvés:")
                        for link in product_links[:5]:
                            href = link.get('href')
                            text = link.get_text().strip()
                            print(f"      • {text} -> {href}")
        
    except Exception as e:
        print(f"   Erreur navigation: {e}")
    
    # 3. EXPLORER UNE PAGE CATÉGORIE EN DÉTAIL
    print(f"\n3. EXPLORATION D'UNE PAGE CATÉGORIE")
    
    try:
        cat_url = "https://www.canoediffusion.com/canoes/canoe-loisirs/"
        response = requests.get(cat_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print(f"   Page catégorie: {cat_url}")
        print(f"   Status: {response.status_code}")
        
        # Chercher les produits WooCommerce
        woo_selectors = [
            '.woocommerce-loop-product__link',
            'a[href*="/produit/"]',
            '.product-item a',
            '.wc-block-grid__product-link',
            'h2.woocommerce-loop-product__title a'
        ]
        
        all_product_links = []
        
        for selector in woo_selectors:
            links = soup.select(selector)
            if links:
                print(f"   Sélecteur '{selector}': {len(links)} liens")
                
                for link in links:
                    href = link.get('href', '')
                    title = link.get('title', '') or link.get_text().strip()
                    
                    if href and '/produit/' in href:
                        all_product_links.append((title, href))
        
        # Supprimer les doublons et afficher
        unique_links = list(set(all_product_links))
        print(f"   → {len(unique_links)} liens produit uniques trouvés:")
        
        for i, (title, href) in enumerate(unique_links[:10], 1):
            print(f"      {i:2}. {title[:30]:<30} -> {href}")
            
    except Exception as e:
        print(f"   Erreur catégorie: {e}")
    
    return True

def test_discovered_products():
    """Tester les URLs /produit/ découvertes"""
    
    # URLs trouvées lors de l'inspection (à remplir avec les résultats)
    discovered_urls = []
    
    if not discovered_urls:
        print("\n4. PAS D'URLS DÉCOUVERTES - Test de patterns courants")
        
        # Tester quelques patterns basés sur nos modèles
        test_patterns = [
            "adirondack",
            "echo",
            "ontario",
            "scout",
            "prospecteur",
            "canoe-adirondack",
            "canoe-echo",
            "esquif-adirondack",
            "esquif-echo"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        for pattern in test_patterns:
            url = f"https://www.canoediffusion.com/produit/{pattern}/"
            
            try:
                response = requests.head(url, headers=headers, timeout=5)
                status = response.status_code
                print(f"   {pattern:<20} -> /produit/{pattern}/ -> {status}")
                
                if status == 200:
                    print("      ★ TROUVÉ!")
                elif status in [301, 302]:
                    print(f"      → Redirection")
                    
            except Exception as e:
                print(f"   {pattern:<20} -> Erreur")
            
            time.sleep(0.3)

if __name__ == "__main__":
    inspect_site_properly()
    test_discovered_products()