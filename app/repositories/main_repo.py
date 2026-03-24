from app.repositories.db_pool import query_db
from app.models.dto import Main_dto_search
from app.models.route_ticket import RouteTicket

def get_tickets_from_city_to_city(dto_request:Main_dto_search):
    from_city = dto_request.from_city
    to_city = dto_request.to_city
    date_start = dto_request.date_start
    date_end = dto_request.date_end
    sql = """
SELECT
    f.flight_id,
    f.route_no,
    f.scheduled_departure,
    f.scheduled_arrival,
    r.departure_airport,
    dep.city->>'en' AS departure_city,
    r.arrival_airport,
    arr.city->>'en' AS arrival_city,
    MIN(s.price) AS price -- Выбираем минимальную цену
FROM bookings.flights f
JOIN bookings.routes r ON f.route_no = r.route_no
LEFT JOIN bookings.segments s ON f.flight_id = s.flight_id
JOIN bookings.airports_data dep ON r.departure_airport = dep.airport_code
JOIN bookings.airports_data arr ON r.arrival_airport = arr.airport_code
WHERE dep.city->>'en' ILIKE %s
  AND arr.city->>'en' ILIKE %s
  AND f.scheduled_departure >= %s::timestamp 
  AND f.scheduled_departure < %s::timestamp + interval '1 day'
GROUP BY 
    f.flight_id, 
    f.route_no, 
    f.scheduled_departure, 
    f.scheduled_arrival, 
    r.departure_airport, 
    dep.city->>'en', 
    r.arrival_airport, 
    arr.city->>'en'
ORDER BY f.scheduled_departure
LIMIT 50;
    """
    tickets = query_db(sql,(f"%{from_city}%", f"%{to_city}%", date_start, date_end))
    field_names = list(RouteTicket.__dataclass_fields__.keys())

    return [RouteTicket(**{field: row[field] for field in field_names}) for row in tickets]
