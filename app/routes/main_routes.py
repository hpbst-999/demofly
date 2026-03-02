from flask import Blueprint
from app.controllers.main import MainController


main_bp = Blueprint("main_bp", __name__)
controller = MainController()

main_bp.add_url_rule("/", "index", view_func=controller.index)
main_bp.add_url_rule('/test', view_func=controller.test_db_connection)
main_bp.add_url_rule('/api/cities', view_func=controller.search_cities)
main_bp.add_url_rule('/api/flights/search', view_func=controller.search_flights)

