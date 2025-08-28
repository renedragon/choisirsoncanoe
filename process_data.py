import pandas as pd
import json

def process_canoe_data():
    excel_file = r'C:\Users\Minerve\Downloads\Tableau_aptitude_canoes_CORRIGE.xlsx'
    df = pd.read_excel(excel_file)
    
    # Filtrer les lignes avec des données de canoës réels
    df_clean = df[df['Unnamed: 1'].notna()].copy()
    
    # Renommer les colonnes pour plus de clarté
    df_clean.columns = [
        'Categorie', 'Modele', 'Longueur_pieds', 'Longueur_m', 'Poids_kg',
        'Niveau_pagayeur', 'Caractere_sportif', 'Possibilite_chargement',
        'Vitesse', 'Maniabilite', 'Stabilite_primaire', 'Stabilite_secondaire',
        'Stabilite_directionnelle', 'Etang_lac', 'Riviere_classe_I_II',
        'Riviere_classe_III_IV', 'Torrent', 'Canot_camping', 'Expedition_sportive',
        'Surf', 'Nb_max_pagayeurs'
    ]
    
    # Ajouter la catégorie à chaque canoë
    current_category = None
    for idx, row in df_clean.iterrows():
        if pd.notna(row['Categorie']):
            current_category = row['Categorie']
        df_clean.at[idx, 'Categorie'] = current_category
    
    # Nettoyer les données
    df_clean = df_clean[df_clean['Modele'].notna()]
    
    # Convertir en format approprié
    canoes_data = []
    for _, row in df_clean.iterrows():
        canoe = {
            'categorie': row['Categorie'],
            'modele': row['Modele'],
            'specifications': {
                'longueur_pieds': str(row['Longueur_pieds']),
                'longueur_m': str(row['Longueur_m']),
                'poids_kg': str(row['Poids_kg']),
                'nb_max_pagayeurs': int(row['Nb_max_pagayeurs']) if pd.notna(row['Nb_max_pagayeurs']) else 2
            },
            'caracteristiques': {
                'niveau_pagayeur': float(row['Niveau_pagayeur']) if pd.notna(row['Niveau_pagayeur']) else 0,
                'caractere_sportif': float(row['Caractere_sportif']) if pd.notna(row['Caractere_sportif']) else 0,
                'possibilite_chargement': float(row['Possibilite_chargement']) if pd.notna(row['Possibilite_chargement']) else 0,
                'vitesse': float(row['Vitesse']) if pd.notna(row['Vitesse']) else 0,
                'maniabilite': float(row['Maniabilite']) if pd.notna(row['Maniabilite']) else 0,
                'stabilite_primaire': float(row['Stabilite_primaire']) if pd.notna(row['Stabilite_primaire']) else 0,
                'stabilite_secondaire': float(row['Stabilite_secondaire']) if pd.notna(row['Stabilite_secondaire']) else 0,
                'stabilite_directionnelle': float(row['Stabilite_directionnelle']) if pd.notna(row['Stabilite_directionnelle']) else 0
            },
            'aptitudes': {
                'etang_lac': float(row['Etang_lac']) if pd.notna(row['Etang_lac']) else 0,
                'riviere_classe_I_II': float(row['Riviere_classe_I_II']) if pd.notna(row['Riviere_classe_I_II']) else 0,
                'riviere_classe_III_IV': float(row['Riviere_classe_III_IV']) if pd.notna(row['Riviere_classe_III_IV']) else 0,
                'torrent': float(row['Torrent']) if pd.notna(row['Torrent']) else 0,
                'canot_camping': float(row['Canot_camping']) if pd.notna(row['Canot_camping']) else 0,
                'expedition_sportive': float(row['Expedition_sportive']) if pd.notna(row['Expedition_sportive']) else 0,
                'surf': float(row['Surf']) if pd.notna(row['Surf']) else 0
            }
        }
        canoes_data.append(canoe)
    
    # Sauvegarder les données
    with open('canoes_data.json', 'w', encoding='utf-8') as f:
        json.dump(canoes_data, f, ensure_ascii=False, indent=2)
    
    print(f"Traitement terminé ! {len(canoes_data)} canoës trouvés.")
    print(f"Catégories: {df_clean['Categorie'].unique().tolist()}")
    
    return canoes_data

if __name__ == "__main__":
    data = process_canoe_data()