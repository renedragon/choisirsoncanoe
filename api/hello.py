from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse URL
        path = self.path
        
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = '''
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>🛶 ChoisirSonCanoe</title>
                <style>
                    * { margin: 0; padding: 0; box-sizing: border-box; }
                    body {
                        font-family: 'Arial', sans-serif;
                        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 50%, #ffd3b6 100%);
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }
                    .container {
                        background: rgba(255, 255, 255, 0.95);
                        padding: 3rem;
                        border-radius: 25px;
                        text-align: center;
                        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                        max-width: 600px;
                        margin: 2rem;
                    }
                    h1 { color: #2c5530; margin-bottom: 1rem; font-size: 2.5rem; }
                    p { color: #666; margin-bottom: 2rem; font-size: 1.2rem; }
                    .btn {
                        display: inline-block;
                        background: linear-gradient(45deg, #4fc3f7, #29b6f6);
                        color: white;
                        padding: 1rem 2rem;
                        border-radius: 25px;
                        text-decoration: none;
                        margin: 0.5rem;
                        transition: transform 0.3s ease;
                        font-weight: bold;
                    }
                    .btn:hover { transform: translateY(-3px); }
                    .features {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                        gap: 1rem;
                        margin-top: 2rem;
                    }
                    .feature {
                        background: rgba(79, 195, 247, 0.1);
                        padding: 1rem;
                        border-radius: 15px;
                        border: 2px solid #4fc3f7;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🛶 ChoisirSonCanoe</h1>
                    <p>Application de recommandation de canoës intelligente</p>
                    
                    <div class="features">
                        <div class="feature">
                            <h3>🎯 Recommandations</h3>
                            <p>Algorithme intelligent pour trouver le canoë parfait</p>
                        </div>
                        <div class="feature">
                            <h3>📊 43 Canoës</h3>
                            <p>Base de données complète avec spécifications détaillées</p>
                        </div>
                        <div class="feature">
                            <h3>🔧 Interface Admin</h3>
                            <p>Gestion complète des canoës et des caractéristiques</p>
                        </div>
                        <div class="feature">
                            <h3>📱 Responsive</h3>
                            <p>Design kawaii adapté à tous les écrans</p>
                        </div>
                    </div>
                    
                    <div style="margin-top: 2rem;">
                        <a href="/api/test" class="btn">🧪 Tester l'API</a>
                        <a href="/api/canoes" class="btn">📋 Voir les Canoës</a>
                    </div>
                    
                    <div style="margin-top: 2rem; padding: 1rem; background: rgba(76, 175, 80, 0.1); border-radius: 15px;">
                        <h3>✅ Déploiement Vercel Réussi !</h3>
                        <p>L'application ChoisirSonCanoe fonctionne parfaitement sur Vercel</p>
                    </div>
                </div>
            </body>
            </html>
            '''
            self.wfile.write(html.encode())
            
        elif path == '/api/test':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'success',
                'message': 'API Vercel fonctionnelle !',
                'app': 'ChoisirSonCanoe',
                'platform': 'Vercel',
                'version': '2.0'
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/api/canoes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Données de test
            sample_canoes = [
                {
                    "modele": "Adirondack",
                    "categorie": "Canoes loisirs",
                    "specifications": {"longueur_m": "4.37", "nb_max_pagayeurs": 2, "prix_indicatif_eur": 1650},
                    "caracteristiques": {"niveau_pagayeur": 2, "vitesse": 3, "stabilite_primaire": 4},
                    "canoe_diffusion_url": "https://www.canoediffusion.com/produit/canoe-esquif-adirondack/"
                },
                {
                    "modele": "Echo",
                    "categorie": "Canoe riviere",
                    "specifications": {"longueur_m": "4.12", "nb_max_pagayeurs": 2, "prix_indicatif_eur": 1850},
                    "caracteristiques": {"niveau_pagayeur": 3, "vitesse": 4, "stabilite_primaire": 3},
                    "canoe_diffusion_url": "https://www.canoediffusion.com/produit/canoe-esquif-echo/"
                }
            ]
            self.wfile.write(json.dumps(sample_canoes, ensure_ascii=False).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Page non trouvee</h1>')