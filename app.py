from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASk_SECRET_KEY", "dev-key")
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER 
    from recherche.routes import recherche_bp
    from gestion.routes import gestion_bp

    app.register_blueprint(recherche_bp)
    app.register_blueprint(gestion_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
