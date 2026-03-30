from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from datetime import timedelta
from psycopg2.extras import DateTimeTZRange

@dataclass
class Flights:
    route_no: str
    flight_id: int
    validity: DateTimeTZRange
    duration: timedelta   
    status: str
    scheduled_departure: datetime
    scheduled_arrival: datetime
    actual_departure: Optional[datetime] 
    actual_arrival: Optional[datetime]
    departure_airport:str
    departure_city:str
    departure_country:str
    arrival_airport:str
    arrival_city:str
    arrival_country:str

@dataclass
class FlightsDTO:
    route_no: str
    flight_id: str
    validity: str
    duration: str
    status: str
    scheduled_departure: str
    scheduled_arrival: str
    actual_departure: Optional[str] 
    actual_arrival: Optional[str]
    departure_airport:str
    departure_city:str
    departure_country:str
    arrival_airport:str
    arrival_city:str
    arrival_country:str

    @classmethod
    def convert_to_dto(cls, flight: Flights) -> 'FlightsDTO':
        lower = flight.validity.lower.isoformat() if flight.validity.lower else "-∞"
        upper = flight.validity.upper.isoformat() if flight.validity.upper else "∞"
        validity_str = f"[{lower}, {upper})"

        total_seconds = int(flight.duration.total_seconds())
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        duration_str = f"{h:02d}:{m:02d}:{s:02d}"
        return cls(
            route_no=str(flight.route_no),
            flight_id=str(flight.flight_id),
            validity=validity_str,
            duration=duration_str,
            status=str(flight.status),
            scheduled_departure=flight.scheduled_departure.isoformat() if flight.scheduled_departure else "",
            scheduled_arrival=flight.scheduled_arrival.isoformat() if flight.scheduled_arrival else "",
            actual_departure=flight.actual_departure.isoformat() if flight.actual_departure else "",
            actual_arrival=flight.actual_arrival.isoformat() if flight.actual_arrival else "",
            departure_airport=flight.departure_airport,
            departure_city=flight.departure_city,
            departure_country=flight.departure_country,
            arrival_airport=flight.arrival_airport,
            arrival_city=flight.arrival_city,
            arrival_country=flight.arrival_country
        )



