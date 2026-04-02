from flask import render_template, jsonify, request, flash
from datetime import datetime
from app.models.dto import Main_dto_request
from app.services.main_service import MainService

class MainController:

    def __init__(self, service: MainService):
        self.service = service

    def main_index(self):
        return render_template('main/index.html', current_page =1)
    
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
        page = request.args.get('page', 1, type=int)           

        if not all([from_city, to_city, date_start, date_end]):
            flash("Заполните все поля", "danger")
            return render_template('main/index.html', tickets=[], current_page = page)

        dto_request = Main_dto_request(from_city=from_city, to_city=to_city, date_start=date_start, date_end=date_end, page=page)
        try:
            tickets, has_next = self.service.get_tickets(dto_request)

            if not tickets:
                flash("Билеты не найдены!", "warning")

            return render_template('main/index.html', tickets = tickets, current_page = page, has_next= has_next)
        except ValueError as e:
            flash(str(e), "warning")
            return render_template('main/index.html', tickets=[], current_page = page)
        except Exception:
            flash("Произошла ошибка", "danger")
            return render_template('main/index.html', tickets=[], current_page = page)
           
