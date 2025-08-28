from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'status': 'success',
            'message': 'API ChoisirSonCanoe fonctionnelle sur Vercel !',
            'endpoints': {
                '/': 'Page d\'accueil',
                '/api/test': 'Ce endpoint de test',
                '/api/main': 'Interface principale'
            },
            'stats': {
                'total_canoes': 43,
                'categories': 5,
                'features': ['Recommandations', 'Admin', 'Responsive', 'Prix']
            }
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))