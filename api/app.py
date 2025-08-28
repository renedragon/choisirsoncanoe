from flask import Flask, jsonify, render_template_string
import json
import os

app = Flask(__name__)

# Template HTML minimal intégré
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛶 ChoisirSonCanoe</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #a8edea, #fed6e3); margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .canoe-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .canoe-card { background: white; border-radius: 15px; padding: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .status { text-align: center; padding: 20px; background: white; border-radius: 15px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛶 ChoisirSonCanoe</h1>
            <p>Application de recommandation de canoës</p>
        </div>
        <div class="status">
            <h2>✅ Application déployée avec succès sur Vercel !</h2>
            <p>Version simplifiée fonctionnelle</p>
        </div>
        <div id="canoes-info"></div>
    </div>
    <script>
        fetch('/api/status')
            .then(r => r.json())
            .then(data => {
                document.getElementById('canoes-info').innerHTML = 
                    '<div class="status"><h3>📊 Statistiques</h3><p>Canoës chargés: ' + data.canoes_count + '</p><p>Status: ' + data.status + '</p></div>';
            })
            .catch(e => {
                document.getElementById('canoes-info').innerHTML = 
                    '<div class="status"><h3>❌ Erreur</h3><p>Impossible de charger les données</p></div>';
            });
    </script>
</body>
</html>
"""

# Données de test intégrées
SAMPLE_CANOES = [
    {
        "modele": "Adirondack",
        "categorie": "Canoes loisirs",
        "specifications": {"longueur_m": "4.37", "nb_max_pagayeurs": 2},
        "caracteristiques": {"niveau_pagayeur": 2, "vitesse": 3, "stabilite_primaire": 4, "maniabilite": 3, "possibilite_chargement": 4},
        "aptitudes": {"etang_lac": 5, "riviere_calme": 4, "riviere_mouvementee": 2, "eau_vive": 1}
    }
]

# Charger les vraies données si possible
def load_canoes():
    try:
        # Plusieurs tentatives de chargement
        paths = [
            'canoes_data_final.json',
            '../canoes_data_final.json',
            'canoes_data.json',
            '../canoes_data.json'
        ]
        
        for path in paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data:
                        return data
            except:
                continue
        
        # Si aucun fichier trouvé, utiliser les données de test
        return SAMPLE_CANOES
    except:
        return SAMPLE_CANOES

canoes = load_canoes()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'OK',
        'canoes_count': len(canoes),
        'message': 'Application fonctionnelle'
    })

@app.route('/api/canoes')
def get_canoes():
    return jsonify(canoes[:10])  # Limiter à 10 pour éviter les timeouts

@app.route('/api/categories')
def get_categories():
    try:
        categories = list(set([c.get('categorie', 'Unknown') for c in canoes]))
        return jsonify(categories)
    except:
        return jsonify(['Canoes loisirs'])

# Point d'entrée pour Vercel
def handler(event, context):
    return app(event, context)

# Export pour Vercel
application = app

if __name__ == '__main__':
    app.run(debug=True)