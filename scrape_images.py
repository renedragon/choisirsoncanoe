import requests
from bs4 import BeautifulSoup
import json
import time
import os

def search_canoe_image(canoe_name):
    """Rechercher une image de canoë sur canoediffusion.com"""
    
    # Nettoyer le nom pour la recherche
    search_name = canoe_name.lower().replace(' ', '-')
    
    # URLs possibles à essayer
    urls_to_try = [
        f"https://www.canoediffusion.com/canoe-{search_name}",
        f"https://www.canoediffusion.com/kayak-{search_name}",
        f"https://www.canoediffusion.com/{search_name}"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for url in urls_to_try:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Chercher l'image principale du produit
                img_selectors = [
                    'img.product-main-image',
                    'img.product-image',
                    'div.product-image img',
                    'div.image-product img',
                    'img[itemprop="image"]'
                ]
                
                for selector in img_selectors:
                    img = soup.select_one(selector)
                    if img and img.get('src'):
                        img_url = img['src']
                        if not img_url.startswith('http'):
                            img_url = 'https://www.canoediffusion.com' + img_url
                        return img_url
        except:
            continue
    
    # Si pas trouvé, retourner une image par défaut ou None
    return None

def update_canoes_with_images():
    """Mettre à jour les données des canoës avec les URLs des images"""
    
    # Charger les données existantes
    with open('canoes_data.json', 'r', encoding='utf-8') as f:
        canoes = json.load(f)
    
    print(f"Recherche d'images pour {len(canoes)} canoës...")
    
    # Images par défaut par catégorie
    default_images = {
        'Canoes loisirs': '🛶',
        'Canoe riviere': '🚣',
        'Canoe Eau vive': '💨',
        'Canoe peche- cahasse': '🎣',
        'Canoe gonflable': '🎈'
    }
    
    for i, canoe in enumerate(canoes):
        model_name = canoe['modele']
        print(f"Recherche {i+1}/{len(canoes)}: {model_name}")
        
        # Chercher l'image
        img_url = search_canoe_image(model_name)
        
        if img_url:
            canoe['image_url'] = img_url
            print(f"  ✓ Image trouvée")
        else:
            # Utiliser emoji par défaut selon la catégorie
            canoe['image_url'] = None
            canoe['emoji'] = default_images.get(canoe['categorie'], '🛶')
            print(f"  × Pas d'image - emoji utilisé")
        
        # Petite pause pour ne pas surcharger le serveur
        time.sleep(0.5)
    
    # Sauvegarder les données mises à jour
    with open('canoes_data_with_images.json', 'w', encoding='utf-8') as f:
        json.dump(canoes, f, ensure_ascii=False, indent=2)
    
    print("\nTerminé ! Données sauvegardées dans canoes_data_with_images.json")
    return canoes

if __name__ == "__main__":
    # Pour l'instant, on va utiliser des placeholders/emojis
    # Le scraping réel peut être activé si nécessaire
    with open('canoes_data.json', 'r', encoding='utf-8') as f:
        canoes = json.load(f)
    
    default_images = {
        'Canoes loisirs': '🛶',
        'Canoe riviere': '🚣',
        'Canoe Eau vive': '💨',
        'Canoe peche- cahasse': '🎣',
        'Canoe gonflable': '🎈'
    }
    
    for canoe in canoes:
        canoe['image_url'] = None
        canoe['emoji'] = default_images.get(canoe['categorie'], '🛶')
    
    with open('canoes_data_with_images.json', 'w', encoding='utf-8') as f:
        json.dump(canoes, f, ensure_ascii=False, indent=2)
    
    print("Données avec emojis sauvegardées!")