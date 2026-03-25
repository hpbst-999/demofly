
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
from app.repositories.db_pool import query_db, db_pool
from app.models.dto import Cud_dto

# class AdminRepository:
     

def get_table_name():
    sql = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'bookings' 
        AND table_type = 'BASE TABLE';
        """
    data_name = query_db(sql)
    names_table = [item['table_name'] for item in data_name]
    return names_table
      
    

def get_data_tables(search_dto:Table_dto_search):

        if search_dto.search_query:
            sql = f"""
    SELECT * FROM {search_dto.table_name} AS t
    WHERE t::text ILIKE %s
    ORDER BY 
        (t::text ILIKE %s) DESC,
        STRPOS(LOWER(t::text), LOWER(%s)) ASC
    LIMIT 100;
"""
            data = query_db(sql, [f"%{search_dto.search_query}%",   f"% {search_dto.search_query},%", search_dto.search_query ])
        else:
            data = query_db(f"SELECT * FROM {search_dto.table_name} ORDER BY 1 LIMIT 100;")
        list_obj = dict_to_objects(data, search_dto.table_name)
        return list_obj

def dict_to_objects(data, table_name):
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
    target_class = CLASS_MAP[table_name]
    field_names = list(target_class.__dataclass_fields__.keys())
    return [target_class(**{field: row[field] for field in field_names}) for row in data]

def delete_record_by_id(record:Cud_dto):
    table_name = record.table_name
    dict_id = record.row_id
    columns = dict_id.keys()
    where_conditions = " AND ".join([f"{col} = %s" for col in columns])
    sql = f"DELETE FROM {table_name} WHERE {where_conditions};"
    params = list(dict_id.values())
    return query_db(sql, params)