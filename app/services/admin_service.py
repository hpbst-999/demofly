from app.models.dto import Table_dto_request, Table_dto_search
from app.models.airplanes import AirplanesDTO
from app.models.airports import AirportsDTO
from app.models.boarding_passes import Boarding_passesDTO
from app.models.bookings import BookingsDTO
from app.models.flights import FlightsDTO
from dataclasses import fields
from app.repositories.admin_repo import AdminRepository

class AdminService:

#     TABLE_KEYS = {
#     "bookings": "book_ref",
#     "tickets": "ticket_no",
#     "flights": "flight_id",
#     "airports_data": "airport_code",
#     "airplanes_data": "airplane_code",
#     "routes": ["route_no","airplane_code"], 
#     "boarding_passes": ["ticket_no", "flight_id"],
#     "seats": ["airplane_code", "seat_no"],
#     "segments": ["flight_id", "ticket_no"]
# }
    CLASS_MAP = {
    'airplanes_data': AirplanesDTO,
    'airports_data': AirportsDTO,
    'boarding_passes': Boarding_passesDTO,
    'bookings': BookingsDTO,
    'flights': FlightsDTO,
}

    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    def get_keys(self, dto_request:Table_dto_request):
        table_name = dto_request.table_name
        keys = self.TABLE_KEYS[table_name]
        return keys
    
    def get_data_airports(self,dto:Table_dto_request):
        search_dto = Table_dto_search(search_query=dto.search_query, limit=dto.limit, offset=dto.offset)
        if dto.search_query:
            data = self.admin_repo.get_filter_airports(search_dto)
        else:
            data = self.admin_repo.get_airports(search_dto)
        data_dto = [AirportsDTO.convert_to_dto(obj) for obj in data]
        columns = [f.name for f in fields(AirportsDTO)]
        return data_dto, columns
    
    def get_data_airplanes(self,dto:Table_dto_request):
        search_dto = Table_dto_search(search_query=dto.search_query, limit=dto.limit, offset=dto.offset)
        if dto.search_query:
            data = self.admin_repo.det_filter_airplanes(search_dto)
        else:
            data = self.admin_repo.get_airplanes()
        data_dto = [AirplanesDTO.convert_to_dto(obj) for obj in data]
        columns = [f.name for f in fields(AirplanesDTO)]
        return data_dto, columns
    
    def get_data_flights(self, dto:Table_dto_request):
        search_dto = Table_dto_search(search_query=dto.search_query, limit=dto.limit, offset=dto.offset)
        if dto.search_query:
            data = self.admin_repo.get_filter_flights(search_dto)
        else:
            data = self.admin_repo.get_flights(search_dto)
        data_dto = [FlightsDTO.convert_to_dto(obj) for obj in data]
        columns = [f.name for f in fields(FlightsDTO)]
        return data_dto, columns
    
    def get_data_bookings(self, dto:Table_dto_request):
        search_dto = Table_dto_search(search_query=dto.search_query, limit=dto.limit, offset=dto.offset)
        if dto.search_query:
            data = self.admin_repo.get_filter_bookings(search_dto)
        else:
            data = self.admin_repo.get_bookings(search_dto)
        data_dto = [BookingsDTO.convert_to_dto(obj) for obj in data]
        columns = [f.name for f in fields(BookingsDTO)]
        return data_dto, columns

    def get_data_boarding_passes(self, dto:Table_dto_request):
        search_dto = Table_dto_search(search_query=dto.search_query, limit=dto.limit, offset=dto.offset)
        if dto.search_query:
            data = self.admin_repo.get_filter_boarding_passes(search_dto)
        else:
            data = self.admin_repo.get_boarding_passes(search_dto)
        data_dto = [Boarding_passesDTO.convert_to_dto(obj) for obj in data]
        columns = [f.name for f in fields(Boarding_passesDTO)]
        return data_dto, columns


    

