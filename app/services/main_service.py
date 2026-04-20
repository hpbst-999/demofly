from app.models.dto import Main_dto_request, Main_dto_search
from app.models.route_ticket import RouteTicketDTO
from app.models.ticket import TicketDTO
from app.repositories.main_repo import MainRepository

class MainService:

    def __init__(self, main_repo: MainRepository):
        self.main_repo = main_repo

    def get_pagination_params(self, page: int, page_size: int = 20):
            if not page or page < 1:
                page = 1
            limit = page_size + 1
            offset = (page - 1) * page_size
            return limit, offset
    
    def get_tickets(self, dto:Main_dto_request):
        from_city=dto.from_city
        to_city = dto.to_city
        date_start =dto.date_start
        date_end = dto.date_end
        limit, offset = self.get_pagination_params(dto.page, page_size=20)
        if from_city == to_city:
            raise ValueError("Город отправления и прибытия не могут совпадать")
        if date_start > date_end:
            raise ValueError("Дата обратного вылета не может быть раньше даты вылета")
        dto_search = Main_dto_search(from_city=from_city, to_city=to_city, date_end=date_end, date_start=date_start, offset=offset, limit=limit)
        tickets = self.main_repo.get_tickets_from_city_to_city(dto_search)
        has_next = len(tickets) > limit-1
        data_dto = [RouteTicketDTO.convert_to_dto(obj) for obj in tickets]
        return data_dto, has_next
    
    
    def get_ticket(self, id):
        ticket = self.main_repo.get_ticket_by_id(id=id)
        ticket_dto = TicketDTO.convert_to_dto(ticket)
        return ticket_dto
