# from flask import Flask
# from config import Config
# from app.repositories.db_pool import db_pool
# from app.routes.admin_routes import admin_bp
# from app.routes.main_routes import main_bp

# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(config_class)
#     app.pool = db_pool 
#     app.register_blueprint(admin_bp, url_prefix='/admin')
#     app.register_blueprint(main_bp)
#     return app
from app import create_app

app = create_app()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5555, debug=True)
    finally:
        app.pool.closeall() 