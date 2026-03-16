import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from config import Config
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

db_pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **Config.DB_CONFIG
)
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
    
def get_columns(table_name):
        sql = """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = %s
                AND data_type IN ('text', 'character varying', 'character', 'integer')
            """
        data = query_db(sql, (table_name,))
        return data
    

def get_data_tables(search_dto:Table_dto_search):

        if search_dto.search_query:
            where_clause = " OR ".join([f"{col}::text ILIKE %s" for col in search_dto.columns])
            sql = f"SELECT * FROM {search_dto.table_name} WHERE {where_clause} LIMIT 100;"
            params = [f"{search_dto.search_query}%"] * len(search_dto.columns)
            data = query_db(sql, params)
    
        else:
            sql = f"SELECT * FROM {search_dto.table_name} LIMIT 100;"
            data = query_db(sql)
        list_obj = dict_to_objects(data, search_dto.table_name)
        return list_obj

def dict_to_objects(data, table_name):
    CLASS_MAP = {
    'airplanes': Airplanes,
    'airports': Airports,
    'boarding_passes': Boarding_passes,
    'bookings': Bookings,
    'flights': Flights,
    'routes': Routes,
    'seats': Seats,
    'segments': Segments,
    'tickets': Tickets
}
    target_class = CLASS_MAP[table_name]
    field_names = list(target_class.__dataclass_fields__.keys())
    return [target_class(**{field: row[field] for field in field_names}) for row in data]
