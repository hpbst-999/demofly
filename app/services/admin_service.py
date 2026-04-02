from app.models.dto import Table_dto_request, Table_dto_search, Table_dto_response
from app.models.airplanes import AirplanesDTO
from app.models.airports import AirportsDTO
from app.models.boarding_passes import Boarding_passesDTO
from app.models.bookings import BookingsDTO
from app.models.flights import FlightsDTO
from dataclasses import fields
from app.repositories.admin_repo import AdminRepository

class AdminService:

    TABLE_KEYS = {
    "airports": "airport_code",
    "airplanes": "airplane_code",
    "bookings": ["book_ref", "ticket_no","flight_id"],
    "flights": ["flight_id", "route_no"],
    "boarding_passes": ["ticket_no", "boarding_no","flight_id"]
}

    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    def get_pagination_params(self, page: int, page_size: int = 20):
        if not page or page < 1:
            page = 1
        limit = page_size + 1
        offset = (page - 1) * page_size
        return limit, offset

    def get_keys(self, dto_request:Table_dto_request):
        table_name = dto_request.table_name
        keys = self.TABLE_KEYS[table_name]
        return keys
    
    def get_data_airports(self,dto:Table_dto_request):
        limit, offset = self.get_pagination_params(dto.page, page_size=20)
        search_dto = Table_dto_search(search_query=dto.search_query, limit=limit,offset=offset)
        if dto.search_query:
            data = self.admin_repo.get_filter_airports(search_dto)
        else:
            data = self.admin_repo.get_airports(search_dto)
        has_next = len(data) > limit-1
        data_dto = [AirportsDTO.convert_to_dto(obj) for obj in data]
        columns = [f.name for f in fields(AirportsDTO)]
        dto_response = Table_dto_response(data=data_dto, columns=columns, has_next=has_next)
        return dto_response
    
    def get_data_airplanes(self,dto:Table_dto_request):
        limit, offset = self.get_pagination_params(dto.page, page_size=20)
        search_dto = Table_dto_search(search_query=dto.search_query, limit=limit,offset=offset)
        if dto.search_query:
            data = self.admin_repo.det_filter_airplanes(search_dto)
        else:
            data = self.admin_repo.get_airplanes()
        has_next = len(data) > limit-1
        data_dto = [AirplanesDTO.convert_to_dto(obj) for obj in data]
        columns = [f.name for f in fields(AirplanesDTO)]
        dto_response = Table_dto_response(data=data_dto, columns=columns, has_next=has_next)
        return dto_response
    
    def get_data_flights(self, dto:Table_dto_request):
        limit, offset = self.get_pagination_params(dto.page, page_size=20)
        search_dto = Table_dto_search(search_query=dto.search_query, limit=limit,offset=offset)
        if dto.search_query:
            data = self.admin_repo.get_filter_flights(search_dto)
        else:
            data = self.admin_repo.get_flights(search_dto)
        has_next = len(data) > limit-1
        data_dto = [FlightsDTO.convert_to_dto(obj) for obj in data]
        columns = [f.name for f in fields(FlightsDTO)]
        dto_response = Table_dto_response(data=data_dto, columns=columns, has_next=has_next)
        return dto_response
    
    def get_data_bookings(self, dto:Table_dto_request):
        limit, offset = self.get_pagination_params(dto.page, page_size=20)
        search_dto = Table_dto_search(search_query=dto.search_query, limit=limit,offset=offset)
        if dto.search_query:
            data = self.admin_repo.get_filter_bookings(search_dto)
        else:
            data = self.admin_repo.get_bookings(search_dto)
        has_next = len(data) > limit-1
        data_dto = [BookingsDTO.convert_to_dto(obj) for obj in data]
        columns = [f.name for f in fields(BookingsDTO)]
        dto_response = Table_dto_response(data=data_dto, columns=columns, has_next=has_next)
        return dto_response

    def get_data_boarding_passes(self, dto:Table_dto_request):
        limit, offset = self.get_pagination_params(dto.page, page_size=20)
        search_dto = Table_dto_search(search_query=dto.search_query, limit=limit,offset=offset)
        if dto.search_query:
            data = self.admin_repo.get_filter_boarding_passes(search_dto)
        else:
            data = self.admin_repo.get_boarding_passes(search_dto)
        has_next = len(data) > limit-1
        data_dto = [Boarding_passesDTO.convert_to_dto(obj) for obj in data]
        columns = [f.name for f in fields(Boarding_passesDTO)]
        dto_response = Table_dto_response(data=data_dto, columns=columns, has_next=has_next)
        return dto_response


    

