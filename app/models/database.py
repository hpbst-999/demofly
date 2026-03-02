import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from config import Config
db_pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **Config.DB_CONFIG
)

#https://pythonru.com/biblioteki/tranzakcii-postgres-v-python

def query_db(sql, params=None, fetchone=False):
    conn = db_pool.getconn()
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
        db_pool.putconn(conn)

#для мейн окна

def get_cities(cities):
    sql = """
        SELECT DISTINCT city
        FROM bookings.airports
        WHERE city ILIKE %s
        ORDER BY city
        LIMIT 10
    """
    return query_db(sql, (f"%{cities}%",))

def get_flights(from_city, to_city, start_date, end_date):
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
    return query_db(
            sql,
            (f"%{from_city}%", f"%{to_city}%", start_date, end_date))

#для мейн окна

#для админки

def get_columns(table_name):
    sql = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s
            AND data_type IN ('text', 'character varying', 'character', 'integer')
        """
    return query_db(sql, (table_name,))

def get_default_data(table_name, columns=None, search_query=None):
    if search_query:
        where_clause = " OR ".join([f"{col}::text ILIKE %s" for col in columns])
        sql = f"SELECT * FROM {table_name} WHERE {where_clause} LIMIT 100;"
        params = [f"{search_query}%"] * len(columns)
        return query_db(sql, params)
    else:
        sql = f"SELECT * FROM {table_name} LIMIT 100;"
        return query_db(sql)




#для админки