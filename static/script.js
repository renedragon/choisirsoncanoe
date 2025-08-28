let allCanoes = [];

// Charger tous les canoës au démarrage
document.addEventListener('DOMContentLoaded', async () => {
    await loadAllCanoes();
    await loadCategories();
    setupEventListeners();
    updateRangeValues();
});

// Charger tous les canoës
async function loadAllCanoes() {
    try {
        const response = await fetch('/api/canoes');
        allCanoes = await response.json();
        displayAllCanoes(allCanoes);
    } catch (error) {
        console.error('Erreur lors du chargement des canoës:', error);
    }
}

// Charger les catégories
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const categories = await response.json();
        
        const categoryFilter = document.getElementById('categoryFilter');
        const categoryIcons = {
            'Canoes loisirs': '🏖️',
            'Canoe riviere': '🏞️',
            'Canoe Eau vive': '💨',
            'Canoe peche- cahasse': '🎣',
            'Canoe gonflable': '🎈'
        };
        
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = `${categoryIcons[category] || '🛶'} ${category}`;
            categoryFilter.appendChild(option);
        });
    } catch (error) {
        console.error('Erreur lors du chargement des catégories:', error);
    }
}

// Configurer les écouteurs d'événements
function setupEventListeners() {
    // Formulaire de recherche
    document.getElementById('criteriaForm').addEventListener('submit', handleFormSubmit);
    
    // Mise à jour des valeurs des sliders avec animation
    const sliders = document.querySelectorAll('input[type="range"]');
    sliders.forEach(slider => {
        slider.addEventListener('input', (e) => {
            updateRangeValue(e.target);
        });
    });
    
    // Filtres pour tous les canoës
    document.getElementById('searchInput').addEventListener('input', filterCanoes);
    document.getElementById('categoryFilter').addEventListener('change', filterCanoes);
}

// Mise à jour d'une valeur de slider
function updateRangeValue(slider) {
    const valueDisplay = slider.parentElement.querySelector('.value-display');
    if (valueDisplay) {
        valueDisplay.textContent = slider.value;
        // Animation du cercle de valeur
        valueDisplay.parentElement.style.transform = 'scale(1.2)';
        setTimeout(() => {
            valueDisplay.parentElement.style.transform = 'scale(1)';
        }, 200);
    }
}

// Mise à jour de toutes les valeurs des sliders
function updateRangeValues() {
    const sliders = document.querySelectorAll('input[type="range"]');
    sliders.forEach(slider => {
        updateRangeValue(slider);
    });
}

// Gérer la soumission du formulaire
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const criteria = {
        niveau: parseInt(formData.get('niveau')),
        usage: formData.get('usage'),
        nb_personnes: parseInt(formData.get('nb_personnes')),
        categorie: formData.get('categorie'),
        pref_vitesse: parseInt(formData.get('pref_vitesse')),
        pref_stabilite: parseInt(formData.get('pref_stabilite')),
        pref_maniabilite: parseInt(formData.get('pref_maniabilite')),
        pref_chargement: parseInt(formData.get('pref_chargement'))
    };
    
    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(criteria)
        });
        
        const recommendations = await response.json();
        displayRecommendations(recommendations);
    } catch (error) {
        console.error('Erreur lors de la recherche de recommandations:', error);
    }
}

