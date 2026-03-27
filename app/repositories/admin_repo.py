
from app.models.dto import Table_dto_search
from app.models.airplanes import Airplanes
from app.models.airports import Airports
from app.models.boarding_passes import Boarding_passes
from app.models.bookings import Bookings
from app.models.flights import Flights
from app.models.routes import Routes
from app.models.seats import Seats
from app.models.segments import Segments
from app.models.tickets import Tickets
from app.models.dto import Cud_dto
from psycopg2.extras import RealDictCursor

class AdminRepository:
    CLASS_MAP = {
    'airplanes_data': Airplanes,
    'airports_data': Airports,
    'boarding_passes': Boarding_passes,
    'bookings': Bookings,
    'flights': Flights,
    'routes': Routes,
    'seats': Seats,
    'segments': Segments,
    'tickets': Tickets
}
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


    def get_table_name(self):
        sql = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'bookings' 
            AND table_type = 'BASE TABLE';
            """
        data_name = self.query_db(sql)
        names_table = [item['table_name'] for item in data_name]
        return names_table
      
    

    def get_data_tables(self, search_dto:Table_dto_search):

            if search_dto.search_query:
                sql = f"""
        SELECT * FROM {search_dto.table_name} AS t
        WHERE t::text ILIKE %s
        ORDER BY 
            (t::text ILIKE %s) DESC,
            STRPOS(LOWER(t::text), LOWER(%s)) ASC
        LIMIT 100;
    """
                data = self.query_db(sql, [f"%{search_dto.search_query}%",   f"% {search_dto.search_query},%", search_dto.search_query ])
            else:
                data = self.query_db(f"SELECT * FROM {search_dto.table_name} ORDER BY 1 LIMIT 100;")

            target_class = self.CLASS_MAP[search_dto.table_name]
            field_names = list(target_class.__dataclass_fields__.keys())

            list_obj = [target_class(**{field: row[field] for field in field_names}) for row in data]
            return list_obj

    def delete_record_by_id(self, record:Cud_dto):
        table_name = record.table_name
        dict_id = record.row_id
        columns = dict_id.keys()
        where_conditions = " AND ".join([f"{col} = %s" for col in columns])
        sql = f"DELETE FROM {table_name} WHERE {where_conditions};"
        params = list(dict_id.values())
        return self.query_db(sql, params)
    
# airports - 
# select * from Airports_data
# offset 0
# limit 50

# airplanes - 
# select * from Airplanes_data
# offset 0
# limit 50

# flights - 
# select r.route_no,f.flight_id,r.validity,r.duration, 
# f.status, f.scheduled_departure, 
# f.scheduled_arrival, f.actual_departure, f.actual_arrival,
# dep.airport_name as departure_airport, dep.city as departure_city, dep.country as departure_country,
# arr.airport_name as arrival_airport, arr.city as arrival_city, arr.country as arrival_country
# from routes r
# join flights f on r.route_no = f.route_no
# join airports_data dep on dep.airport_code = r.departure_airport 
# join airports_data arr on arr.airport_code = r.arrival_airport
# offset 0
# limit 50

# bookings - 
# select b.book_ref,t.ticket_no, b.book_date, b.total_amount,s.fare_conditions,
# t.passenger_id, t.passenger_name,f.flight_id, 
# dep.airport_name as departure_airport, dep.city as departure_city, 
# arr.airport_name as arrival_airport, arr.city as arrival_city
# from bookings b
# join tickets t on b.book_ref =t.book_ref 
# join segments s on t.ticket_no = s.ticket_no 
# join flights f on s.flight_id = f .flight_id 
# join routes r on r.route_no = f.route_no
# join airports_data dep on dep.airport_code = r.departure_airport 
# join airports_data arr on arr.airport_code = r.arrival_airport
# offset 0
# limit 50

# boarding_passes - 

# select t.ticket_no, f.flight_id, b.boarding_no,b.boarding_time,b.seat_no, s.fare_conditions,
# t.passenger_id, t.passenger_name, t.outbound, f.flight_id,f.scheduled_departure, 
# f.scheduled_arrival,r.duration,
# dep.airport_name as departure_airport, dep.city as departure_city, 
# arr.airport_name as arrival_airport, arr.city as arrival_city
# from boarding_passes b
# join tickets t on b.ticket_no = t.ticket_no 
# join flights f on b.flight_id =  f.flight_id
# join segments s on s.ticket_no = t.ticket_no 
# join routes r on r.route_no = f.route_no
# join airports_data dep on dep.airport_code = r.departure_airport 
# join airports_data arr on arr.airport_code = r.arrival_airport
# offset 0
# limit 50

