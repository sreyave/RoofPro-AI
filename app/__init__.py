from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key"

    # ✅ IMPORT ALL BLUEPRINTS
    from app.routes.home import home_bp
    from app.routes.chat import chat_bp
    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp   # 🔥 THIS WAS MISSING

    # ✅ REGISTER ALL BLUEPRINTS
    app.register_blueprint(home_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(auth_bp)       # 🔥 THIS WAS MISSING
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
