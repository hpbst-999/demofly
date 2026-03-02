from flask import render_template, jsonify, request
from datetime import datetime
from app.models.database import query_db, get_cities, get_flights

class MainController:
    def index(self):
        return render_template('main/index.html')
    
    def parse_date(self, value):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except Exception:
            return None

    def test_db_connection(self):
        try:
            query_db("SELECT 1")
            return jsonify({"status": "success", "message": "Database connected"})
        except Exception:
            return jsonify({"status": "error", "message": "Database error"}), 500
    
    def search_cities(self):
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify([])
        
        try:
            cities = get_cities(query)
            return jsonify([{"name": c["city"]} for c in cities])
        except Exception:
            return jsonify({"error": "Server error"}), 500

    def search_flights(self):
        from_city = request.args.get('from', '').strip()
        to_city = request.args.get('to', '').strip()
        date_start_raw = request.args.get('date_start', '').strip()
        date_end_raw = request.args.get('date_end', date_start_raw).strip()


        if not all([from_city, to_city, date_start_raw]):
            return jsonify({
                "error": "Укажите город вылета, прилета и дату"
            }), 400
        
        date_start = self.parse_date(date_start_raw)
        date_end = self.parse_date(date_end_raw)

        if not date_start or not date_end:
            return jsonify({"error": "Неверный формат даты. Используйте YYYY-MM-DD"}), 400

        try:
            flights = get_flights(from_city, to_city, date_start, date_end)

            results = []
            for flight in flights:
                results.append({
                    "id": flight['flight_id'],
                    "flight": flight['route_no'],
                    "price": float(flight['price']),
                    "from": {
                        "airport": flight['departure_airport'],
                        "city": flight['departure_city'],
                        "time": flight['scheduled_departure'].strftime('%H:%M'),
                        "date": flight['scheduled_departure'].strftime('%Y-%m-%d')
                    },
                    "to": {
                        "airport": flight['arrival_airport'],
                        "city": flight['arrival_city'],
                        "time": flight['scheduled_arrival'].strftime('%H:%M'),
                        "date": flight['scheduled_arrival'].strftime('%Y-%m-%d')
                    }
                })

            return jsonify({
                "flights": results,
                "count": len(results)
            })

        except Exception:
            return jsonify({
                "error": "Ошибка при поиске рейсов"
            }), 500

