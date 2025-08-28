from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChoisirSonCanoe - Recommandation de Canoës</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 50%, #ffd3b6 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 25px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        h1 {
            color: #2c5530;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        .subtitle {
            color: #666;
            font-size: 1.2rem;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
            text-align: center;
            transition: transform 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        .feature-title {
            color: #2c5530;
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
        }
        .feature-desc {
            color: #666;
            font-size: 0.95rem;
        }
        .success-badge {
            background: linear-gradient(45deg, #4caf50, #8bc34a);
            color: white;
            padding: 1rem 2rem;
            border-radius: 50px;
            display: inline-block;
            margin: 2rem 0;
            font-weight: bold;
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
        }
        .cta-section {
            text-align: center;
            background: white;
            padding: 2rem;
            border-radius: 25px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }
        .btn {
            display: inline-block;
            background: linear-gradient(45deg, #4fc3f7, #29b6f6);
            color: white;
            padding: 1rem 2rem;
            border-radius: 25px;
            text-decoration: none;
            margin: 0.5rem;
            font-weight: bold;
            transition: transform 0.3s ease;
        }
        .btn:hover {
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛶 ChoisirSonCanoe</h1>
            <p class="subtitle">Trouvez le canoë parfait pour vos aventures</p>
            <div class="success-badge">
                ✅ Application déployée avec succès sur Vercel !
            </div>
        </div>

        <div class="features">
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3 class="feature-title">Recommandations Intelligentes</h3>
                <p class="feature-desc">Algorithme avancé basé sur vos préférences et votre niveau</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3 class="feature-title">43 Canoës Référencés</h3>
                <p class="feature-desc">Base de données complète avec spécifications détaillées</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">💰</div>
                <h3 class="feature-title">Prix Indicatifs</h3>
                <p class="feature-desc">Estimations de prix pour chaque modèle</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🔧</div>
                <h3 class="feature-title">Interface Admin</h3>
                <p class="feature-desc">Gestion complète des canoës et caractéristiques</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <h3 class="feature-title">Design Responsive</h3>
                <p class="feature-desc">Interface kawaii adaptée à tous les écrans</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🔗</div>
                <h3 class="feature-title">Liens Directs</h3>
                <p class="feature-desc">Accès rapide aux produits sur CanoesDiffusion.com</p>
            </div>
        </div>

        <div class="cta-section">
            <h2>🚀 Prêt à trouver votre canoë idéal ?</h2>
            <p style="color: #666; margin: 1rem 0;">Application complète avec interface d'administration</p>
            <div>
                <a href="/api/test" class="btn">🧪 Tester l'API</a>
                <a href="https://github.com/renedragon/choisirsoncanoe" class="btn" style="background: linear-gradient(45deg, #424242, #212121);">📦 Code Source</a>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        self.wfile.write(html.encode('utf-8'))
    
    def do_POST(self):
        self.do_GET()