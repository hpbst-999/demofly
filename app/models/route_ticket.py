from dataclasses import dataclass
from typing import  Optional
from decimal import Decimal
from datetime import datetime

@dataclass
class RouteTicket:
    flight_id: int
    route_no: str
    scheduled_departure: datetime
    scheduled_arrival: datetime
    departure_airport: str
    departure_city: str
    arrival_airport: str
    arrival_city: str  
    price: Optional[Decimal]        

@dataclass
class RouteTicketDTO:
    flight_id: str
    route_no: str
    scheduled_departure: str
    scheduled_arrival: str
    departure_airport: str
    departure_city: str
    arrival_airport: str
    arrival_city: str  
    price: str

    @classmethod
    def convert_to_dto(cls, route: RouteTicket) -> 'RouteTicketDTO': 
     return cls(
            flight_id=str(route.flight_id),
            route_no=route.route_no,
            scheduled_departure=route.scheduled_departure.isoformat(),
            scheduled_arrival=route.scheduled_arrival.isoformat(),
            departure_airport = route.departure_airport,
            departure_city=route.departure_city,
            arrival_airport=route.arrival_airport,
            arrival_city=route.arrival_city,
            price=str(route.price) if route.price is not None else ""
        )

