from flask import render_template, jsonify, request, redirect, url_for
from app.services.admin_service import AdminService
from app.models.dto import Table_dto_request


class AdminController:
    
    def admin_index(self):
        tables = AdminService.entities["tables"]
        return render_template("admin/newadmin.html", tables=tables)

    
    def view_data_table(self, table_name):
        search_query = request.args.get("q", "").strip()
        row_id = request.args.get("id","").strip()
        action = None
        service = AdminService()

        if request.args.get("create"):
            template = "admin/overlay.html"
            action = "create"
        elif request.args.get("update") and row_id:
            template = "admin/overlay.html"
            action = "update"
        else:
            template = "admin/newadmin.html"
            
        dto_request= Table_dto_request(table_name=table_name, search_query=search_query)

        try:
            data_dto, columns = AdminService.get_data_tables(service, dto_request)
            keys = AdminService.get_keys(service, dto_request)
            tables = AdminService.get_name_tables(service)
            data  = [obj.__dict__ for obj in data_dto]
            return render_template(template, data=data, columns = columns, tables=tables, current_table=table_name, keys = keys, selected_id = row_id, action = action)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
    
    
    def delete_row(self, table_name):
        search_query = request.args.get("q", "").strip()
        row_id = request.form.get('id')
        service = AdminService()
        dto_request= Table_dto_request(table_name=table_name, search_query=search_query, id_row=row_id)
        AdminService.delete_record(service, dto_request)

        return redirect(url_for('admin_bp.search_default_data', 
                            table_name=table_name, 
                            q=search_query))
    

    def update_row(self, table_name):
        search_query = request.args.get("q", "").strip()
        row_id = request.args.get("id","").strip()
        service = AdminService()
        dto_request= Table_dto_request(table_name=table_name, search_query=search_query, id_row=row_id)
        AdminService.update_record(service, dto_request)

        return redirect()
    

    def create_row(self, table_name):
        search_query = request.args.get("q", "").strip()
        row_id = request.args.get("id","").strip()
        service = AdminService()
        dto_request= Table_dto_request(table_name=table_name, search_query=search_query, id_row=row_id)
        AdminService.create_record(service, dto_request)

        return redirect()
    


    