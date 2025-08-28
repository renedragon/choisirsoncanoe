import json
import re

def generate_canoe_links():
    """Générer les liens vers canoediffusion.com pour chaque canoë"""
    
    # Charger les données avec images
    with open('canoes_data_with_images.json', 'r', encoding='utf-8') as f:
        canoes = json.load(f)
    
    def normalize_name(name):
        """Normaliser le nom du canoë pour créer l'URL"""
        # Convertir en minuscules
        name = name.lower()
        # Remplacer les espaces par des tirets
        name = re.sub(r'\s+', '-', name)
        # Supprimer les caractères spéciaux
        name = re.sub(r'[^\w\-]', '', name)
        # Supprimer les tirets multiples
        name = re.sub(r'-+', '-', name)
        # Supprimer les tirets en début/fin
        name = name.strip('-')
        return name
    
    # Mapping manuel pour les modèles connus
    manual_mappings = {
        'adirondack': 'canoe-adirondack',
        'echo': 'canoe-echo', 
        'ontario-13': 'canoe-ontario-13',
        'scout': 'canoe-scout',
        'ontario-15': 'canoe-ontario-15',
        'prospector-15': 'canoe-prospector-15',
        'prospector-16': 'canoe-prospector-16',
        'champlain': 'canoe-champlain',
        'athabaska': 'canoe-athabaska',
        'yukon': 'canoe-yukon',
        'tripper': 'canoe-tripper',
        'cascadia': 'canoe-cascadia',
        'nova-craft': 'nova-craft',
        'swift': 'swift-canoe',
        'wenonah': 'wenonah-canoe',
        'old-town': 'old-town-canoe'
    }
    
    for canoe in canoes:
        model_name = canoe['modele']
        normalized = normalize_name(model_name)
        
        # Vérifier si on a un mapping manuel
        if normalized in manual_mappings:
            url_slug = manual_mappings[normalized]
        else:
            # Créer l'URL basée sur le nom normalisé
            url_slug = f"canoe-{normalized}"
        
        # Générer l'URL complète
        canoe['canoe_diffusion_url'] = f"https://www.canoediffusion.com/{url_slug}"
        
        # Ajouter aussi quelques URLs alternatives à essayer
        alternatives = [
            f"https://www.canoediffusion.com/kayak-{normalized}",
            f"https://www.canoediffusion.com/produit/{normalized}",
            f"https://www.canoediffusion.com/{normalized}"
        ]
        canoe['alternative_urls'] = alternatives
        
        print(f"OK {model_name} -> {canoe['canoe_diffusion_url']}")
    
    # Sauvegarder les données mises à jour
    with open('canoes_data_with_links.json', 'w', encoding='utf-8') as f:
        json.dump(canoes, f, ensure_ascii=False, indent=2)
    
    print(f"\nOK Liens generes pour {len(canoes)} canoes")
    return canoes

if __name__ == "__main__":
    generate_canoe_links()