// Afficher les recommandations
function displayRecommendations(canoes) {
    const resultsDiv = document.getElementById('results');
    
    if (canoes.length === 0) {
        resultsDiv.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">😢</div>
                <p>Aucun canoë ne correspond à vos critères<br>Essayez d'ajuster vos préférences!</p>
            </div>
        `;
        return;
    }
    
    resultsDiv.innerHTML = canoes.map((canoe, index) => createCanoeCard(canoe, index)).join('');
    
    // Animation d'apparition
    const cards = resultsDiv.querySelectorAll('.canoe-recommendation');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Créer une fiche de canoë selon le modèle du screenshot
function createCanoeCard(canoe, index) {
    const compatibility = Math.round(canoe.score * 10); // Score sur 10 -> pourcentage
    
    // Affichage amélioré des tailles (pouces + mètres)
    const longueurPieds = canoe.specifications.longueur_pieds || '';
    const longueurM = canoe.specifications.longueur_m || '';
    const longueurDisplay = longueurPieds ? `${longueurPieds}' (${longueurM}m)` : `${longueurM}m`;
    
    // Prix indicatif
    const prix = canoe.specifications.prix_indicatif_eur;
    const prixDisplay = prix ? `${prix.toLocaleString('fr-FR')}€` : 'Prix non disponible';
    
    // Générer les tags basés sur les aptitudes élevées
    const tags = generateTags(canoe);
    const idealFor = generateIdealFor(canoe);
    
    return `
        <div class="canoe-recommendation" style="animation-delay: ${index * 0.1}s">
            ${index === 0 ? '<div class="recommendation-badge">Choix correct</div>' : ''}
            
            <div class="canoe-header">
                <div class="canoe-header-content">
                    <div class="canoe-title-section">
                        <h3 class="canoe-name">
                            <span class="canoe-emoji">${canoe.emoji || '🛶'}</span>
                            ${canoe.modele}
                        </h3>
                        <div class="canoe-subtitle">
                            ${longueurDisplay} • ${getCanoeDescription(canoe)}
                        </div>
                        <div class="canoe-price">Prix indicatif : ${prixDisplay}</div>
                    </div>
                    <div class="compatibility-badge">
                        <span class="compatibility-percentage">${compatibility}%</span>
                        <span class="compatibility-text">compatibilité</span>
                    </div>
                </div>
            </div>
            
            <div class="canoe-body">
                <div class="points-forts">
                    <h4>Points forts :</h4>
                    <div class="tags-container">
                        ${tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                    </div>
                </div>
                
                <div class="characteristics-grid">
                    <div class="characteristic">
                        <h5>Stabilité</h5>
                        <div class="stars">
                            ${createStars(canoe.caracteristiques.stabilite_primaire)}
                        </div>
                    </div>
                    <div class="characteristic">
                        <h5>Vitesse</h5>
                        <div class="stars">
                            ${createStars(canoe.caracteristiques.vitesse)}
                        </div>
                    </div>
                    <div class="characteristic">
                        <h5>Maniabilité</h5>
                        <div class="stars">
                            ${createStars(canoe.caracteristiques.maniabilite)}
                        </div>
                    </div>
                    <div class="characteristic">
                        <h5>Débutant</h5>
                        <div class="stars">
                            ${createStars(6 - canoe.caracteristiques.niveau_pagayeur)}
                        </div>
                    </div>
                </div>
                
                <div class="ideal-for">
                    <h4>Idéal pour :</h4>
                    <div class="activity-tags">
                        ${idealFor.map(activity => `<span class="activity-tag ${activity.class}">
                            <span class="activity-icon">${activity.icon}</span>
                            ${activity.text}
                        </span>`).join('')}
                    </div>
                </div>
                
                <a href="${canoe.verified_url || canoe.canoe_diffusion_url || '#'}" target="_blank" class="canoe-diffusion-btn">
                    <span class="btn-icon">🛒</span>
                    Voir sur Canoë Diffusion
                </a>
            </div>
        </div>
    `;
}

// Créer les étoiles
function createStars(rating) {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    
    for (let i = 0; i < 5; i++) {
        if (i < fullStars) {
            stars.push('<span class="star filled">★</span>');
        } else if (i === fullStars && hasHalfStar) {
            stars.push('<span class="star half-filled">★</span>');
        } else {
            stars.push('<span class="star">★</span>');
        }
    }
    
    return stars.join('');
}

// Générer les tags selon les points forts
function generateTags(canoe) {
    const tags = [];
    const chars = canoe.caracteristiques;
    
    if (chars.niveau_pagayeur <= 2) tags.push('débutant');
    if (chars.stabilite_primaire >= 4) tags.push('stable');
    if (canoe.aptitudes.expedition_sportive >= 4) tags.push('expédition');
    if (canoe.aptitudes.riviere_classe_I_II >= 4) tags.push('rivière calme');
    if (chars.vitesse >= 4) tags.push('rapide');
    if (chars.maniabilite >= 4) tags.push('maniable');
    
    return tags.slice(0, 4); // Maximum 4 tags
}

// Générer les activités idéales
function generateIdealFor(canoe) {
    const activities = [];
    const aptitudes = canoe.aptitudes;
    
    if (aptitudes.expedition_sportive >= 3) {
        activities.push({ icon: '🏔️', text: 'Expéditions', class: '' });
    }
    if (canoe.caracteristiques.niveau_pagayeur <= 2) {
        activities.push({ icon: '🌱', text: 'Débutants', class: 'beginner' });
    }
    if (canoe.caracteristiques.maniabilite >= 4) {
        activities.push({ icon: '🎯', text: 'Précision', class: 'precision' });
    }
    
    return activities.slice(0, 3); // Maximum 3 activités
}

// Obtenir la description du canoë
function getCanoeDescription(canoe) {
    const descriptions = {
        'Canoes loisirs': 'Canoë robuste et stable, parfait pour débuter',
        'Canoe riviere': 'Idéal pour les rivières et les randonnées',
        'Canoe Eau vive': 'Parfait pour les sports d\'eau vive',
        'Canoe peche- cahasse': 'Optimisé pour la pêche et la chasse',
        'Canoe gonflable': 'Pratique et transportable'
    };
    
    return descriptions[canoe.categorie] || 'Canoë polyvalent';
}

// Créer une barre de caractéristique
function createCharBar(label, value) {
    const percentage = (value / 5) * 100;
    return `
        <div class="char-item">
            <div class="char-label">
                ${label}
            </div>
            <div class="char-bar">
                <div class="char-fill" style="width: ${percentage}%"></div>
            </div>
        </div>
    `;
}

// Afficher tous les canoës avec plus d'informations
function displayAllCanoes(canoes) {
    const allCanoesDiv = document.getElementById('allCanoes');
    
    allCanoesDiv.innerHTML = canoes.map((canoe, index) => createGridCanoeCard(canoe, index)).join('');
    
    // Animation d'apparition
    const cards = allCanoesDiv.querySelectorAll('.canoe-grid-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.3s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 30);
    });
}

