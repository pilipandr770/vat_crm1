import os
import sys

# Add parent directory to Python path for imports
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_cors import CORS

try:
    from .config import settings
    from .extensions import db, migrate
    from .api import api_bp
except ImportError:
    # Fallback for when running as script
    from backend.config import settings
    from backend.extensions import db, migrate
    from backend.api import api_bp

def create_app():
    app = Flask(__name__)
    # Enable CORS for all routes
    CORS(app)
    app.config.from_object(settings)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/ping")
    def ping(): return {"status":"pong"}
    
    @app.get("/")
    def index():
        return """
        <html>
        <head>
            <title>VAT CRM API</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #0070f3; }
                code { background: #f5f5f5; padding: 2px 5px; border-radius: 3px; }
                pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
                a { color: #0070f3; text-decoration: none; }
                a:hover { text-decoration: underline; }
                .endpoint { margin-bottom: 20px; border-left: 3px solid #0070f3; padding-left: 15px; }
            </style>
        </head>
        <body>
            <h1>VAT CRM API</h1>
            <p>Willkommen bei der VAT CRM API. Diese API bietet Funktionen zur Überprüfung und Verwaltung von Umsatzsteuer-Identifikationsnummern.</p>
            
            <h2>Verfügbare Endpunkte:</h2>
            
            <div class="endpoint">
                <h3>VAT-Nummer überprüfen</h3>
                <code>POST /api/companies/full-check</code>
                <p>Überprüft eine VAT-Nummer und gibt Informationen zum Unternehmen zurück.</p>
                <pre>
{
  "requester": {
    "requester_country_code": "DE",
    "requester_vat": "123456789" // Optional
  },
  "counterparty": {
    "country_code": "DE",
    "vat_number": "123456789" // Erforderlich
  }
}
                </pre>
            </div>
            
            <div class="endpoint">
                <h3>Alle Unternehmen auflisten</h3>
                <code>GET /api/companies</code>
                <p>Gibt eine Liste aller gespeicherten Unternehmen zurück.</p>
            </div>
            
            <div class="endpoint">
                <h3>Unternehmensinformationen abrufen</h3>
                <code>GET /api/companies/{id}</code>
                <p>Gibt detaillierte Informationen zu einem bestimmten Unternehmen zurück.</p>
            </div>
            
            <div class="endpoint">
                <h3>API-Status prüfen</h3>
                <code>GET /ping</code>
                <p>Prüft, ob die API verfügbar ist.</p>
            </div>
            
            <footer style="margin-top: 40px; border-top: 1px solid #eaeaea; padding-top: 20px;">
                <p>Für die Frontend-Anwendung besuchen Sie bitte <a href="http://localhost:3000">http://localhost:3000</a></p>
            </footer>
        </body>
        </html>
        """

    return app

app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
