from app.models.dto import Main_dto_search
from app.models.route_ticket import RouteTicket
from app.models.ticket import Ticket
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

    def get_tickets_from_city_to_city(self, dto:Main_dto_search):
        from_city = dto.from_city
        to_city = dto.to_city
        date_start = dto.date_start
        date_end = dto.date_end
        offset = dto.offset
        limit = dto.limit
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
                    COALESCE(MIN(s.price), 0) AS price 
                FROM flights f
                JOIN routes r ON f.route_no = r.route_no
                LEFT JOIN segments s ON f.flight_id = s.flight_id
                JOIN airports_data dep ON r.departure_airport = dep.airport_code
                JOIN airports_data arr ON r.arrival_airport = arr.airport_code
                WHERE LOWER(dep.city->>'en') = LOWER(%s)
                AND LOWER(arr.city->>'en') = LOWER(%s)
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
                OFFSET %s
                LIMIT %s;
            """
        params = [from_city,to_city,date_start,date_end,offset, limit]
        tickets = self.query_db(sql,params=params)
        field_names = list(RouteTicket.__dataclass_fields__.keys())

        return [RouteTicket(**{field: row[field] for field in field_names}) for row in tickets]
    
    def get_ticket_by_id(self, id):
        sql="""
                SELECT
                f.route_no,
                f.flight_id,
                COALESCE(MIN(s.price), 0) AS price,
                f.scheduled_departure,
                f.scheduled_arrival,
                r.duration,
                ais.model->>'en' AS model,
                r.departure_airport,
                dep.city->>'en' AS departure_city,
                dep.country->>'en' AS departure_country,
                r.arrival_airport,
                arr.city->>'en' AS arrival_city,
                arr.country->>'en' AS arrival_country
                FROM flights f
                LEFT JOIN segments s ON f.flight_id = s.flight_id
                JOIN routes r ON f.route_no = r.route_no
                JOIN airports_data dep ON r.departure_airport = dep.airport_code
                JOIN airports_data arr ON r.arrival_airport = arr.airport_code
                JOIN airplanes_data ais ON r.airplane_code = ais.airplane_code
                WHERE f.flight_id::text = %s 
                GROUP BY
                f.route_no,
                f.flight_id,
                f.scheduled_departure,
                f.scheduled_arrival,
                r.duration,
                ais.model->>'en',
                r.departure_airport,
                dep.city->>'en',
                dep.country->>'en',
                r.arrival_airport,
                arr.city->>'en',
                arr.country->>'en';
            """
        params = [id]
        ticket = self.query_db(sql,params=params)
        if not ticket:     
            return None   
        print(ticket)   
        field_names = list(Ticket.__dataclass_fields__.keys())
        dto = [Ticket(**{field: row[field] for field in field_names}) for row in ticket]
        return dto[0]
