from flask import Blueprint
from app.controllers.main import MainController


main_bp = Blueprint("main_bp", __name__)

def init_main_routes(controller):
    main_bp.add_url_rule("/", "index", view_func=controller.main_index)
    main_bp.add_url_rule('/tickets', view_func=controller.view_search_tickets)

