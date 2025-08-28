from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <html>
    <head><title>ChoisirSonCanoe Test</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px; background: #a8edea;">
        <div style="background: white; padding: 30px; border-radius: 20px; display: inline-block;">
            <h1>🛶 ChoisirSonCanoe</h1>
            <h2>✅ Vercel Test OK</h2>
            <p>Flask app working on Vercel!</p>
        </div>
    </body>
    </html>
    """

@app.route('/test')
def test():
    return {'status': 'working', 'message': 'Flask on Vercel OK'}

# Vercel handler
app = app