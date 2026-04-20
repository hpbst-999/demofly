from flask import Blueprint

auth_bp = Blueprint("auth_bp", __name__)

def init_auth_routes(controller):

    auth_bp.add_url_rule("/login", "login", view_func=controller.login, methods=["GET", "POST"])
    auth_bp.add_url_rule("/logout", "logout", view_func=controller.logout)