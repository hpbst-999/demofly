
from flask import render_template, jsonify, request, redirect, url_for
from app.services.admin_service import AdminService
from app.models.dto import Table_dto_request

class AdminController:

    def __init__(self, service: AdminService):
        self.service = service
    
    def admin_index(self):
        return render_template("admin/newadmin.html")  

    def view_airports(self):
        query = request.args.get('q', '')
        limit = request.args.get('limit', 20, type=int)    
        offset = request.args.get('offset', 0, type=int)
        row_id = request.args.get("id","").strip()
        dto_search = Table_dto_request(limit=limit, offset=offset, search_query=query)
        try:
            data_dto , columns = self.service.get_data_airports(dto_search)
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", data=data, columns = columns, selected_id = row_id)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
        
    def view_airplanes(self):
        query = request.args.get('q', '')
        row_id = request.args.get("id","").strip()
        dto_search = Table_dto_request(search_query=query,limit=20, offset=0)        
        try:
            data_dto , columns = self.service.get_data_airplanes(dto_search)
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", data=data, columns = columns, selected_id = row_id)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
        
    def view_flights(self):
        query = request.args.get('q', '')
        limit = request.args.get('limit', 20, type=int)    
        offset = request.args.get('offset', 0, type=int)
        row_id = request.args.get("id","").strip()
        dto_search = Table_dto_request(search_query=query,limit=limit, offset=offset)
        try:
            data_dto , columns = self.service.get_data_flights(dto_search)
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", data=data, columns = columns, selected_id = row_id)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
        
    def view_bookings(self):
        query = request.args.get('q', '')
        limit = request.args.get('limit', 20, type=int)    
        offset = request.args.get('offset', 0, type=int)
        row_id = request.args.get("id","").strip()
        dto_search = Table_dto_request(search_query=query,limit=limit, offset=offset)
        try:
            data_dto , columns = self.service.get_data_bookings(dto_search)
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", data=data, columns = columns, selected_id = row_id)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500
        
    def view_boarding_passes(self):
        query = request.args.get('q', '')
        limit = request.args.get('limit', 20, type=int)    
        offset = request.args.get('offset', 0, type=int)
        row_id = request.args.get("id","").strip()
        dto_search = Table_dto_request(search_query=query, limit=limit, offset=offset)
        try:
            data_dto , columns = self.service.get_data_boarding_passes(dto_search)
            data  = [obj.__dict__ for obj in data_dto]

            return render_template("admin/newadmin.html", data=data, columns = columns, selected_id = row_id)
        except Exception as e:
            print(e)
            return jsonify({"error": "Server error"}), 500

    
    




    

