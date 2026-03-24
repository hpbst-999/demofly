from app.models.dto import Main_dto_request, Main_dto_search
from app.repositories.main_repo import get_tickets_from_city_to_city
from app.models.route_ticket import RouteTicketDTO

class MainService:

    def get_tickets(self, dto_request:Main_dto_request):
        from_city=dto_request.from_city
        to_city = dto_request.to_city
        date_start =dto_request.date_start
        date_end = dto_request.date_end

        if from_city == to_city:
            raise ValueError("Город отправления и прибытия не могут совпадать")
        
        if date_start > date_end:
            raise ValueError("Дата обратного вылета не может быть раньше даты вылета")
        
        dto_search = Main_dto_search(from_city=from_city, to_city=to_city, date_end=date_end, date_start=date_start)
        tickets = get_tickets_from_city_to_city(dto_search)
        data_dto = [RouteTicketDTO.convert_to_dto(obj) for obj in tickets]
        return data_dto
