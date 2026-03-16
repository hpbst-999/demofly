import psycopg2.extras
import datetime
import re
from app.models.dto import Table_dto_request, Table_dto_search
from app.repositories.admin_repo import get_columns, get_data_tables
from app.models.airplanes import AirplanesDTO
from app.models.airports import AirportsDTO
from app.models.boarding_passes import Boarding_passesDTO
from app.models.bookings import BookingsDTO
from app.models.flights import FlightsDTO
from app.models.routes import RoutesDTO
from app.models.seats import SeatsDTO
from app.models.segments import SegmentsDTO
from app.models.tickets import TicketsDTO
class AdminService:

    pattern_num = r"^\d{13}$"
    pattern_code_num = r"^[A-Z]{2}\s\d{13}$"
    pattern_time = r'\d{2}:\d{2}:\d{2}'
    entities = {
    "tables": [
      {"name": "bookings"},
      {"name": "tickets"},
      {"name": "boarding_passes"},
      {"name": "segments"},
      {"name": "flights"},
      {"name": "routes"},
      {"name": "airports"},
      {"name": "airplanes"},
      {"name": "seats"}
            ]}

    TABLE_KEYS = {
    "bookings": "book_ref",
    "tickets": "ticket_no",
    "flights": "flight_id",
    "airports": "airport_code",
    "airplanes": "airplane_code",
    "routes": ["route_no","airplane_code"], 
    "boarding_passes": ["ticket_no", "flight_id"],
    "seats": ["airplane_code", "seat_no"],
    "segments": ["flight_id", "ticket_no"]
}
    CLASS_MAP = {
    'airplanes': AirplanesDTO,
    'airports': AirportsDTO,
    'boarding_passes': Boarding_passesDTO,
    'bookings': BookingsDTO,
    'flights': FlightsDTO,
    'routes': RoutesDTO,
    'seats': SeatsDTO,
    'segments': SegmentsDTO,
    'tickets': TicketsDTO
}

    # def serialize_row_safe(self,row):

    #     result = {}
    #     for key, value in row.items():
    #         if value is None:
    #             result[key] = None
    #         elif isinstance(value, psycopg2.extras.Range):
    #             result[key] = f"[{value.lower},{value.upper})"
    #         elif isinstance(value, (datetime.time, datetime.datetime)):
    #             result[key] = value.isoformat()
    #         elif isinstance(value, datetime.timedelta):
    #             total_seconds = int(value.total_seconds())
    #             hours = total_seconds // 3600
    #             minutes = (total_seconds % 3600) // 60
    #             seconds = total_seconds % 60
    #             result[key] = f"{hours:02}:{minutes:02}:{seconds:02}"
    #         else:
    #             result[key] = value
    #     return result
    
    def get_name_tables(self):
        return self.entities["tables"]
    

    def get_keys(self, dto_request:Table_dto_request):
        table_name = dto_request.table_name
        keys = self.TABLE_KEYS[table_name]
        return keys

        
    def get_data_tables(self, dto_request:Table_dto_request):
        table_name = dto_request.table_name
        search_query = dto_request.search_query

        if search_query:
            if re.match(self.pattern_num, search_query):
                columns_search  =['ticket_no']  
            elif re.match(self.pattern_code_num, search_query):
                columns_search  =['passenger_id']
            else:
                columns_search = [item['column_name'] for item in get_columns(table_name)] #?-----

            search_dto = Table_dto_search(table_name=table_name, columns=columns_search, search_query=search_query)

            data = get_data_tables(search_dto)
            data_dto = [self.CLASS_MAP[table_name].convert_to_dto(obj) for obj in data]
            
            # if table_name == "routes" and rows:
            #     data = [self.serialize_row_safe(r) for r in rows]
            # else:
            #     data = rows if rows else []
            # columns = list(data[0].keys())

        else:
            search_dto = Table_dto_search(table_name=table_name)

            data = get_data_tables(search_dto)
            data_dto = [self.CLASS_MAP[table_name].convert_to_dto(obj) for obj in data]

            # if table_name == "routes" and rows:
            #     data = [self.serialize_row_safe(r) for r in rows]
            # else:
            #     data = rows if rows else []
            # columns = list(data[0].keys())

        columns= list(data[0].__dataclass_fields__.keys())
        return data_dto, columns


    def delete_record(self, dto_request:Table_dto_request):
        keys = self.TABLE_KEYS[dto_request.table_name]
        return
    

    def create_record(self, dto_request:Table_dto_request):
        keys = self.TABLE_KEYS[dto_request.table_name]
        return
    

    def update_record(self, dto_request:Table_dto_request):
        keys = self.TABLE_KEYS[dto_request.table_name]
        return
    
