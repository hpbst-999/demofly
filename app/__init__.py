from flask import Flask
from config import Config
from app.routes.admin_routes import admin_bp
from app.routes.main_routes import main_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(main_bp)

    return app