// Créer une carte de canoë pour le catalogue complet
function createGridCanoeCard(canoe, index) {
    // Affichage amélioré des tailles (pouces + mètres)
    const longueurPieds = canoe.specifications.longueur_pieds || '';
    const longueurM = canoe.specifications.longueur_m || '';
    const longueurDisplay = longueurPieds ? `${longueurPieds}' (${longueurM}m)` : `${longueurM}m`;
    
    // Prix indicatif
    const prix = canoe.specifications.prix_indicatif_eur;
    const prixDisplay = prix ? `${prix.toLocaleString('fr-FR')}€` : 'Prix non disponible';
    
    const compatibilityScore = calculateCompatibilityScore(canoe);
    const tags = generateTags(canoe);
    const canoeUrl = canoe.verified_url || canoe.canoe_diffusion_url || '#';
    
    return `
        <div class="canoe-grid-card" style="animation-delay: ${index * 0.05}s">
            <div class="grid-canoe-header">
                <div class="grid-canoe-title">
                    <div class="grid-canoe-name-section">
                        <div class="grid-canoe-name">
                            <span class="grid-canoe-emoji">${canoe.emoji || '🛶'}</span>
                            ${canoe.modele}
                        </div>
                        <div class="grid-canoe-subtitle">
                            ${getCanoeDescription(canoe)}
                        </div>
                        <div class="grid-canoe-length">
                            ${longueurDisplay} • ${canoe.specifications.poids_kg} kg • ${canoe.specifications.nb_max_pagayeurs} pers.
                        </div>
                        <div class="grid-canoe-price">
                            💰 ${prixDisplay}
                        </div>
                    </div>
                    <div class="grid-compatibility">
                        <span class="grid-compatibility-score">${compatibilityScore}%</span>
                        <span class="grid-compatibility-text">adapté</span>
                    </div>
                </div>
            </div>
            
            <div class="grid-canoe-body">
                <span class="grid-canoe-category">${canoe.categorie}</span>
                
                <div class="grid-specs-row">
                    <div class="grid-spec-item">
                        <span class="grid-spec-label">📏 Longueur</span>
                        <span class="grid-spec-value">${canoe.specifications.longueur_m} m</span>
                    </div>
                    <div class="grid-spec-item">
                        <span class="grid-spec-label">⚖️ Poids</span>
                        <span class="grid-spec-value">${canoe.specifications.poids_kg} kg</span>
                    </div>
                    <div class="grid-spec-item">
                        <span class="grid-spec-label">👥 Capacité</span>
                        <span class="grid-spec-value">${canoe.specifications.nb_max_pagayeurs} pers.</span>
                    </div>
                    <div class="grid-spec-item">
                        <span class="grid-spec-label">⭐ Niveau</span>
                        <span class="grid-spec-value">${canoe.caracteristiques.niveau_pagayeur}/5</span>
                    </div>
                </div>
                
                <div class="grid-characteristics">
                    <div class="grid-chars-title">Caractéristiques</div>
                    <div class="grid-chars-row">
                        <div class="grid-char-item">
                            <span class="grid-char-label">Stabilité</span>
                            <div class="grid-char-stars">
                                ${createStars(canoe.caracteristiques.stabilite_primaire)}
                            </div>
                        </div>
                        <div class="grid-char-item">
                            <span class="grid-char-label">Vitesse</span>
                            <div class="grid-char-stars">
                                ${createStars(canoe.caracteristiques.vitesse)}
                            </div>
                        </div>
                        <div class="grid-char-item">
                            <span class="grid-char-label">Maniabilité</span>
                            <div class="grid-char-stars">
                                ${createStars(canoe.caracteristiques.maniabilite)}
                            </div>
                        </div>
                        <div class="grid-char-item">
                            <span class="grid-char-label">Chargement</span>
                            <div class="grid-char-stars">
                                ${createStars(canoe.caracteristiques.possibilite_chargement)}
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="grid-tags">
                    <div class="grid-tags-title">Points forts</div>
                    <div class="grid-tag-list">
                        ${tags.slice(0, 3).map(tag => `<span class="grid-tag">${tag}</span>`).join('')}
                    </div>
                </div>
                
                <a href="${canoeUrl}" target="_blank" class="grid-canoe-link">
                    🛒 Voir sur Canoë Diffusion
                </a>
            </div>
        </div>
    `;
}

// Calculer un score de compatibilité général pour le catalogue
function calculateCompatibilityScore(canoe) {
    // Score basé sur les caractéristiques moyennes (sur 5)
    const chars = canoe.caracteristiques;
    const avgScore = (chars.stabilite_primaire + chars.vitesse + chars.maniabilite + chars.possibilite_chargement) / 4;
    
    // Bonus pour débutants (niveau faible)
    const beginnerBonus = chars.niveau_pagayeur <= 2 ? 0.5 : 0;
    
    // Score final sur 100 (base sur 5, convertie en %)
    const baseScore = (avgScore / 5) * 80; // 80% max pour les caractéristiques
    const finalScore = Math.min(100, Math.round(baseScore + (beginnerBonus * 20))); // +20% max pour débutants
    
    return finalScore;
}

// Filtrer les canoës
function filterCanoes() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const selectedCategory = document.getElementById('categoryFilter').value;
    
    const filtered = allCanoes.filter(canoe => {
        const matchesSearch = canoe.modele.toLowerCase().includes(searchTerm);
        const matchesCategory = !selectedCategory || canoe.categorie === selectedCategory;
        return matchesSearch && matchesCategory;
    });
    
    displayAllCanoes(filtered);
}