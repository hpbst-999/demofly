from app.models.dto import Main_dto_request, Main_dto_search
from app.models.route_ticket import RouteTicketDTO
from app.repositories.main_repo import MainRepository

class MainService:

    def __init__(self, main_repo: MainRepository):
        self.main_repo = main_repo

    def get_tickets(self, dto_request:Main_dto_request):
        from_city=dto_request.from_city
        to_city = dto_request.to_city
        date_start =dto_request.date_start
        date_end = dto_request.date_end
        offset = dto_request.offset
        limit = dto_request.limit

        if from_city == to_city:
            raise ValueError("Город отправления и прибытия не могут совпадать")
        
        if date_start > date_end:
            raise ValueError("Дата обратного вылета не может быть раньше даты вылета")
        
        dto_search = Main_dto_search(from_city=from_city, to_city=to_city, date_end=date_end, date_start=date_start, offset=offset, limit=limit)
        tickets = self.main_repo.get_tickets_from_city_to_city(dto_search)
        data_dto = [RouteTicketDTO.convert_to_dto(obj) for obj in tickets]
        return data_dto
