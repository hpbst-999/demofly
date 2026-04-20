from flask import Blueprint

admin_bp = Blueprint("admin_bp", __name__)

def init_admin_routes(controller):
    admin_bp.add_url_rule("/", "dashboard", view_func=controller.admin_index)

    admin_bp.add_url_rule("/airports/", view_func=controller.view_airports, methods=['GET'])
    admin_bp.add_url_rule("/airports/create", view_func=controller.create_airport, methods=['GET', 'POST'])
    admin_bp.add_url_rule("/airports/update", view_func=controller.update_airport, methods=['GET', 'POST'])
    admin_bp.add_url_rule("/airports/delete", view_func=controller.delete_airport, methods=['POST'])

    admin_bp.add_url_rule("/airplanes/", view_func=controller.view_airplanes, methods=['GET'])
    admin_bp.add_url_rule("/airplanes/create", view_func=controller.create_airplane, methods=['GET', 'POST'])
    admin_bp.add_url_rule("/airplanes/update", view_func=controller.update_airplane, methods=['GET', 'POST'])
    admin_bp.add_url_rule("/airplanes/delete", view_func=controller.delete_airplane, methods=['POST'])

    admin_bp.add_url_rule("/flights/", view_func=controller.view_flights, methods=['GET'])
    admin_bp.add_url_rule("/flights/create", view_func=controller.create_flight, methods=['GET', 'POST'])
    admin_bp.add_url_rule("/flights/update", view_func=controller.update_flight, methods=['GET', 'POST'])
    admin_bp.add_url_rule("/flights/delete", view_func=controller.delete_flight, methods=['POST'])

    admin_bp.add_url_rule("/routes/", view_func=controller.view_routes, methods=['GET'])
    admin_bp.add_url_rule("/routes/create", view_func=controller.create_routes, methods=['GET', 'POST'])
    admin_bp.add_url_rule("/routes/update", view_func=controller.update_routes, methods=['GET', 'POST'])
    admin_bp.add_url_rule("/routes/delete", view_func=controller.delete_routes, methods=['POST'])
    
    admin_bp.add_url_rule("/bookings/", view_func=controller.view_bookings, methods=['GET'])
    admin_bp.add_url_rule("/bookings/create", view_func=controller.create_booking, methods=['GET', 'POST'])
    admin_bp.add_url_rule("/bookings/update", view_func=controller.update_booking, methods=['GET', 'POST'])
    admin_bp.add_url_rule("/bookings/delete", view_func=controller.delete_booking, methods=['POST'])

    admin_bp.add_url_rule("/boarding_passes/", view_func=controller.view_boarding_passes, methods=['GET'])
    admin_bp.add_url_rule("/boarding_passes/create", view_func=controller.create_boarding_pass, methods=['GET', 'POST'])
    admin_bp.add_url_rule("/boarding_passes/update", view_func=controller.update_boarding_pass, methods=['GET', 'POST'])
    admin_bp.add_url_rule("/boarding_passes/delete", view_func=controller.delete_boarding_pass, methods=['POST'])
