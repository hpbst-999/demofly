from flask import Blueprint

admin_bp = Blueprint("admin_bp", __name__)

def init_admin_routes(controller):
    admin_bp.add_url_rule("/", "dashboard", view_func=controller.admin_index)
    admin_bp.add_url_rule("/table/<string:table_name>/", view_func=controller.view_data_table)
    admin_bp.add_url_rule("/table/<string:table_name>/delete", methods=['POST'],  view_func=controller.delete_row)
    admin_bp.add_url_rule("/table/<string:table_name>/update", methods=['POST'], view_func=controller.update_row)
    admin_bp.add_url_rule("/table/<string:table_name>/create", methods=['POST'], view_func=controller.create_row)

