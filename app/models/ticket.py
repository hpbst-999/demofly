from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Ticket:
    route_no: str
    flight_id: int
    price: float
    scheduled_departure: datetime
    scheduled_arrival: datetime
    duration: timedelta
    model: str
    departure_airport: str
    departure_city: str
    departure_country: str
    arrival_airport: str
    arrival_city: str
    arrival_country: str

@dataclass
class TicketDTO:
    route_no: str
    flight_id: str
    price: str
    scheduled_departure: str
    scheduled_arrival: str
    duration: str
    model: str
    departure_airport: str
    departure_city: str
    departure_country: str
    arrival_airport: str
    arrival_city: str
    arrival_country: str

    @classmethod
    def convert_to_dto(cls, detail: Ticket) -> 'TicketDTO':
        if detail.duration:
            total_seconds = int(detail.duration.total_seconds())
            h = total_seconds // 3600
            m = (total_seconds % 3600) // 60
            s = total_seconds % 60
            duration_str = f"{h:02d}:{m:02d}:{s:02d}"
        else:
            duration_str = ""

        return cls(
            route_no=str(detail.route_no) if detail.route_no else "",
            flight_id = str(detail.flight_id) if detail.route_no else "",
            price=str(detail.price) if detail.price is not None else "0.0",
            scheduled_departure=detail.scheduled_departure.isoformat() if detail.scheduled_departure else "",
            scheduled_arrival=detail.scheduled_arrival.isoformat() if detail.scheduled_arrival else "",
            duration=duration_str,
            model=str(detail.model) if detail.model else "",
            departure_airport=str(detail.departure_airport) if detail.departure_airport else "",
            departure_city=str(detail.departure_city) if detail.departure_city else "",
            departure_country=str(detail.departure_country) if detail.departure_country else "",
            arrival_airport=str(detail.arrival_airport) if detail.arrival_airport else "",
            arrival_city=str(detail.arrival_city) if detail.arrival_city else "",
            arrival_country=str(detail.arrival_country) if detail.arrival_country else ""
        )