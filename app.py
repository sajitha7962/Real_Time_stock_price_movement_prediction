from flask import Flask
from config import Config

# Blueprints
from routes.auth import auth
from routes.main import main


def create_app():
    app = Flask(__name__)

    # ✅ Load config
    app.config.from_object(Config)

    # 🔥 VERY IMPORTANT (for login/session)
    app.secret_key = "supersecretkey"

    # ✅ Register Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app


# 🚀 Run app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)