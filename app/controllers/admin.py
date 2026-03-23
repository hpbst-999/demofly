from flask import render_template, jsonify, request, redirect, url_for
from app.services.admin_service import AdminService
from app.models.dto import Table_dto_request


class AdminController:
    
    def admin_index(self):
        service= AdminService()
        tables = service.get_name_tables()
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
            data, columns = service.get_data_tables(dto_request)
            keys = service.get_keys(dto_request=dto_request)
            tables = service.get_name_tables()
            return render_template(template, data=data, columns = columns, tables=tables, current_table=table_name, keys = keys, selected_id = row_id, action = action)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
    
    
    def delete_row(self, table_name):
        search_query = request.args.get("q", "").strip()
        row_id = request.form.get('id')
        service = AdminService()
        dto_request= Table_dto_request(table_name=table_name, row_id=row_id)
        service.delete_record(dto_request)

        return redirect(url_for('admin_bp.view_data_table', 
                            table_name=table_name, 
                            q=search_query))
    

    def update_row(self, table_name):
        search_query = request.args.get("q", "").strip()
        row_id = request.args.get("id","").strip()
        service = AdminService()
        dto_request= Table_dto_request(table_name=table_name, search_query=search_query, id_row=row_id)
        service.update_record( dto_request)

        return redirect()
    

    def create_row(self, table_name):
        search_query = request.args.get("q", "").strip()
        row_id = request.args.get("id","").strip()
        service = AdminService()
        dto_request= Table_dto_request(table_name=table_name, search_query=search_query, id_row=row_id)
        service.create_record( dto_request)

        return redirect()
    


    