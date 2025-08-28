from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ChoisirSonCanoe - Test</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #a8edea, #fed6e3); }
            .container { background: white; padding: 30px; border-radius: 20px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛶 ChoisirSonCanoe</h1>
            <h2>✅ Test Vercel Réussi !</h2>
            <p>L'application Flask fonctionne sur Vercel</p>
            <a href="/api/test">Tester l'API</a>
        </div>
    </body>
    </html>
    '''

@app.route('/api/test')
def test_api():
    return {
        'status': 'success',
        'message': 'API Flask fonctionne !',
        'app': 'ChoisirSonCanoe'
    }

# Export pour Vercel
def handler(request):
    return app(request)

if __name__ == '__main__':
    app.run(debug=True)