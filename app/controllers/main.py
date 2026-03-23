from flask import render_template, jsonify, request
from datetime import datetime
from app.models.dto import Main_dto_request
from app.services.main_service import MainService

class MainController:
    def main_index(self):
        return render_template('main/index.html')
    
    def parse_date(self, value):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except Exception:
            return None

    
    def view_search_tickets(self):
        from_city = request.args.get('from', '').strip()
        to_city = request.args.get('to', '').strip()
        date_start = self.parse_date(request.args.get('date_start', '').strip())
        date_end = self.parse_date(request.args.get('date_end', date_start).strip())
        dto_request = Main_dto_request(from_city=from_city, to_city=to_city, date_start=date_start, date_end=date_end)
        
        try:
            service = MainService()
            tickets = MainService.get_tickets(service,dto_request)
            return render_template('main/index.html', tickets = tickets)
        except:
            return jsonify({"error": "Server error"}), 500
           
