import json

def update_canoe_urls():
    """Mettre à jour les URLs des canoës avec les correspondances trouvées dans le sitemap"""
    
    # Charger les données existantes
    with open('canoes_data_final.json', 'r', encoding='utf-8') as f:
        canoes_data = json.load(f)
    
    # Charger les correspondances du sitemap
    with open('sitemap_matches.json', 'r', encoding='utf-8') as f:
        sitemap_matches = json.load(f)
    
    # Créer un dictionnaire des correspondances par modèle
    matches_dict = {}
    for match in sitemap_matches:
        matches_dict[match['our_model']] = {
            'url': match['matched_url'],
            'score': match['score']
        }
    
    print("=== MISE A JOUR DES URLS ===")
    updated_count = 0
    
    # Mettre à jour chaque canoë
    for canoe in canoes_data:
        model_name = canoe['modele']
        
        if model_name in matches_dict:
            match_info = matches_dict[model_name]
            old_url = canoe.get('canoe_diffusion_url', 'Aucune')
            new_url = match_info['url']
            score = match_info['score']
            
            # Mettre à jour les URLs
            canoe['canoe_diffusion_url'] = new_url
            canoe['verified_url'] = new_url
            canoe['verification_score'] = score
            canoe['manually_verified'] = False
            canoe['sitemap_verified'] = True
            
            print(f"OK {model_name}")
            print(f"  Ancienne URL: {old_url}")
            print(f"  Nouvelle URL: {new_url}")
            print(f"  Score: {score*100:.0f}%")
            print()
            
            updated_count += 1
        else:
            print(f"XX {model_name} - Pas de correspondance dans le sitemap")
    
    # Sauvegarder les données mises à jour
    with open('canoes_data_updated.json', 'w', encoding='utf-8') as f:
        json.dump(canoes_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== RÉSUMÉ ===")
    print(f"Total canoës: {len(canoes_data)}")
    print(f"URLs mises à jour: {updated_count}")
    print(f"Non trouvés: {len(canoes_data) - updated_count}")
    print(f"\nDonnées sauvegardées dans: canoes_data_updated.json")
    
    return canoes_data

if __name__ == "__main__":
    update_canoe_urls()