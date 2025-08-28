from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'choisirsoncanoe_admin_2025_secret_key'

# Identifiants admin préenregistrés
ADMIN_USERS = {
    'admin': 'canoe2025!',
    'minerve': 'admin123'
}

# Charger les données des canoës avec liens finaux
def load_canoes_data():
    # Chercher le fichier de données dans plusieurs emplacements
    possible_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'canoes_data_final.json'),
        os.path.join(os.path.dirname(__file__), '..', 'canoes_data.json'),
        'canoes_data_final.json',
        'canoes_data.json'
    ]
    
    for path in possible_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            continue
    
    # Si aucun fichier n'est trouvé, retourner des données par défaut
    return []

canoes = load_canoes_data()

# Décorateur pour protéger les routes admin
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Fonction pour sauvegarder les données (désactivée sur Vercel - read-only)
def save_canoes_data():
    # Sur Vercel, le filesystem est read-only en production
    # Cette fonction pourrait être adaptée pour utiliser une base de données
    pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/canoes')
def get_canoes():
    return jsonify(canoes)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    criteria = request.json
    
    # Récupérer les préférences de l'utilisateur
    niveau = criteria.get('niveau', 3)
    usage = criteria.get('usage', 'etang_lac')
    nb_personnes = criteria.get('nb_personnes', 1)
    categorie_filter = criteria.get('categorie', '')
    
    # Préférences pour les caractéristiques
    pref_vitesse = criteria.get('pref_vitesse', 3)
    pref_stabilite = criteria.get('pref_stabilite', 3)
    pref_maniabilite = criteria.get('pref_maniabilite', 3)
    pref_chargement = criteria.get('pref_chargement', 3)
    
    # Calculer le score pour chaque canoë (score sur 10, converti en % dans le frontend)
    scored_canoes = []
    for canoe in canoes:
        total_score = 0
        max_possible_score = 10
        
        # Filtrer par catégorie si spécifiée
        if categorie_filter and canoe['categorie'] != categorie_filter:
            continue
        
        # Vérifier si le canoë convient au nombre de personnes
        if canoe['specifications']['nb_max_pagayeurs'] < nb_personnes:
            continue
        
        # 1. Score niveau (0-2.5 points) - Plus on est proche du niveau, mieux c'est
        niveau_diff = abs(canoe['caracteristiques']['niveau_pagayeur'] - niveau)
        niveau_score = max(0, (5 - niveau_diff) / 5) * 2.5
        total_score += niveau_score
        
        # 2. Score usage (0-2.5 points) - Aptitude pour l'usage prévu
        if usage in canoe['aptitudes']:
            usage_score = (canoe['aptitudes'][usage] / 5) * 2.5
            total_score += usage_score
        
        # 3. Score préférences (0-5 points total, 1.25 par caractéristique)
        char_scores = [
            canoe['caracteristiques']['vitesse'] * pref_vitesse,
            canoe['caracteristiques']['stabilite_primaire'] * pref_stabilite,
            canoe['caracteristiques']['maniabilite'] * pref_maniabilite,
            canoe['caracteristiques']['possibilite_chargement'] * pref_chargement
        ]
        
        # Normaliser les scores de caractéristiques (max 5*5=25, on veut max 5)
        char_total = sum(char_scores)
        char_normalized = min(5, (char_total / 25) * 5)
        total_score += char_normalized
        
        # S'assurer que le score ne dépasse jamais 10
        final_score = min(max_possible_score, total_score)
        
        scored_canoes.append({
            **canoe,
            'score': round(final_score, 2)
        })
    
    # Trier par score décroissant
    scored_canoes.sort(key=lambda x: x['score'], reverse=True)
    
    # Retourner les 5 meilleurs
    return jsonify(scored_canoes[:5])

@app.route('/api/categories')
def get_categories():
    categories = list(set([canoe['categorie'] for canoe in canoes]))
    return jsonify(categories)

# Routes admin
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in ADMIN_USERS and ADMIN_USERS[username] == password:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Identifiants incorrects')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    categories = list(set([canoe['categorie'] for canoe in canoes]))
    return render_template('admin_dashboard.html', canoes=canoes, categories=categories)

# API admin pour CRUD (mode lecture seule sur Vercel)
@app.route('/admin/api/canoe/<string:modele>')
@login_required
def get_canoe(modele):
    canoe = next((c for c in canoes if c['modele'] == modele), None)
    if canoe:
        return jsonify(canoe)
    return jsonify({'error': 'Canoë non trouvé'}), 404

@app.route('/admin/api/canoe', methods=['POST'])
@login_required
def add_canoe():
    return jsonify({'error': 'Fonctionnalité désactivée en production (filesystem read-only)'}), 403

@app.route('/admin/api/canoe/<string:modele>', methods=['PUT'])
@login_required
def update_canoe(modele):
    return jsonify({'error': 'Fonctionnalité désactivée en production (filesystem read-only)'}), 403

@app.route('/admin/api/canoe/<string:modele>', methods=['DELETE'])
@login_required
def delete_canoe(modele):
    return jsonify({'error': 'Fonctionnalité désactivée en production (filesystem read-only)'}), 403

# Point d'entrée pour Vercel
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Pour Vercel
def handler(request):
    return app(request)

# Export pour Vercel
def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)