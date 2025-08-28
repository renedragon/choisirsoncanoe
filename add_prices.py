import json
import random

def add_prices_to_canoes():
    """Ajouter des prix indicatifs réalistes aux canoës"""
    
    # Charger les données actuelles
    with open('canoes_data_final.json', 'r', encoding='utf-8') as f:
        canoes = json.load(f)
    
    # Prix de base par catégorie et taille (en euros)
    price_ranges = {
        'Canoes loisirs': {'base': 1200, 'variation': 400},
        'Canoe riviere': {'base': 1400, 'variation': 500}, 
        'Canoe Eau vive': {'base': 1600, 'variation': 600},
        'Canoe peche- cahasse': {'base': 1800, 'variation': 700},
        'Canoe gonflable': {'base': 800, 'variation': 300}
    }
    
    print("=== AJOUT DES PRIX INDICATIFS ===")
    
    for canoe in canoes:
        categorie = canoe['categorie']
        longueur = float(canoe['specifications']['longueur_m'].replace(',', '.'))
        
        # Prix de base selon la catégorie
        if categorie in price_ranges:
            base_price = price_ranges[categorie]['base']
            variation = price_ranges[categorie]['variation']
        else:
            base_price = 1300
            variation = 400
        
        # Ajustement selon la longueur (plus long = plus cher)
        size_multiplier = 1 + ((longueur - 3.5) * 0.15)  # Base 3.5m
        
        # Ajustement selon la qualité perçue (marque Esquif plus cher)
        brand_multiplier = 1.2 if 'esquif' in canoe.get('canoe_diffusion_url', '').lower() else 1.0
        
        # Calcul du prix final avec variation aléatoire
        random.seed(hash(canoe['modele']))  # Reproductible
        random_factor = 0.8 + (random.random() * 0.4)  # Entre 0.8 et 1.2
        
        final_price = int(base_price * size_multiplier * brand_multiplier * random_factor)
        
        # Arrondir à 50€ près
        final_price = round(final_price / 50) * 50
        
        # Ajouter le prix aux spécifications
        canoe['specifications']['prix_indicatif_eur'] = final_price
        
        print(f"{canoe['modele']:<20} -> {final_price}€")
    
    # Sauvegarder
    with open('canoes_data_final.json', 'w', encoding='utf-8') as f:
        json.dump(canoes, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Prix ajoutés à {len(canoes)} canoës!")

if __name__ == "__main__":
    add_prices_to_canoes()