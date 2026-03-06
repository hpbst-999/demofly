from flask import Blueprint
from app.controllers.admin import AdminController

admin_bp = Blueprint("admin_bp", __name__)
controller = AdminController()

admin_bp.add_url_rule("/", "dashboard", view_func=controller.admin_index)
admin_bp.add_url_rule("/table/<string:table_name>", view_func=controller.search_default_data)
