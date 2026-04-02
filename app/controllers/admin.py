
from flask import render_template, jsonify, request, redirect, url_for
from app.services.admin_service import AdminService
from app.models.dto import Table_dto_request

class AdminController:

    def __init__(self, service: AdminService):
        self.service = service
    
    def admin_index(self):
        return render_template("admin/newadmin.html", current_page=1, has_next=False,)  

    def view_airports(self):
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)    
        pk_columns = self.service.TABLE_KEYS['airports']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(page=page, search_query=query)
        try:
            dto_response = self.service.get_data_airports(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", 
                                   data=data, columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
        
    def view_airplanes(self):
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int) 
        pk_columns = self.service.TABLE_KEYS['airplanes']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(page=page,search_query=query)        
        try:
            dto_response = self.service.get_data_airplanes(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", 
                                   data=data, 
                                   columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
        
    def view_flights(self):
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int) 
        pk_columns = self.service.TABLE_KEYS['flights']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(search_query=query,page=page)
        try:
            dto_response = self.service.get_data_flights(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", 
                                   data=data, 
                                   columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
        
    def view_bookings(self):
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int) 
        pk_columns = self.service.TABLE_KEYS['bookings']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(search_query=query,page=page)
        try:
            dto_response = self.service.get_data_bookings(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", 
                                   data=data, 
                                   columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
        
    def view_boarding_passes(self):
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int) 
        pk_columns = self.service.TABLE_KEYS['boarding_passes']
        selected_id = request.args.get("selected_id","").strip()
        dto_search = Table_dto_request(search_query=query, page=page)
        try:
            dto_response = self.service.get_data_boarding_passes(dto_search)
            data_dto = dto_response.data
            columns = dto_response.columns
            has_next = dto_response.has_next
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", 
                                   data=data, 
                                   columns = columns, 
                                   selected_id = selected_id, 
                                   current_page = page, 
                                   has_next=has_next,
                                   pk_columns=pk_columns)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500

    
    




    

