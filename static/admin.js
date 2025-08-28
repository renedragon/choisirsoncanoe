// Variables globales
let currentEditingCanoe = null;
const modal = document.getElementById('canoeModal');
const modalTitle = document.getElementById('modalTitle');
const canoeForm = document.getElementById('canoeForm');

// Événements
document.getElementById('addCanoeBtn').addEventListener('click', () => openAddModal());
document.querySelector('.close').addEventListener('click', closeModal);
document.getElementById('categoryFilter').addEventListener('change', filterCanoes);
document.getElementById('searchFilter').addEventListener('input', filterCanoes);
canoeForm.addEventListener('submit', handleFormSubmit);

// Fermer modal en cliquant à l'extérieur
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        closeModal();
    }
});

// Ouvrir modal d'ajout
function openAddModal() {
    currentEditingCanoe = null;
    modalTitle.textContent = 'Ajouter un canoë';
    canoeForm.reset();
    // Réinitialiser les valeurs par défaut
    ['niveau_pagayeur', 'vitesse', 'stabilite_primaire', 'maniabilite', 'possibilite_chargement', 'etang_lac', 'riviere_calme', 'riviere_mouvementee', 'eau_vive'].forEach(field => {
        document.getElementById(field).value = '3';
    });
    modal.style.display = 'block';
}

// Éditer un canoë
async function editCanoe(modele) {
    try {
        const response = await fetch(`/admin/api/canoe/${encodeURIComponent(modele)}`);
        const canoe = await response.json();
        
        currentEditingCanoe = modele;
        modalTitle.textContent = 'Éditer le canoë';
        
        // Remplir le formulaire
        fillForm(canoe);
        modal.style.display = 'block';
    } catch (error) {
        alert('Erreur lors du chargement du canoë: ' + error.message);
    }
}

// Remplir le formulaire avec les données du canoë
function fillForm(canoe) {
    document.getElementById('modele').value = canoe.modele;
    document.getElementById('categorie').value = canoe.categorie;
    
    // Spécifications
    document.getElementById('longueur_m').value = canoe.specifications.longueur_m;
    document.getElementById('longueur_pieds').value = canoe.specifications.longueur_pieds || '';
    document.getElementById('largeur_cm').value = canoe.specifications.largeur_cm;
    document.getElementById('nb_max_pagayeurs').value = canoe.specifications.nb_max_pagayeurs;
    document.getElementById('prix_indicatif_eur').value = canoe.specifications.prix_indicatif_eur || '';
    document.getElementById('canoe_diffusion_url').value = canoe.canoe_diffusion_url || '';
    
    // Caractéristiques
    document.getElementById('niveau_pagayeur').value = canoe.caracteristiques.niveau_pagayeur;
    document.getElementById('vitesse').value = canoe.caracteristiques.vitesse;
    document.getElementById('stabilite_primaire').value = canoe.caracteristiques.stabilite_primaire;
    document.getElementById('maniabilite').value = canoe.caracteristiques.maniabilite;
    document.getElementById('possibilite_chargement').value = canoe.caracteristiques.possibilite_chargement;
    
    // Aptitudes
    document.getElementById('etang_lac').value = canoe.aptitudes.etang_lac;
    document.getElementById('riviere_calme').value = canoe.aptitudes.riviere_calme;
    document.getElementById('riviere_mouvementee').value = canoe.aptitudes.riviere_mouvementee;
    document.getElementById('eau_vive').value = canoe.aptitudes.eau_vive;
}

// Supprimer un canoë
async function deleteCanoe(modele) {
    if (!confirm(`Êtes-vous sûr de vouloir supprimer le canoë "${modele}" ?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/admin/api/canoe/${encodeURIComponent(modele)}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            location.reload();
        } else {
            const error = await response.json();
            alert('Erreur lors de la suppression: ' + error.error);
        }
    } catch (error) {
        alert('Erreur lors de la suppression: ' + error.message);
    }
}

// Fermer modal
function closeModal() {
    modal.style.display = 'none';
    currentEditingCanoe = null;
}

// Gérer la soumission du formulaire
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(canoeForm);
    const canoeData = {
        modele: formData.get('modele'),
        categorie: formData.get('categorie'),
        specifications: {
            longueur_m: formData.get('longueur_m'),
            longueur_pieds: formData.get('longueur_pieds'),
            largeur_cm: parseInt(formData.get('largeur_cm')),
            nb_max_pagayeurs: parseInt(formData.get('nb_max_pagayeurs')),
            prix_indicatif_eur: formData.get('prix_indicatif_eur') ? parseInt(formData.get('prix_indicatif_eur')) : null
        },
        caracteristiques: {
            niveau_pagayeur: parseInt(formData.get('niveau_pagayeur')),
            vitesse: parseInt(formData.get('vitesse')),
            stabilite_primaire: parseInt(formData.get('stabilite_primaire')),
            maniabilite: parseInt(formData.get('maniabilite')),
            possibilite_chargement: parseInt(formData.get('possibilite_chargement'))
        },
        aptitudes: {
            etang_lac: parseInt(formData.get('etang_lac')),
            riviere_calme: parseInt(formData.get('riviere_calme')),
            riviere_mouvementee: parseInt(formData.get('riviere_mouvementee')),
            eau_vive: parseInt(formData.get('eau_vive'))
        },
        canoe_diffusion_url: formData.get('canoe_diffusion_url')
    };
    
    try {
        const url = currentEditingCanoe 
            ? `/admin/api/canoe/${encodeURIComponent(currentEditingCanoe)}`
            : '/admin/api/canoe';
        
        const method = currentEditingCanoe ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(canoeData)
        });
        
        if (response.ok) {
            closeModal();
            location.reload();
        } else {
            const error = await response.json();
            alert('Erreur lors de la sauvegarde: ' + error.error);
        }
    } catch (error) {
        alert('Erreur lors de la sauvegarde: ' + error.message);
    }
}

// Filtrer les canoës
function filterCanoes() {
    const categoryFilter = document.getElementById('categoryFilter').value;
    const searchFilter = document.getElementById('searchFilter').value.toLowerCase();
    const canoeCards = document.querySelectorAll('.admin-canoe-card');
    
    canoeCards.forEach(card => {
        const category = card.dataset.category;
        const modele = card.querySelector('h3').textContent.toLowerCase();
        
        const matchesCategory = !categoryFilter || category === categoryFilter;
        const matchesSearch = !searchFilter || modele.includes(searchFilter);
        
        if (matchesCategory && matchesSearch) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}