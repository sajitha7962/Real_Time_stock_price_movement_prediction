from flask import Flask
from config import Config

# Blueprints
from routes.auth import auth
from routes.main import main


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Secret key (for sessions/login)
    app.secret_key = "supersecretkey"

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app


# Optional local run only (Render will NOT use this)
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)