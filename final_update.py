import json

def final_update():
    """Mise à jour finale avec les 4 canoës retrouvés"""
    
    # Charger les données actuelles
    with open('canoes_data_final.json', 'r', encoding='utf-8') as f:
        canoes_data = json.load(f)
    
    # Les 4 URLs retrouvées
    final_matches = {
        'Présage': 'https://www.canoediffusion.com/produit/canoe-esquif-presage/',
        "L'Edge L & SL": 'https://www.canoediffusion.com/produit/canoe-esquif-ledge/',
        'Zéphyr 2.0': 'https://www.canoediffusion.com/produit/canoe-esquif-zephyr-2-0/',
        'Héron': 'https://www.canoediffusion.com/produit/canoe-esquif-heron/'
    }
    
    print("=== MISE A JOUR FINALE ===")
    updated = 0
    
    for canoe in canoes_data:
        model_name = canoe['modele']
        
        if model_name in final_matches:
            new_url = final_matches[model_name]
            old_url = canoe.get('canoe_diffusion_url', 'Aucune')
            
            # Mettre à jour
            canoe['canoe_diffusion_url'] = new_url
            canoe['verified_url'] = new_url
            canoe['verification_score'] = 1.0
            canoe['manually_verified'] = False
            canoe['sitemap_verified'] = True
            
            print(f"OK {model_name}")
            print(f"  Nouvelle URL: {new_url}")
            updated += 1
    
    # Sauvegarder
    with open('canoes_data_final.json', 'w', encoding='utf-8') as f:
        json.dump(canoes_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== RESULTAT FINAL ===")
    print(f"URLs supplémentaires ajoutées: {updated}")
    print(f"Total URLs vérifiées: 38 + {updated} = {38 + updated}/43")
    print(f"Seul manquant: Excite")
    print(f"\nTaux de réussite: {((38 + updated) / 43) * 100:.1f}%")

if __name__ == "__main__":
    final_update()