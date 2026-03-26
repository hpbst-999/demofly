from app.models.dto import Main_dto_search
from app.models.route_ticket import RouteTicket
from psycopg2.extras import RealDictCursor

class MainRepository:

    def __init__(self, pool):
        self.pool = pool

    def query_db(self, sql, params=None, fetchone=False):
        conn = self.pool.getconn()
        try:
            with conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(sql, params or ())
                    if cur.description is None:
                        return None
                    return cur.fetchone() if fetchone else cur.fetchall()
        except Exception as e:
            raise e 
        finally:
            self.pool.putconn(conn)

    def get_tickets_from_city_to_city(self, dto_request:Main_dto_search):
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
        MIN(s.price) AS price
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
        tickets = self.query_db(sql,(f"%{from_city}%", f"%{to_city}%", date_start, date_end)) #Убрать фстроки
        field_names = list(RouteTicket.__dataclass_fields__.keys())

        return [RouteTicket(**{field: row[field] for field in field_names}) for row in tickets]
