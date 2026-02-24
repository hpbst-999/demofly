from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from config import Config
import logging
from datetime import datetime
from admin import admin_bp
from db import query_db

app = Flask(__name__)
CORS(app)



def parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception:
        return None
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test_page():
    return "Сервер работает!"

@app.route('/api/test')
def test_db():
    try:
        query_db("SELECT 1")
        return jsonify({"status": "success", "message": "Database connected"})
    except Exception:
        return jsonify({"status": "error", "message": "Database error"}), 500

@app.route('/api/cities')
def search_cities():
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify([])

    sql = """
        SELECT DISTINCT city
        FROM bookings.airports
        WHERE city ILIKE %s
        ORDER BY city
        LIMIT 10
    """
    try:
        cities = query_db(sql, (f"%{query}%",))
        return jsonify([{"name": c["city"]} for c in cities]) #убрать цикл и оставить cities во фронте изменить ключ

    except Exception:
        return jsonify({"error": "Server error"}), 500

@app.route('/api/flights/search')
def search_flights():
    from_city = request.args.get('from', '').strip()
    to_city = request.args.get('to', '').strip()
    date_start_raw = request.args.get('date_start', '').strip()
    date_end_raw = request.args.get('date_end', date_start_raw).strip()


    if not all([from_city, to_city, date_start_raw]):
        return jsonify({
            "error": "Укажите город вылета, прилета и дату"
        }), 400

    date_start = parse_date(date_start_raw)
    date_end = parse_date(date_end_raw)

    if not date_start or not date_end:
        return jsonify({"error": "Неверный формат даты. Используйте YYYY-MM-DD"}), 400

    sql = """
        SELECT 
            f.flight_id,
            f.route_no,
            f.scheduled_departure,
            f.scheduled_arrival,
            r.departure_airport,
            dep.city as departure_city,
            r.arrival_airport,
            arr.city as arrival_city,
            COALESCE(MIN(s.price), 0) as price
        FROM bookings.flights f
        JOIN bookings.routes r ON f.route_no = r.route_no
        LEFT JOIN bookings.segments s ON f.flight_id = s.flight_id
        JOIN bookings.airports dep ON r.departure_airport = dep.airport_code
        JOIN bookings.airports arr ON r.arrival_airport = arr.airport_code
        WHERE dep.city ILIKE %s
          AND arr.city ILIKE %s
          AND DATE(f.scheduled_departure) BETWEEN %s AND %s
          AND f.status IN ('Scheduled', 'On Time')
        GROUP BY f.flight_id, f.route_no, f.scheduled_departure, f.scheduled_arrival,
                 r.departure_airport, dep.city, r.arrival_airport, arr.city
        ORDER BY f.scheduled_departure
        LIMIT 50
    """

    try:
        flights = query_db(
            sql,
            (f"%{from_city}%", f"%{to_city}%", date_start, date_end)
        )

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

#----------------------------------------------------------------------------------------------------
app.register_blueprint(admin_bp)
#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

