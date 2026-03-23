from app.models.dto import Main_dto_request
from app.repositories.main_repo import get_tickets_from_city_to_city
from app.models.route_ticket import RouteTicketDTO

class MainService:

    def get_tickets(self, dto_request:Main_dto_request):
        tickets = get_tickets_from_city_to_city(dto_request)
        data_dto = [RouteTicketDTO.convert_to_dto(obj) for obj in tickets]
        return data_dto
