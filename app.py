from flask import Flask
from dotenv import load_dotenv
import os
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman

load_dotenv()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASk_SECRET_KEY", "dev-key")
    

    csp = {
        'default-src': ["'self'"],
        'style-src': ["'self'", "'unsafe-inline'"],
        'script-src': ["'self'", "'unsafe-inline'"]
    }


    Talisman(app, content_security_policy= csp)
        


    
    CSRFProtect(app)

    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 Mo


    
    from recherche.routes import recherche_bp
    from gestion.routes import gestion_bp

    app.register_blueprint(recherche_bp)
    app.register_blueprint(gestion_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
