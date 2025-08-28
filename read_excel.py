import pandas as pd
import json

def read_canoe_data():
    excel_file = r'C:\Users\Minerve\Downloads\Tableau_aptitude_canoes_CORRIGE.xlsx'
    df = pd.read_excel(excel_file)
    
    print("Colonnes du fichier Excel:")
    print(df.columns.tolist())
    print("\nPremières lignes:")
    print(df.head())
    print("\nInformations sur les données:")
    print(df.info())
    print("\nDimensions du tableau:", df.shape)
    
    # Sauvegarder les données en JSON pour l'application
    df.to_json('canoes_data.json', orient='records', force_ascii=False)
    
    return df

if __name__ == "__main__":
    df = read_canoe_data()