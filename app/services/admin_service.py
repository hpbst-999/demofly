from app.models.dto import Table_dto_request, Table_dto_search, Table_dto_response
from app.models.airplanes import AirplanesDTO
from app.models.airports import AirportsDTO
from app.models.boarding_passes import Boarding_passesDTO
from app.models.bookings import BookingsDTO
from app.models.flights import FlightsDTO
from app.models.routes import RoutesDTO
from app.models.segments import SegmentDTO
from dataclasses import fields
from app.repositories.admin_repo import AdminRepository
import re
from flask import flash
from datetime import datetime

class AdminService:

    TABLE_KEYS = {
    "airports": "airport_code",
    "airplanes": "airplane_code",
    "bookings": "book_ref",
    "flights": "flight_id",
    "boarding_passes": ["ticket_no","flight_id"],
    "routes":["route_no","validity"]

}

    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    def parse_datetime(self, value):
        if not value:
            return None
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
        
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
    
    def create_data_airport(self, dto:AirportsDTO):
        if len(dto.airport_code) != 3 or not dto.airport_code.isalpha():
            flash("Код аэропорта должен состоять ровно из 3 БУКВ!", "warning")
        elif not re.match(r'^\(-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?\)$', dto.coordinates):
            flash("Координаты должны быть в формате (lat,long)", "warning")
        else:
            self.admin_repo.create_airport(dto=dto)

    def delete_data_airport(self,id):
        if len(id) != 3 or not id.isalpha():
            flash("Неверный код аэропорта", "warning")
        self.admin_repo.delete_airport(id=id)

    def update_data_airport(self, dto:AirportsDTO):
        if len(dto.airport_code) != 3 or not dto.airport_code.isalpha():
            flash("Код аэропорта должен состоять ровно из 3 БУКВ!", "warning")
        elif not re.match(r'^\(-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?\)$', dto.coordinates):
            flash("Координаты должны быть в формате (lat,long)", "warning")
        else:
            self.admin_repo.update_airport(dto=dto)

    def get_data_airport_by_id(self, id):
        airport = self.admin_repo.get_airport_by_id(id=id)
        airport_dto = AirportsDTO.convert_to_dto(airport)
        return airport_dto


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

    def create_data_airplane(self, dto:AirplanesDTO):
        if len(dto.airplane_code) != 3 :
            flash("Код самолета должен состоять ровно из 3 БУКВ!", "warning")
        elif not dto.range.isdigit():
            flash("Дальность должна быть целым положительным числом!", "warning")
        elif not dto.speed.isdigit():
            flash("Скорость должна быть целым положительным числом!", "warning")
        else:
            self.admin_repo.create_airplane(dto=dto)

    def delete_data_airplane(self,id):
        if len(id) != 3 :
            flash("Неверный код самолета", "warning")
        else:
            self.admin_repo.delete_airplane(id=id)

    def update_data_airplane(self, dto:AirplanesDTO):
        if len(dto.airplane_code) != 3:
            flash("Код самолета должен состоять ровно из 3 БУКВ!", "warning")
        elif not dto.range.isdigit():
            flash("Дальность должна быть целым положительным числом!", "warning")
        elif not dto.speed.isdigit():
            flash("Скорость должна быть целым положительным числом!", "warning")
        else:
            self.admin_repo.update_airplane(dto=dto)

    def get_data_airplane_by_id(self, id):
        airplane = self.admin_repo.get_airplane_by_id(id=id)
        airplane_dto = AirplanesDTO.convert_to_dto(airplane)
        return airplane_dto
    

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
    
    def create_data_flight(self, dto:FlightsDTO):
        scheduled_departure_dt = self.parse_datetime(dto.scheduled_departure)
        scheduled_arrival_dt = self.parse_datetime(dto.scheduled_arrival)
        actual_departure_dt = self.parse_datetime(dto.actual_departure)
        actual_arrival_dt = self.parse_datetime(dto.actual_arrival)
        if len(dto.route_no) != 6:
            flash("Номер маршрута должен состоять ровно из 6 символов!", "warning")
        elif not (scheduled_departure_dt and scheduled_arrival_dt):
            flash("Укажите корректные даты планового вылета и прилета!", "warning")
        elif scheduled_departure_dt >= scheduled_arrival_dt:
            flash("Плановое время вылета не может быть позже или равно времени прилета!", "warning")
        elif actual_departure_dt and actual_arrival_dt and actual_departure_dt >= actual_arrival_dt:
            flash("Фактическое время вылета не может быть позже времени прилета!", "warning")
        else:
            self.admin_repo.create_flight(dto=dto)
        
    def delete_data_flight(self,id):
        if not id.isdigit():
            flash("Неверный код рейса", "warning")
        else:
            self.admin_repo.delete_flight(id=id)

    def update_data_flight(self, dto:FlightsDTO):
        scheduled_departure_dt = self.parse_datetime(dto.scheduled_departure)
        scheduled_arrival_dt = self.parse_datetime(dto.scheduled_arrival)
        actual_departure_dt = self.parse_datetime(dto.actual_departure)
        actual_arrival_dt = self.parse_datetime(dto.actual_arrival)
        if len(dto.route_no) != 6:
            flash("Номер маршрута должен состоять ровно из 6 символов!", "warning")
        elif not (scheduled_departure_dt and scheduled_arrival_dt):
            flash("Укажите корректные даты планового вылета и прилета!", "warning")
        elif scheduled_departure_dt >= scheduled_arrival_dt:
            flash("Плановое время вылета не может быть позже или равно времени прилета!", "warning")
        elif actual_departure_dt and actual_arrival_dt and actual_departure_dt >= actual_arrival_dt:
            flash("Фактическое время вылета не может быть позже времени прилета!", "warning")
        else:
            self.admin_repo.update_flight(dto=dto)

    def get_data_flight_by_id(self, id):
        flight = self.admin_repo.get_flight_by_id(id=id)
        flight_dto = FlightsDTO.convert_to_dto(flight)
        flight_dto.scheduled_departure = flight.scheduled_departure.strftime('%Y-%m-%dT%H:%M')
        flight_dto.scheduled_arrival = flight.scheduled_arrival.strftime('%Y-%m-%dT%H:%M')
        flight_dto.actual_departure = flight.actual_departure.strftime('%Y-%m-%dT%H:%M') if flight.actual_departure else None
        flight_dto.actual_arrival = flight.actual_arrival.strftime('%Y-%m-%dT%H:%M') if flight.actual_arrival else None
        return flight_dto


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

    def create_data_booking(self, dto_list: list):
        for index, dto in enumerate(dto_list):
            book_date_dt = self.parse_datetime(dto.book_date)
            name_parts = str(dto.passenger_name).strip().split()
            
            prefix = f"Ошибка (запись №{index + 1}): "

            if len(dto.book_ref) != 6:
                flash(prefix + "Номер бронирования (book_ref) должен состоять ровно из 6 символов!", "warning")
                raise ValueError("Validation failed")
                
            elif len(dto.ticket_no) != 13:
                flash(prefix + "Введите корректный номер билета (13 символов)!", "warning")
                raise ValueError("Validation failed")
                
            elif float(dto.total_amount) < 0:
                flash(prefix + "Сумма бронирования не может быть отрицательной!", "warning")
                raise ValueError("Validation failed")
                
            elif len(name_parts) != 2:
                flash(prefix + "Имя пассажира должно состоять ровно из двух слов (Имя и Фамилия)!", "warning")
                raise ValueError("Validation failed")
                
            elif not re.match(r'^[a-zA-Z]{2}\s\d{13}$', str(dto.passenger_id).strip()):
                flash(prefix + "ID пассажира должен быть в формате: AB 1234567890123", "warning")
                raise ValueError("Validation failed")
                
            elif not book_date_dt:
                flash(prefix + "Укажите корректную дату", "warning")
                raise ValueError("Validation failed")
                
            elif not str(dto.flight_id).isdigit():
                flash(prefix + "Неверный код рейса", "warning")
                raise ValueError("Validation failed")

        for dto in dto_list:
            self.admin_repo.create_booking(dto=dto)

    def delete_data_booking(self, id):
        if len(id) != 6:
            flash("Номер бронирования (book_ref) должен состоять ровно из 6 символов!", "warning")
        else:
            self.admin_repo.delete_booking(book_ref=id)

    def update_data_booking(self, dto_list: list):
        for index, dto in enumerate(dto_list):
            book_date_dt = self.parse_datetime(dto.book_date)
            name_parts = str(dto.passenger_name).strip().split()
            
            prefix = f"Ошибка (запись №{index + 1}): "

            if len(dto.book_ref) != 6:
                flash(prefix + "Номер бронирования (book_ref) должен состоять ровно из 6 символов!", "warning")
                raise ValueError("Validation failed")
                
            elif len(dto.ticket_no) != 13:
                flash(prefix + "Введите корректный номер билета (13 символов)!", "warning")
                raise ValueError("Validation failed")
                
            elif float(dto.total_amount) < 0:
                flash(prefix + "Сумма бронирования не может быть отрицательной!", "warning")
                raise ValueError("Validation failed")
                
            elif len(name_parts) != 2:
                flash(prefix + "Имя пассажира должно состоять ровно из двух слов (Имя и Фамилия)!", "warning")
                raise ValueError("Validation failed")
                
            elif not re.match(r'^[a-zA-Z]{2}\s\d{13}$', str(dto.passenger_id).strip()):
                flash(prefix + "ID пассажира должен быть в формате: AB 1234567890123", "warning")
                raise ValueError("Validation failed")
                
            elif not book_date_dt:
                flash(prefix + "Укажите корректную дату", "warning")
                raise ValueError("Validation failed")
                
            elif not str(dto.flight_id).isdigit():
                flash(prefix + "Неверный код рейса", "warning")
                raise ValueError("Validation failed")
        self.admin_repo.update_booking(dto_list[0])
        for dto in dto_list:
            self.admin_repo.create_booking(dto=dto)

    def get_data_booking_by_id(self, id):

        bookings = self.admin_repo.get_booking_by_id(book_ref=id)
        dto_list = []
        for booking in bookings:
            dto = BookingsDTO.convert_to_dto(booking)
            dto.book_date = booking.book_date.strftime('%Y-%m-%dT%H:%M')
            dto_list.append(dto)
        return dto_list
    

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

    def create_data_boarding_pass(self, dto:Boarding_passesDTO):
        boarding_time_dt = self.parse_datetime(dto.boarding_time)
        if len(dto.ticket_no) != 13:
            flash("Номер билета должен состоять ровно из 13 символов!", "warning")
        elif not dto.flight_id.isdigit():
            flash("Идентификатор рейса (ID) число", "warning")
        elif dto.boarding_no and int(dto.boarding_no) <= 0:
            flash("Номер посадки должен быть числом!", "warning")
        elif not boarding_time_dt:
            flash("Укажите корректное время и дату посадки!", "warning")
        else:
            self.admin_repo.create_boarding_pass(dto=dto)

    def delete_data_boarding_pass(self, id):
        ticket_no, flight_id = id.split('|')
        if len(ticket_no) != 13:
            flash("Номер билета должен состоять ровно из 13 символов!", "warning")
        elif not flight_id.isdigit():
            flash("Идентификатор рейса (ID) число", "warning")
        else:
            self.admin_repo.delete_boarding_pass(ticket_no=ticket_no, flight_id=flight_id)

    def update_data_boarding_pass(self, dto:Boarding_passesDTO):
        boarding_time_dt = self.parse_datetime(dto.boarding_time)
        if len(dto.ticket_no) != 13:
            flash("Номер билета должен состоять ровно из 13 символов!", "warning")
        elif not dto.flight_id.isdigit():
            flash("Идентификатор рейса (ID) число", "warning")
        elif dto.boarding_no and int(dto.boarding_no) <= 0:
            flash("Номер посадки должен быть числом!", "warning")
        elif not boarding_time_dt:
            flash("Укажите корректное время и дату посадки!", "warning")
        else:
            self.admin_repo.update_boarding_pass(dto=dto)

    def get_data_boarding_pass_by_id(self, id):
        ticket_no, flight_id = id.split('|')
        boarding_pass = self.admin_repo.get_boarding_pass_by_id(ticket_no=ticket_no, flight_id=flight_id)
        boarding_pass_dto = Boarding_passesDTO.convert_to_dto(boarding_pass)
        boarding_pass_dto.boarding_time = boarding_pass.boarding_time.strftime('%Y-%m-%dT%H:%M')
        return boarding_pass_dto
    
    
    def get_data_routes(self, dto:Table_dto_request):
        limit, offset = self.get_pagination_params(dto.page, page_size=20)
        search_dto = Table_dto_search(search_query=dto.search_query, limit=limit,offset=offset)
        if dto.search_query:
            data = self.admin_repo.get_filter_routes(search_dto)
        else:
            data = self.admin_repo.get_routes(search_dto)
        has_next = len(data) > limit-1
        data_dto = [RoutesDTO.convert_to_dto(obj) for obj in data]
        columns = [f.name for f in fields(RoutesDTO)]
        dto_response = Table_dto_response(data=data_dto, columns=columns, has_next=has_next)
        return dto_response
    
    def create_data_routes(self, dto:RoutesDTO):
        dto.days_of_week = "{" + dto.days_of_week + "}"
        dto.validity =  f"[{dto.v_start}, {dto.v_end})"
        if len(dto.departure_airport) != 3 or not dto.departure_airport.isalpha():
            flash("Код аэропорта вылета должен состоять ровно из 3 БУКВ!", "warning")
        elif len(dto.arrival_airport) != 3 or not dto.arrival_airport.isalpha():
            flash("Код аэропорта прибытия должен состоять ровно из 3 БУКВ!", "warning")
        elif len(dto.airplane_code) != 3:
            flash("Код самолета должен состоять из 3 символов!", "warning")
        elif not re.match(r'^\d{2,3}:\d{2}:\d{2}$', dto.duration):
            flash("Длительность должна быть в формате HH:MM:SS (напр. 02:30:00)", "warning")
        elif len(dto.route_no) != 6:
            flash("Номер маршрута должен состоять ровно из 6 символов!", "warning")
        else:
            self.admin_repo.create_routes(dto)

    def delete_data_routes(self, id):
        route_no,validity = id.split('|')
        validity = validity.replace(' ', '+')
        if len(route_no) != 6:
            flash("Номер маршрута должен состоять ровно из 6 символов!", "warning")
        self.admin_repo.delete_routes(route_no=route_no, validity=validity)
    
    def update_data_routes(self, dto:RoutesDTO):
        dto.days_of_week = "{" + dto.days_of_week + "}"
        dto.validity =  f"[{dto.v_start}, {dto.v_end})"
        if len(dto.departure_airport) != 3 or not dto.departure_airport.isalpha():
            flash("Код аэропорта вылета должен состоять ровно из 3 БУКВ!", "warning")
        elif len(dto.arrival_airport) != 3 or not dto.arrival_airport.isalpha():
            flash("Код аэропорта прибытия должен состоять ровно из 3 БУКВ!", "warning")
        elif len(dto.airplane_code) != 3:
            flash("Код самолета должен состоять из 3 символов!", "warning")
        elif not re.match(r'^\d{2,3}:\d{2}:\d{2}$', dto.duration):
            flash("Длительность должна быть в формате HH:MM:SS (напр. 02:30:00)", "warning")
        elif len(dto.route_no) != 6:
            flash("Номер маршрута должен состоять ровно из 6 символов!", "warning")
        else:
            self.admin_repo.update_routes(dto)
            
    def get_data_route_by_id(self, id):
        route_no,validity = id.split('|')
        validity = validity.replace(' ', '+')
        route = self.admin_repo.get_route_by_id(route_no, validity) #что делать если ключ изменился
        route_dto = RoutesDTO.convert_to_dto(route)
        v_start,v_end = route_dto.validity[1:-1].split(',')
        v_start_obj = datetime.fromisoformat(v_start)
        v_end_obj = datetime.fromisoformat(v_end)
        route_dto.v_start = v_start_obj.strftime('%Y-%m-%d')
        route_dto.v_end = v_end_obj.strftime('%Y-%m-%d')
        return route_dto
    

    def get_data_timezone(self):
        timezone = self.admin_repo.get_timezone()
        return timezone
        
    def get_data_country(self):
        country = self.admin_repo.get_country()
        return country

    def get_data_city_by_country(self, id):
        city = self.admin_repo.get_city_by_country(id=id)
        return city

    def get_data_airplane_names(self):
        airplane_list = self.admin_repo.get_airplane_names()
        return airplane_list
    
    def get_data_airplane_code_by_model(self,name):
        airplane_code = self.admin_repo.get_airplane_code_by_model(name=name)
        return airplane_code
    
    def get_data_airport_names_by_city(self,id):
        airport_list = self.admin_repo.get_airport_names_by_city(id=id)
        return airport_list
    
    def get_data_airport_code_by_name(self,name):
        airport_code = self.admin_repo.get_airport_code_by_name(name=name)
        return airport_code
    
    def get_data_route_no_by_airports(self, scheduled_departure,departure_airport,arrival_airport):
        route_no = self.admin_repo.get_route_no_by_airports(scheduled_departure=scheduled_departure,departure_airport=departure_airport,arrival_airport=arrival_airport)
        return route_no
    
    def get_data_segments(self, id):
        data = self.admin_repo.get_segments(id=id)
        data_dto = [SegmentDTO.convert_to_dto(obj) for obj in data]
        return data_dto

    def get_data_segment_by_id(self,ticket_no, flight_id):
        segment = self.admin_repo.get_segment_by_id(ticket_no, flight_id)
        segment_dto = SegmentDTO.convert_to_dto(segment)
        return segment_dto
    
    def get_data_seats(self, id):
        seats = self.admin_repo.get_seats(id=id)
        return seats
    