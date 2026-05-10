from app.models.dto import Table_dto_search
from app.models.airplanes import Airplanes, AirplanesDTO
from app.models.airports import Airports, AirportsDTO
from app.models.boarding_passes import Boarding_passes, Boarding_passesDTO
from app.models.bookings import Bookings, BookingsDTO
from app.models.flights import Flights, FlightsDTO
from app.models.routes import Routes, RoutesDTO
from app.models.segments import Segment,SegmentDTO
from psycopg2.extras import RealDictCursor
import json

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

    def create_airport(self, dto:AirportsDTO):
        name_json = json.dumps({"en": dto.airport_name})
        city_json = json.dumps({"en": dto.city})
        country_json = json.dumps({"en": dto.country})
        
        sql = """
        INSERT INTO airports_data (airport_code, airport_name, city, country, coordinates, timezone)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
        params = [dto.airport_code,name_json,city_json,country_json, dto.coordinates, dto.timezone]
        print(params)
        self.query_db(sql, params)

    def delete_airport(self, id):
        sql = "DELETE FROM airports_data WHERE airport_code = %s"
        params = [id.upper()]
        self.query_db(sql, params)

    def update_airport(self, dto:AirportsDTO):
        sql = """
        UPDATE airports_data 
        SET 
            airport_name = %s, 
            city = %s, 
            country = %s, 
            coordinates = %s, 
            timezone = %s
        WHERE airport_code = %s
    """
        params = [json.dumps({"en": dto.airport_name}), json.dumps({"en": dto.city}),json.dumps({"en": dto.country}),dto.coordinates,dto.timezone,dto.airport_code.upper()]
        self.query_db(sql, params)
    
    def get_airport_by_id(self,id):
        sql = "SELECT airport_code, airport_name->>'en' as airport_name,city->>'en' as city, country->>'en' as country, coordinates, timezone FROM airports_data WHERE airport_code = %s LIMIT 1;"
        params = [id.upper()]
        airport = self.query_db(sql, params,fetchone=True)
        if not airport:
            return None
        field_names = list(Airports.__dataclass_fields__.keys())
        airport_obj = Airports(**{field: airport[field] for field in field_names})
        return airport_obj
    

    def get_airplanes(self):
        sql ="""
            select airplane_code, model->>'en' as model,range,speed from Airplanes_data
            """
        airplanes = self.query_db(sql)
        field_names = list(Airplanes.__dataclass_fields__.keys())
        airplanes_obj = [Airplanes(**{field: row[field] for field in field_names}) for row in airplanes]
        return airplanes_obj

    def create_airplane(self, dto:AirplanesDTO):
        model_json = json.dumps({"en": dto.model})
        sql = """
        INSERT INTO airplanes_data (airplane_code, model, range, speed)
        VALUES (%s, %s, %s, %s)
    """
        params = [dto.airplane_code,model_json, dto.range, dto.speed]
        self.query_db(sql, params)

    def delete_airplane(self, id):
        sql = "DELETE FROM airplanes_data WHERE airplane_code = %s"
        params = [id.upper()]
        self.query_db(sql, params)

    def update_airplane(self, dto:AirplanesDTO):
        sql = """
        UPDATE airplanes_data 
        SET 
            airplane_code = %s, 
            model = %s, 
            range = %s, 
            speed = %s
        WHERE airplane_code = %s
    """
        params = [dto.airplane_code,json.dumps({"en": dto.model}), dto.range, dto.speed,dto.airplane_code]
        self.query_db(sql, params)

    def get_airplane_by_id(self,id):
        sql = "SELECT airplane_code, model->>'en' as model,range, speed FROM airplanes_data WHERE airplane_code = %s LIMIT 1;"
        params = [id.upper()]
        airplane = self.query_db(sql, params,fetchone=True)
        if not airplane:
            return None
        field_names = list(Airplanes.__dataclass_fields__.keys())
        airplane_obj = Airplanes(**{field: airplane[field] for field in field_names})
        return airplane_obj

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
            f.scheduled_arrival, f.actual_departure, f.actual_arrival,r.days_of_week,airp.model->>'en' as model,
            dep.airport_name->>'en' as departure_airport, dep.city->>'en' as departure_city, dep.country->>'en' as departure_country,
            arr.airport_name->>'en' as arrival_airport, arr.city->>'en' as arrival_city, arr.country->>'en' as arrival_country
            from routes r
            join flights f on r.route_no = f.route_no AND r.validity @> f.scheduled_departure
            join airplanes_data airp on airp.airplane_code = r.airplane_code
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
            f.scheduled_arrival, f.actual_departure, f.actual_arrival,r.days_of_week,airp.model->>'en' as model,
            dep.airport_name->>'en' as departure_airport, dep.city->>'en' as departure_city, dep.country->>'en' as departure_country,
            arr.airport_name->>'en' as arrival_airport, arr.city->>'en' as arrival_city, arr.country->>'en' as arrival_country
            from routes r
            join flights f on r.route_no = f.route_no AND r.validity @> f.scheduled_departure
            join airplanes_data airp on airp.airplane_code = r.airplane_code
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
    
    def create_flight(self, dto:FlightsDTO):
        sql="""
            INSERT INTO flights (
            route_no, 
            status, 
            scheduled_departure, 
            scheduled_arrival, 
            actual_departure, 
            actual_arrival) 
            VALUES ( %s, %s,%s, %s, %s, %s)
            """
        params = [dto.route_no, dto.status, dto.scheduled_departure, dto.scheduled_arrival, dto.actual_departure,dto.actual_arrival]
        self.query_db(sql, params)

    def delete_flight(self, id):
        sql = "DELETE FROM flights WHERE flight_id = %s"
        params = [id]
        self.query_db(sql, params)

    def update_flight(self, dto:FlightsDTO):
        sql = """
                UPDATE flights 
                SET 
                    route_no = %s,
                    status = %s,
                    scheduled_departure = %s,
                    scheduled_arrival = %s,
                    actual_departure = %s,
                    actual_arrival = %s
                WHERE 
                    flight_id = %s;
                """
        params = [dto.route_no, dto.status, dto.scheduled_departure, dto.scheduled_arrival, dto.actual_departure, dto.actual_arrival, dto.flight_id]
        self.query_db(sql, params)
        
    def get_flight_by_id(self, id):
        sql = """
            SELECT 
            r.route_no,f.flight_id,r.validity, r.duration, f.status,  f.scheduled_departure,  f.scheduled_arrival,  f.actual_departure,airp.model->>'en' as model, 
            f.actual_arrival, r.days_of_week, dep.airport_name->>'en' as departure_airport,  dep.city->>'en' as departure_city,  dep.country->>'en' as departure_country, 
            arr.airport_name->>'en' as arrival_airport,  arr.city->>'en' as arrival_city, 
            arr.country->>'en' as arrival_country
            FROM routes r
            JOIN flights f ON r.route_no = f.route_no
            join airplanes_data airp on airp.airplane_code = r.airplane_code
            JOIN airports_data dep ON dep.airport_code = r.departure_airport 
            JOIN airports_data arr ON arr.airport_code = r.arrival_airport
            WHERE f.flight_id = %s
            LIMIT 1;
            """
        params = [id]
        flights = self.query_db(sql, params,fetchone=True)
        if not flights:
            return None
        field_names = list(Flights.__dataclass_fields__.keys())
        flight_obj = Flights(**{field: flights[field] for field in field_names})
        return flight_obj


    def get_bookings(self, dto:Table_dto_search):
        sql ="""
            select b.book_ref,t.ticket_no, b.book_date, b.total_amount,s.fare_conditions,
            t.passenger_id, t.passenger_name,s.flight_id ,s.price, t.outbound
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
            t.passenger_id, t.passenger_name,s.flight_id,s.price, t.outbound
            from bookings b
            join tickets t on b.book_ref =t.book_ref 
            join segments s on t.ticket_no = s.ticket_no 
            WHERE
                b.book_ref::text = %s OR
                t.ticket_no::text = %s OR
                t.passenger_id::text = %s OR
                LOWER(t.passenger_name) = LOWER(%s) OR
                s.flight_id::text = %s
            offset %s
            limit %s
            """
        params = [dto.search_query, dto.search_query, dto.search_query, dto.search_query, dto.search_query, dto.offset, dto.limit]
        bookings = self.query_db(sql, params)
        field_names = list(Bookings.__dataclass_fields__.keys())
        bookings_obj = [Bookings(**{field: row[field] for field in field_names}) for row in bookings]
        return bookings_obj
    
    def create_booking(self, dto: BookingsDTO):
        sql = """
            INSERT INTO bookings (book_ref, book_date, total_amount) 
            VALUES (%s, %s, %s) 
            ON CONFLICT (book_ref) DO NOTHING;

            INSERT INTO tickets (ticket_no, book_ref, passenger_id, passenger_name, outbound) 
            VALUES (%s, %s, %s, %s, %s) 
            ON CONFLICT (ticket_no) DO NOTHING;

            INSERT INTO segments (ticket_no, flight_id, fare_conditions, price) 
            VALUES (%s, %s, %s, %s);
        """
        params = [
            dto.book_ref, dto.book_date, dto.total_amount, 
            dto.ticket_no, dto.book_ref, dto.passenger_id, dto.passenger_name, dto.outbound,
            dto.ticket_no, dto.flight_id, dto.fare_conditions, dto.price 
        ]
        
        self.query_db(sql, params)

    def delete_booking(self, book_ref):
        sql = """
        DELETE FROM segments 
        WHERE ticket_no IN (SELECT ticket_no FROM tickets WHERE book_ref = %s);

        DELETE FROM tickets 
        WHERE book_ref = %s;

        DELETE FROM bookings 
        WHERE book_ref = %s;
        """
        params = [book_ref, book_ref, book_ref]
        self.query_db(sql, params)
        
    def update_booking(self, dto:BookingsDTO):
        sql = """
            UPDATE bookings 
            SET book_date = %s, total_amount = %s 
            WHERE book_ref = %s;

            DELETE FROM segments WHERE ticket_no IN (SELECT ticket_no FROM tickets WHERE book_ref = %s);
            DELETE FROM tickets WHERE book_ref = %s;
        """
        params = [dto.book_date, dto.total_amount, dto.book_ref, dto.book_ref, dto.book_ref]
        self.query_db(sql, params)

    def get_booking_by_id(self, book_ref):
        sql = """
                SELECT b.book_ref, t.ticket_no, b.book_date, b.total_amount,
                    s.fare_conditions, t.passenger_id, t.passenger_name,
                    s.flight_id,s.price, t.outbound
                FROM bookings b
                JOIN tickets t ON b.book_ref = t.book_ref
                JOIN segments s ON t.ticket_no = s.ticket_no
                WHERE b.book_ref = %s;
            """
        params = [book_ref]
        booking = self.query_db(sql, params)
        if not booking:
            return []
            
        field_names = list(Bookings.__dataclass_fields__.keys())
        
        bookings_list = []
        for row in booking:
            booking_obj = Bookings(**{field: row[field] for field in field_names})
            bookings_list.append(booking_obj)
            
        return bookings_list


    def get_boarding_passes(self, dto:Table_dto_search):
        sql ="""
          SELECT
                b.ticket_no,
                b.boarding_no,
                b.boarding_time,
                b.seat_no,
                s.fare_conditions,
                t.passenger_id,
                t.passenger_name,
                b.flight_id,
                t.outbound
            FROM segments s
            JOIN boarding_passes b ON s.ticket_no = b.ticket_no AND s.flight_id = b.flight_id
            JOIN tickets t ON b.ticket_no = t.ticket_no
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
            SELECT
                b.ticket_no,
                b.boarding_no,
                b.boarding_time,
                b.seat_no,
                s.fare_conditions,
                t.passenger_id,
                t.passenger_name,
                b.flight_id,
                t.outbound
            FROM segments s
            JOIN boarding_passes b ON s.ticket_no = b.ticket_no AND s.flight_id = b.flight_id
            JOIN tickets t ON b.ticket_no = t.ticket_no
                        WHERE 
                t.ticket_no::text = %s OR
                b.boarding_no::text = %s OR
                t.passenger_id::text = %s OR
                LOWER(t.passenger_name) = LOWER(%s) OR
                s.flight_id::text = %s
            offset %s
            limit %s
            """
        params = [dto.search_query, dto.search_query,  dto.search_query, dto.search_query, dto.search_query, dto.offset, dto.limit]
        boardisng_pases = self.query_db(sql, params)
        field_names = list(Boarding_passes.__dataclass_fields__.keys())
        boardisng_pases_obj = [Boarding_passes(**{field: row[field] for field in field_names}) for row in boardisng_pases]
        return boardisng_pases_obj
    
    def create_boarding_pass(self, dto:Boarding_passes):
        sql = """
                INSERT INTO boarding_passes (
                    ticket_no, 
                    flight_id, 
                    seat_no, 
                    boarding_no, 
                    boarding_time
                ) 
                VALUES (%s, %s, %s, %s, %s)
            """
        params = [dto.ticket_no,dto.flight_id,  dto.seat_no, dto.boarding_no, dto.boarding_time]
        self.query_db(sql, params)

    def delete_boarding_pass(self, ticket_no,flight_id):
        sql = "DELETE FROM boarding_passes WHERE ticket_no = %s AND flight_id = %s"
        params = [ticket_no, flight_id]
        self.query_db(sql, params)

    def update_boarding_pass(self, dto:Boarding_passesDTO):
        sql = """
                UPDATE boarding_passes 
                SET seat_no = %s, boarding_no = %s, boarding_time = %s
                WHERE ticket_no = %s AND flight_id = %s;
                """
        params = [ dto.seat_no, dto.boarding_no, dto.boarding_time,dto.ticket_no,dto.flight_id]
        self.query_db(sql, params)
        
    def get_boarding_pass_by_id(self, ticket_no,flight_id):
        sql = """
            SELECT
            b.ticket_no,
            b.boarding_no,
            b.boarding_time,
            b.seat_no,
            s.fare_conditions,
            t.passenger_id,
            t.passenger_name,
            b.flight_id,
            t.outbound
        FROM segments s
        JOIN boarding_passes b ON s.ticket_no = b.ticket_no AND s.flight_id = b.flight_id
        JOIN tickets t ON b.ticket_no = t.ticket_no
            WHERE b.ticket_no = %s AND b.flight_id = %s
            LIMIT 1;
            """
        params = [ticket_no, flight_id]
        boarding_pass = self.query_db(sql, params,fetchone=True)
        if not boarding_pass:
            return None
        field_names = list(Boarding_passes.__dataclass_fields__.keys())
        boarding_pass_obj = Boarding_passes(**{field: boarding_pass[field] for field in field_names})
        return boarding_pass_obj


    def get_routes(self, dto:Table_dto_search):
        sql ="""
            SELECT 
            r.route_no,
            r.validity,
            r.departure_airport,
            dep.airport_name->>'en' AS departure_airport_name,
            dep.city->>'en' AS departure_city,
            dep.country->>'en' AS departure_country,
            r.arrival_airport,
            arr.airport_name->>'en' AS arrival_airport_name,
            arr.city->>'en' AS arrival_city,
            arr.country->>'en' AS arrival_country,
            r.airplane_code,
            ais.model->>'en' AS model,
            r.days_of_week,
            r.scheduled_time,
            r.duration
        FROM routes r
        JOIN airports_data dep ON r.departure_airport = dep.airport_code
        JOIN airports_data arr ON r.arrival_airport = arr.airport_code
        JOIN airplanes_data ais ON r.airplane_code = ais.airplane_code
            offset %s
            limit %s
            """
        params = [dto.offset, dto.limit]
        routes = self.query_db(sql, params)
        field_names = list(Routes.__dataclass_fields__.keys())
        routes_obj = [Routes(**{field: row[field] for field in field_names}) for row in routes]
        return routes_obj
    
    def get_filter_routes(self, dto:Table_dto_search):
        sql ="""
            SELECT 
            r.route_no,
            r.validity,
            r.departure_airport,
            dep.airport_name->>'en' AS departure_airport_name,
            dep.city->>'en' AS departure_city,
            dep.country->>'en' AS departure_country,
            r.arrival_airport,
            arr.airport_name->>'en' AS arrival_airport_name,
            arr.city->>'en' AS arrival_city,
            arr.country->>'en' AS arrival_country,
            r.airplane_code,
            ais.model->>'en' AS model,
            r.days_of_week,
            r.scheduled_time,
            r.duration
        FROM routes r
        JOIN airports_data dep ON r.departure_airport = dep.airport_code
        JOIN airports_data arr ON r.arrival_airport = arr.airport_code
        JOIN airplanes_data ais ON r.airplane_code = ais.airplane_code
        WHERE 
        LOWER(r.route_no) = LOWER(%s)
        OR LOWER(dep.airport_name->>'en') = LOWER(%s)
        OR LOWER(arr.airport_name->>'en') = LOWER(%s)
        OR LOWER(dep.city->>'en') = LOWER(%s)
        OR LOWER(arr.city->>'en') = LOWER(%s)
            offset %s
            limit %s
            """
        params = [dto.search_query, dto.search_query, dto.search_query, dto.search_query, dto.search_query, dto.offset, dto.limit]
        routes = self.query_db(sql, params)
        field_names = list(Routes.__dataclass_fields__.keys())
        routes_obj = [Routes(**{field: row[field] for field in field_names}) for row in routes]
        return routes_obj

    def create_routes(self, dto:RoutesDTO):
        sql = """
                INSERT INTO routes (
                route_no, validity, departure_airport, 
                arrival_airport, airplane_code, days_of_week, 
                scheduled_time, duration) 
                VALUES (%s,%s::tstzrange,%s,%s,%s,%s::integer[],%s,%s)
            """
        params = [dto.route_no, dto.validity, dto.departure_airport, dto.arrival_airport, dto.airplane_code,
                  dto.days_of_week, dto.scheduled_time, dto.duration]
        self.query_db(sql, params)

    def delete_routes(self, route_no, validity):
        sql = """
            DELETE FROM routes 
            WHERE route_no = %s 
              AND validity = %s::tstzrange
        """
        params = [route_no, validity]
        self.query_db(sql, params)

    def update_routes(self, dto:RoutesDTO):
        sql = """
                UPDATE routes 
                SET route_no = %s, validity = %s, departure_airport = %s, arrival_airport = %s, airplane_code =%s, days_of_week=%s, scheduled_time=%s,duration=%s 
                WHERE route_no = %s AND validity = %s;
                """
        params = [dto.route_no, dto.validity, dto.departure_airport, dto.arrival_airport, dto.airplane_code,
                    dto.days_of_week, dto.scheduled_time, dto.duration, dto.route_no, dto.validity]
        self.query_db(sql, params)

    def get_route_by_id(self, route_no, validity):
        sql = """
            SELECT 
            r.route_no,
            r.validity,
            r.departure_airport,
            dep.airport_name->>'en' AS departure_airport_name,
            dep.city->>'en' AS departure_city,
            dep.country->>'en' AS departure_country,
            r.arrival_airport,
            arr.airport_name->>'en' AS arrival_airport_name,
            arr.city->>'en' AS arrival_city,
            arr.country->>'en' AS arrival_country,
            r.airplane_code,
            ais.model->>'en' AS model,
            r.days_of_week,
            r.scheduled_time,
            r.duration
        FROM routes r
        JOIN airports_data dep ON r.departure_airport = dep.airport_code
        JOIN airports_data arr ON r.arrival_airport = arr.airport_code
        JOIN airplanes_data ais ON r.airplane_code = ais.airplane_code
            WHERE r.route_no = %s AND r.validity = %s
            LIMIT 1;
            """
        params = [route_no, validity]
        route = self.query_db(sql, params,fetchone=True)
        if not route:
            return None
        field_names = list(Routes.__dataclass_fields__.keys())
        route_obj = Routes(**{field: route[field] for field in field_names})
        return route_obj
    

    def get_timezone(self):
        sql = "SELECT DISTINCT timezone FROM airports ORDER BY timezone"
        timezone = self.query_db(sql)
        return [row['timezone'] for row in timezone]
        

    def get_country(self):
        sql = "SELECT DISTINCT country->>'en' as country FROM airports_data ORDER BY country->>'en'"
        country = self.query_db(sql)
        return [row['country'] for row in country]

    def get_city_by_country(self, id):
        sql = "SELECT DISTINCT city->>'en' as city FROM airports_data where country->>'en' = %s  ORDER BY city->>'en'"
        params = [id]
        city = self.query_db(sql, params=params)
        return [row['city'] for row in city]
    
    def get_airport_names_by_city(self, id):
        sql = "SELECT DISTINCT airport_name->>'en' as airport_name FROM airports_data where city->>'en' = %s  ORDER BY airport_name->>'en'"
        params = [id]
        airports = self.query_db(sql, params=params)
        return [row['airport_name'] for row in airports]
    

    def get_airplane_names(self):
        sql = "SELECT DISTINCT model->>'en' as model FROM airplanes_data"
        airplanes = self.query_db(sql)
        return [row['model'] for row in airplanes]

    def get_airplane_code_by_model(self,name):
        sql = "select airplane_code from airplanes_data where model->>'en' = %s"
        params = [name]
        airplane_code = self.query_db(sql, params=params, fetchone=True)
        return airplane_code['airplane_code']
    
    def get_airport_code_by_name(self,name):
        sql = "select airport_code from airports_data where airport_name->>'en' = %s"
        params = [name]
        airport_code = self.query_db(sql, params=params, fetchone=True)
        return airport_code['airport_code']
    
    def get_route_no_by_airports(self, scheduled_departure,departure_airport,arrival_airport):
        sql = "select route_no from routes where validity @> %s::timestamptz and departure_airport = %s and arrival_airport = %s"
        params = [scheduled_departure,departure_airport,arrival_airport]
        route_no = self.query_db(sql, params=params, fetchone=True)
        if route_no is None:
            return " "
        return route_no['route_no']
    
    def get_segments(self, id):
        sql = """
            SELECT 
                segments.ticket_no, 
                segments.flight_id, 
                segments.fare_conditions, 
                segments.price,  
                flights.scheduled_departure, 
                routes.departure_airport, 
                routes.arrival_airport
            FROM segments
            JOIN flights ON segments.flight_id = flights.flight_id
            JOIN routes ON flights.route_no = routes.route_no 
                AND routes.validity @> flights.scheduled_departure
            WHERE segments.ticket_no = %s;
            """
        params = [id]
        segments = self.query_db(sql, params)
        field_names = list(Segment.__dataclass_fields__.keys())
        segments_obj = [Segment(**{field: row[field] for field in field_names}) for row in segments]
        return segments_obj
    
    def get_segment_by_id(self, ticket_no, flight_id):
        sql = """
            SELECT 
                segments.ticket_no, 
                segments.flight_id, 
                segments.fare_conditions, 
                segments.price,  
                flights.scheduled_departure, 
                routes.departure_airport, 
                routes.arrival_airport
            FROM segments
            JOIN flights ON segments.flight_id = flights.flight_id
            JOIN routes ON flights.route_no = routes.route_no 
                AND routes.validity @> flights.scheduled_departure
            WHERE segments.ticket_no = %s and segments.flight_id = %s;
            """
        params = [ticket_no, flight_id]
        segment = self.query_db(sql, params,fetchone=True)
        if not segment:
            return None
        field_names = list(Segment.__dataclass_fields__.keys())
        segment_obj = Segment(**{field: segment[field] for field in field_names})
        return segment_obj
    
    def get_seats(self,id):
        sql="""
            SELECT
                seats.seat_no
            FROM flights
            JOIN routes ON flights.route_no = routes.route_no 
                AND routes.validity @> flights.scheduled_departure
            JOIN seats ON routes.airplane_code = seats.airplane_code
            WHERE flights.flight_id = %s
            """
        params = [id]
        seats = self.query_db(sql, params=params)
        return [row['seat_no'] for row in seats]