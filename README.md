# 🛶 ChoisirSonCanoe

![Flask](https://img.shields.io/badge/Flask-3.0.0-blue?logo=flask)
![Python](https://img.shields.io/badge/Python-3.8+-green?logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Canoes](https://img.shields.io/badge/Canoes-43-orange)
![Responsive](https://img.shields.io/badge/Responsive-✓-brightgreen)

Une application web interactive pour choisir le canoë parfait selon vos besoins et préférences.

## 🎥 Démo Live

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/renedragon/choisirsoncanoe)

**🚀 Déploiement Vercel :**
1. Cliquez sur "Deploy with Vercel" ☝️
2. Connectez votre compte GitHub
3. L'app se déploie automatiquement !

**💻 Développement local :**
1. Clone le repo : `git clone https://github.com/renedragon/choisirsoncanoe.git`
2. Install : `pip install -r requirements.txt`
3. Run : `python app.py`
4. Ouvrez : http://127.0.0.1:5000

**🔐 Admin Demo :** `/admin/login`
- User: `admin` / Pass: `canoe2025!`

## ✨ Fonctionnalités

### 🎯 Interface Utilisateur
- **Recommandations personnalisées** basées sur le niveau, l'usage et les préférences
- **Design kawaii** avec animations de bulles et couleurs pastel
- **Fiches détaillées** de canoës avec évaluations étoilées
- **Catalogue complet** avec filtres par catégorie
- **Interface responsive** (mobile, tablette, desktop)

### 🔧 Administration
- **Authentification sécurisée** avec identifiants pré-configurés
- **CRUD complet** : Ajouter, modifier, supprimer des canoës
- **Interface intuitive** avec modales d'édition
- **Statistiques** en temps réel
- **Filtres et recherche** dans le dashboard admin

### 📊 Données
- **43 canoës** répertoriés avec spécifications complètes
- **5 catégories** : Loisirs, Rivière, Eau vive, Pêche-chasse, Gonflable
- **Prix indicatifs** calculés automatiquement
- **Liens directs** vers les produits sur CanoesDiffusion.com

## 🚀 Installation

### Prérequis
- Python 3.8+
- Flask

### Étapes
1. **Cloner le repo**
   ```bash
   git clone https://github.com/VOTRE_USERNAME/choisirsoncanoe.git
   cd choisirsoncanoe
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   python app.py
   ```

4. **Accéder à l'app**
   - Interface utilisateur : http://127.0.0.1:5000
   - Administration : http://127.0.0.1:5000/admin/login

## 🔑 Accès Admin (Démo)

**Identifiants pré-configurés :**
- Username: `admin`
- Password: `canoe2025!`

Alternative :
- Username: `minerve`
- Password: `admin123`

## 🏗️ Structure du Projet

```
choisirsoncanoe/
├── app.py                      # Application Flask principale
├── add_prices.py              # Script d'ajout de prix automatique
├── canoes_data_final.json     # Base de données des canoës
├── templates/
│   ├── index.html             # Interface utilisateur
│   ├── admin_login.html       # Page de connexion admin
│   └── admin_dashboard.html   # Dashboard d'administration
├── static/
│   ├── style.css             # Styles CSS avec responsive
│   ├── script.js             # Logique frontend
│   └── admin.js              # Logique admin
└── requirements.txt          # Dépendances Python
```

## 💡 Algorithme de Recommandation

L'app utilise un système de scoring sophistiqué (0-10 points) :

1. **Score niveau** (2.5 pts max) - Proximité avec le niveau utilisateur
2. **Score usage** (2.5 pts max) - Aptitude pour l'activité choisie  
3. **Score préférences** (5 pts max) - Correspondance avec les caractéristiques souhaitées

**Caractéristiques évaluées :**
- Vitesse ⚡
- Stabilité primaire 🏗️
- Maniabilité 🎯
- Possibilité de chargement 🎒

## 📱 Responsive Design

- **Desktop** : Interface complète avec grilles multi-colonnes
- **Tablette (≤768px)** : Navigation adaptée, colonnes réduites
- **Mobile (≤480px)** : Interface verticale optimisée

## 🎨 Design System

**Palette de couleurs :**
- Gradients pastel : `#a8edea → #fed6e3 → #ffd3b6`
- Accent bleu-vert : `#4fc3f7`
- Texte foncé : `#2c5530`

**Animations :**
- Bulles flottantes en arrière-plan
- Transitions fluides sur les cartes
- Effets hover interactifs

## 🔄 Données Produits

**Sources :**
- Tableau Excel original avec 43 canoës
- URLs vérifiées via sitemap XML de CanoesDiffusion.com
- Prix calculés selon algorithme propriétaire

**Catégories disponibles :**
- Canoes loisirs
- Canoe riviere  
- Canoe Eau vive
- Canoe peche-chasse
- Canoe gonflable

## 🛠️ Technologies

- **Backend :** Flask (Python)
- **Frontend :** HTML5, CSS3, JavaScript vanilla
- **Data :** JSON
- **Authentification :** Sessions Flask
- **Design :** CSS Grid, Flexbox, Responsive

## 📈 Fonctionnalités Futures

- [ ] Synchronisation WooCommerce
- [ ] API REST complète
- [ ] Système de favoris
- [ ] Comparateur de canoës
- [ ] Notifications admin
- [ ] Export PDF des recommandations

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou proposer une PR.

## 📄 Licence

Projet développé pour [CanoesDiffusion.com](https://www.canoediffusion.com)

---

*Développé avec ❤️ et Claude Code*