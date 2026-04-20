from flask import Flask
from config import Config
from app.repositories.db_pool import db_pool
from app.routes.admin_routes import admin_bp
from app.routes.main_routes import main_bp
from app.routes.auth_routes import auth_bp
from app.repositories.admin_repo import AdminRepository
from app.services.admin_service import AdminService
from app.controllers.admin import AdminController
from app.routes.admin_routes import init_admin_routes
from app.routes.main_routes import init_main_routes
from app.routes.auth_routes import init_auth_routes
from app.repositories.main_repo import MainRepository
from app.services.main_service import MainService
from app.controllers.main import MainController
from app.repositories.auth_repo import AuthRepository
from app.services.auth_service import AuthService
from app.controllers.auth import AuthController
from flask import session, redirect, url_for, request,flash

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.pool = db_pool 


    admin_repo = AdminRepository(db_pool)
    admin_service = AdminService(admin_repo)
    admin_controller = AdminController(admin_service)

    main_repo = MainRepository(db_pool)
    main_service = MainService(main_repo)
    main_controller = MainController(main_service)

    auth_repo = AuthRepository(db_pool)
    auth_service = AuthService(auth_repo)
    auth_controller = AuthController(auth_service)

    init_auth_routes(auth_controller)
    init_admin_routes(admin_controller)
    init_main_routes(main_controller)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(main_bp)

    @app.before_request
    def security_check():
        allowed_routes = ['auth_bp.login', 'static']
        if 'user_id' not in session and request.endpoint not in allowed_routes:
            return redirect(url_for('auth_bp.login'))

        if request.path.startswith('/admin') and session.get('role') != 'admin':
            flash("Нужны права администратора", "danger")
            return redirect(url_for('main_bp.index'))
    return app

