import pandas as pd

excel_file = r'C:\Users\Minerve\Downloads\Tableau_aptitude_canoes_CORRIGE.xlsx'
df = pd.read_excel(excel_file)

# Vérifier le nombre max de pagayeurs
print("Analyse du nombre de pagayeurs:")
print(df['Nb. max de pagayeurs'].value_counts().sort_index())
print(f"\nMaximum: {df['Nb. max de pagayeurs'].max()}")
print(f"Minimum: {df['Nb. max de pagayeurs'].min()}")

# Vérifier les catégories
print("\n\nCatégories disponibles:")
categories = df[df['Unnamed: 0'].notna()]['Unnamed: 0'].unique()
print(categories)