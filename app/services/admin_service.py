import psycopg2.extras
import datetime
import re
from app.models.dto import Table_dto_request, Table_dto_search
from app.repositories.admin_repo import get_data_tables, get_table_name, delete_record_by_id
from app.models.airplanes import AirplanesDTO
from app.models.airports import AirportsDTO
from app.models.boarding_passes import Boarding_passesDTO
from app.models.bookings import BookingsDTO
from app.models.flights import FlightsDTO
from app.models.routes import RoutesDTO
from app.models.seats import SeatsDTO
from app.models.segments import SegmentsDTO
from app.models.tickets import TicketsDTO
from app.models.dto import Cud_dto
from dataclasses import fields

class AdminService:

    TABLE_KEYS = {
    "bookings": "book_ref",
    "tickets": "ticket_no",
    "flights": "flight_id",
    "airports_data": "airport_code",
    "airplanes_data": "airplane_code",
    "routes": ["route_no","airplane_code"], 
    "boarding_passes": ["ticket_no", "flight_id"],
    "seats": ["airplane_code", "seat_no"],
    "segments": ["flight_id", "ticket_no"]
}
    CLASS_MAP = {
    'airplanes_data': AirplanesDTO,
    'airports_data': AirportsDTO,
    'boarding_passes': Boarding_passesDTO,
    'bookings': BookingsDTO,
    'flights': FlightsDTO,
    'routes': RoutesDTO,
    'seats': SeatsDTO,
    'segments': SegmentsDTO,
    'tickets': TicketsDTO
}

    
    def get_name_tables(self):
        name_tables = get_table_name()
        return name_tables
    

    def get_keys(self, dto_request:Table_dto_request):
        table_name = dto_request.table_name
        keys = self.TABLE_KEYS[table_name]
        return keys

        
    def get_data_tables(self, dto_request:Table_dto_request):
        table_name = dto_request.table_name
        search_query = dto_request.search_query

        if search_query:

            search_dto = Table_dto_search(table_name=table_name, search_query=search_query)

            data = get_data_tables(search_dto)
            data_dto = [self.CLASS_MAP[table_name].convert_to_dto(obj) for obj in data]

        else:
            search_dto = Table_dto_search(table_name=table_name)

            data = get_data_tables(search_dto)
            
            data_dto = [self.CLASS_MAP[table_name].convert_to_dto(obj) for obj in data]
        columns = [f.name for f in fields(self.CLASS_MAP[table_name])]
        return data_dto, columns


    def delete_record(self, dto_request:Table_dto_request):
        keys = self.TABLE_KEYS[dto_request.table_name]
        table_name = dto_request.table_name
        row_id = dto_request.row_id
        #проверка на айди не пустой
        if isinstance(keys, str):
            keys = [keys]
        values = row_id.split('|')
        data_dict = dict(zip(keys, values))
        delete_data_dto = Cud_dto(table_name=table_name, row_id=data_dict)
        delete_record_by_id(delete_data_dto)
        return
    

    def create_record(self, dto_request:Table_dto_request):
        keys = self.TABLE_KEYS[dto_request.table_name]
        return
    

    def update_record(self, dto_request:Table_dto_request):
        keys = self.TABLE_KEYS[dto_request.table_name]
        return
    
