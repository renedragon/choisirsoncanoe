from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>ChoisirSonCanoe</title>
            <style>
                body { 
                    font-family: Arial; 
                    text-align: center; 
                    padding: 50px; 
                    background: linear-gradient(135deg, #a8edea, #fed6e3);
                }
                .container { 
                    background: white; 
                    padding: 30px; 
                    border-radius: 20px; 
                    display: inline-block;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                }
                h1 { color: #2c5530; }
                .success { 
                    background: #4caf50; 
                    color: white; 
                    padding: 10px 20px; 
                    border-radius: 10px; 
                    display: inline-block;
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🛶 ChoisirSonCanoe</h1>
                <div class="success">✅ Vercel Deployment Working!</div>
                <p>Application de recommandation de canoës</p>
                <p>43 canoës disponibles</p>
            </div>
        </body>
        </html>
        '''
        
        self.wfile.write(html.encode())