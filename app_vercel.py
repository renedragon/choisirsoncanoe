from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os

# Configuration Flask pour Vercel
app = Flask(__name__)
app.secret_key = 'choisirsoncanoe_admin_2025_secret_key'

# Identifiants admin
ADMIN_USERS = {'admin': 'canoe2025!', 'minerve': 'admin123'}

# Charger les données
def load_canoes():
    try:
        with open('canoes_data_final.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

canoes = load_canoes()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/canoes')
def get_canoes():
    return jsonify(canoes)

@app.route('/api/categories')
def get_categories():
    categories = list(set([c['categorie'] for c in canoes]))
    return jsonify(categories)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    criteria = request.json
    niveau = criteria.get('niveau', 3)
    usage = criteria.get('usage', 'etang_lac')
    nb_personnes = criteria.get('nb_personnes', 1)
    categorie_filter = criteria.get('categorie', '')
    
    pref_vitesse = criteria.get('pref_vitesse', 3)
    pref_stabilite = criteria.get('pref_stabilite', 3)
    pref_maniabilite = criteria.get('pref_maniabilite', 3)
    pref_chargement = criteria.get('pref_chargement', 3)
    
    scored_canoes = []
    for canoe in canoes:
        if categorie_filter and canoe['categorie'] != categorie_filter:
            continue
        if canoe['specifications']['nb_max_pagayeurs'] < nb_personnes:
            continue
            
        total_score = 0
        
        # Score niveau (2.5 pts max)
        niveau_diff = abs(canoe['caracteristiques']['niveau_pagayeur'] - niveau)
        niveau_score = max(0, (5 - niveau_diff) / 5) * 2.5
        total_score += niveau_score
        
        # Score usage (2.5 pts max)
        if usage in canoe['aptitudes']:
            usage_score = (canoe['aptitudes'][usage] / 5) * 2.5
            total_score += usage_score
        
        # Score préférences (5 pts max)
        char_scores = [
            canoe['caracteristiques']['vitesse'] * pref_vitesse,
            canoe['caracteristiques']['stabilite_primaire'] * pref_stabilite,
            canoe['caracteristiques']['maniabilite'] * pref_maniabilite,
            canoe['caracteristiques']['possibilite_chargement'] * pref_chargement
        ]
        char_total = sum(char_scores)
        char_normalized = min(5, (char_total / 25) * 5)
        total_score += char_normalized
        
        final_score = min(10, total_score)
        scored_canoes.append({**canoe, 'score': round(final_score, 2)})
    
    scored_canoes.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(scored_canoes[:5])

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in ADMIN_USERS and ADMIN_USERS[username] == password:
            session['admin_logged_in'] = True
            return redirect('/admin')
        return render_template('admin_login.html', error='Identifiants incorrects')
    return render_template('admin_login.html')

@app.route('/admin')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return redirect('/admin/login')
    categories = list(set([c['categorie'] for c in canoes]))
    return render_template('admin_dashboard.html', canoes=canoes, categories=categories)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/')

# Pour Vercel
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)