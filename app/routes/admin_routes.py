from flask import Blueprint

admin_bp = Blueprint("admin_bp", __name__)

def init_admin_routes(controller):
    admin_bp.add_url_rule("/", "dashboard", view_func=controller.admin_index)
    admin_bp.add_url_rule("/airports/", view_func=controller.view_airports)
    admin_bp.add_url_rule("/airplanes/", view_func=controller.view_airplanes)
    admin_bp.add_url_rule("/flights/", view_func=controller.view_flights)
    admin_bp.add_url_rule("/bookings/", view_func=controller.view_bookings)
    admin_bp.add_url_rule("/boarding_passes/", view_func=controller.view_boarding_passes)

