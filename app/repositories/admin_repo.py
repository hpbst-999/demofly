from app.models.dto import Table_dto_search
from app.models.airplanes import Airplanes
from app.models.airports import Airports
from app.models.boarding_passes import Boarding_passes
from app.models.bookings import Bookings
from app.models.flights import Flights
from psycopg2.extras import RealDictCursor

class AdminRepository:
    
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
    

    def get_airports(self, dto:Table_dto_search):
        sql ="""
            select airport_code, airport_name->>'en' as airport_name,
            city->>'en' as city, country->>'en' as country, coordinates, timezone
            from Airports_data
            offset %s
            limit %s
            """
        params = [dto.offset, dto.limit]
        airports = self.query_db(sql, params)
        field_names = list(Airports.__dataclass_fields__.keys())
        airports_obj = [Airports(**{field: row[field] for field in field_names}) for row in airports]
        return airports_obj
    
    def get_filter_airports(self, dto:Table_dto_search):
        sql ="""
            select airport_code, airport_name->>'en' as airport_name,
            city->>'en' as city, country->>'en' as country, coordinates, timezone
            from Airports_data
            WHERE LOWER(airport_code) = LOWER(%s)
               OR LOWER(airport_name->>'en') = LOWER(%s)
               OR LOWER(city->>'en') = LOWER(%s)
               OR LOWER(country->>'en') = LOWER(%s) 
            offset %s
            limit %s
            """
        params = [dto.search_query,dto.search_query,dto.search_query,dto.search_query, dto.offset, dto.limit]
        airports = self.query_db(sql, params)
        field_names = list(Airports.__dataclass_fields__.keys())
        airports_obj = [Airports(**{field: row[field] for field in field_names}) for row in airports]
        return airports_obj
    
    def get_airplanes(self):
        sql ="""
            select airplane_code, model->>'en' as model,range,speed from Airplanes_data
            """
        airplanes = self.query_db(sql)
        field_names = list(Airplanes.__dataclass_fields__.keys())
        airplanes_obj = [Airplanes(**{field: row[field] for field in field_names}) for row in airplanes]
        return airplanes_obj
    
    def det_filter_airplanes(self, dto:Table_dto_search):
        sql ="""
            select airplane_code, model->>'en' as model,range,speed from Airplanes_data
            WHERE LOWER(airplane_code) = LOWER(%s)
               OR LOWER(model->>'en') = LOWER(%s)
            """
        params = [dto.search_query, dto.search_query]
        airplanes = self.query_db(sql, params=params)
        field_names = list(Airplanes.__dataclass_fields__.keys())
        airplanes_obj = [Airplanes(**{field: row[field] for field in field_names}) for row in airplanes]
        return airplanes_obj
        
    def get_flights(self, dto:Table_dto_search):
        sql ="""
            select r.route_no,f.flight_id,r.validity,r.duration, 
            f.status, f.scheduled_departure, 
            f.scheduled_arrival, f.actual_departure, f.actual_arrival,
            dep.airport_name->>'en' as departure_airport, dep.city->>'en' as departure_city, dep.country->>'en' as departure_country,
            arr.airport_name->>'en' as arrival_airport, arr.city->>'en' as arrival_city, arr.country->>'en' as arrival_country
            from routes r
            join flights f on r.route_no = f.route_no
            join airports_data dep on dep.airport_code = r.departure_airport 
            join airports_data arr on arr.airport_code = r.arrival_airport
            offset %s
            limit %s
            """
        params = [dto.offset, dto.limit]
        flights = self.query_db(sql, params)
        field_names = list(Flights.__dataclass_fields__.keys())
        flights_obj = [Flights(**{field: row[field] for field in field_names}) for row in flights]
        return  flights_obj
    
    def get_filter_flights(self, dto:Table_dto_search):
        sql ="""
            select r.route_no,f.flight_id,r.validity,r.duration, 
            f.status, f.scheduled_departure, 
            f.scheduled_arrival, f.actual_departure, f.actual_arrival,
            dep.airport_name->>'en' as departure_airport, dep.city->>'en' as departure_city, dep.country->>'en' as departure_country,
            arr.airport_name->>'en' as arrival_airport, arr.city->>'en' as arrival_city, arr.country->>'en' as arrival_country
            from routes r
            join flights f on r.route_no = f.route_no
            join airports_data dep on dep.airport_code = r.departure_airport 
            join airports_data arr on arr.airport_code = r.arrival_airport
            WHERE
            r.route_no::text = %s OR
            f.flight_id::text = %s OR
            LOWER(dep.airport_name->>'en') = LOWER(%s) OR
            LOWER(arr.airport_name->>'en') = LOWER(%s) OR
            LOWER(dep.city->>'en') = LOWER(%s) OR
            LOWER(arr.city->>'en') = LOWER(%s) OR
            LOWER(dep.country->>'en') = LOWER(%s) OR
            LOWER(arr.country->>'en') = LOWER(%s) OR
            f.scheduled_departure::text ILIKE %s OR
            f.scheduled_arrival::text ILIKE %s
            offset %s
            limit %s
            """
        params = [dto.search_query,dto.search_query,dto.search_query,dto.search_query,dto.search_query,dto.search_query,dto.search_query,dto.search_query,dto.search_query+'%',dto.search_query+'%',dto.offset, dto.limit]
        flights = self.query_db(sql, params)
        field_names = list(Flights.__dataclass_fields__.keys())
        flights_obj = [Flights(**{field: row[field] for field in field_names}) for row in flights]
        return  flights_obj
    
    def get_bookings(self, dto:Table_dto_search):
        sql ="""
            select b.book_ref,t.ticket_no, b.book_date, b.total_amount,s.fare_conditions,
            t.passenger_id, t.passenger_name,s.flight_id , t.outbound
            from bookings b
            join tickets t on b.book_ref =t.book_ref 
            join segments s on t.ticket_no = s.ticket_no 
            offset %s
            limit %s
            """
        params = [dto.offset, dto.limit]
        bookings = self.query_db(sql, params)
        field_names = list(Bookings.__dataclass_fields__.keys())
        bookings_obj = [Bookings(**{field: row[field] for field in field_names}) for row in bookings]
        return bookings_obj
    
    def get_filter_bookings(self, dto:Table_dto_search):
        sql ="""
            select b.book_ref,t.ticket_no, b.book_date, b.total_amount,s.fare_conditions,
            t.passenger_id, t.passenger_name,s.flight_id , t.outbound
            from bookings b
            join tickets t on b.book_ref =t.book_ref 
            join segments s on t.ticket_no = s.ticket_no 
            WHERE
                b.book_ref::text = %s OR
                t.ticket_no::text = %s OR
                b.book_date::text ILIKE %s OR
                t.passenger_id::text = %s OR
                LOWER(t.passenger_name) = LOWER(%s) OR
                s.flight_id::text = %s
            offset %s
            limit %s
            """
        params = [dto.search_query, dto.search_query, dto.search_query+'%', dto.search_query, dto.search_query, dto.search_query, dto.offset, dto.limit]
        bookings = self.query_db(sql, params)
        field_names = list(Bookings.__dataclass_fields__.keys())
        bookings_obj = [Bookings(**{field: row[field] for field in field_names}) for row in bookings]
        return bookings_obj
    
    def get_boarding_passes(self, dto:Table_dto_search):
        sql ="""
            select t.ticket_no, b.boarding_no,b.boarding_time,b.seat_no, s.fare_conditions,
            t.passenger_id, t.passenger_name,s.flight_id, t.outbound
            from boarding_passes b
            join tickets t on b.ticket_no = t.ticket_no 
            join segments s on s.ticket_no = t.ticket_no
            offset %s
            limit %s
            """
        params = [dto.offset, dto.limit]
        boardisng_pases = self.query_db(sql, params)
        field_names = list(Boarding_passes.__dataclass_fields__.keys())
        boardisng_pases_obj = [Boarding_passes(**{field: row[field] for field in field_names}) for row in boardisng_pases]
        return boardisng_pases_obj
    
    def get_filter_boarding_passes(self, dto:Table_dto_search):
        sql ="""
            select t.ticket_no, b.boarding_no,b.boarding_time,b.seat_no, s.fare_conditions,
            t.passenger_id, t.passenger_name,s.flight_id, t.outbound
            from boarding_passes b
            join tickets t on b.ticket_no = t.ticket_no 
            join segments s on s.ticket_no = t.ticket_no
            WHERE 
                t.ticket_no::text = %s OR
                b.boarding_no::text = %s OR
                b.boarding_time::text ILIKE %s OR
                t.passenger_id::text = %s OR
                LOWER(t.passenger_name) = LOWER(%s) OR
                s.flight_id::text = %s
            offset %s
            limit %s
            """
        params = [dto.search_query, dto.search_query, dto.search_query+'%', dto.search_query, dto.search_query, dto.search_query, dto.offset, dto.limit]
        boardisng_pases = self.query_db(sql, params)
        field_names = list(Boarding_passes.__dataclass_fields__.keys())
        boardisng_pases_obj = [Boarding_passes(**{field: row[field] for field in field_names}) for row in boardisng_pases]
        return boardisng_pases_obj

