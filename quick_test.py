import requests

def quick_test_urls():
    """Test rapide de quelques URLs avec la structure découverte"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # URLs à tester basées sur la découverte
    test_urls = [
        ("adirondack", "https://www.canoediffusion.com/canoe-esquif-adirondack/"),
        ("echo", "https://www.canoediffusion.com/canoe-esquif-echo/"),
        ("ontario-15", "https://www.canoediffusion.com/canoe-esquif-ontario-15/"),
        ("scout", "https://www.canoediffusion.com/canoe-esquif-scout/"),
        ("prospecteur-15", "https://www.canoediffusion.com/canoe-esquif-prospecteur-15/"),
        ("huron-15", "https://www.canoediffusion.com/canoe-nova-craft-huron-15/"),
        ("ranger-16", "https://www.canoediffusion.com/canoe-swift-ranger-16/"),
        ("triton-16", "https://www.canoediffusion.com/canoe-swift-triton-16/"),
    ]
    
    print("=== Test rapide d'URLs specifiques ===")
    
    valid_count = 0
    
    for model, url in test_urls:
        print(f"{model.upper():<15} -> ", end="")
        
        try:
            response = requests.head(url, headers=headers, timeout=8)
            if response.status_code == 200:
                print("VALIDE (200)")
                valid_count += 1
            elif response.status_code in [301, 302]:
                print(f"REDIRECTION ({response.status_code})")
                valid_count += 1
            else:
                print(f"ERREUR ({response.status_code})")
        except Exception as e:
            print(f"TIMEOUT/ERREUR")
    
    print(f"\nResultat: {valid_count}/{len(test_urls)} URLs valides")
    return valid_count

if __name__ == "__main__":
    quick_test_urls()