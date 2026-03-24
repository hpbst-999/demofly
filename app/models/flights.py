from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Flights:
    flight_id: int
    route_no: str
    status: str
    scheduled_departure: datetime
    scheduled_arrival: datetime
    actual_departure: Optional[datetime] # Может быть None
    actual_arrival: Optional[datetime]   # Может быть None

@dataclass
class FlightsDTO:
    flight_id: str
    route_no: str
    status: str
    scheduled_departure: str
    scheduled_arrival: str
    actual_departure: Optional[str]
    actual_arrival: Optional[str]

    @classmethod
    def convert_to_dto(cls, flight: Flights) -> 'FlightsDTO':
        return cls(
            flight_id=str(flight.flight_id),
            route_no=str(flight.route_no),
            status=str(flight.status),
            scheduled_departure=flight.scheduled_departure,
            scheduled_arrival=flight.scheduled_arrival,
            actual_departure=flight.actual_departure if flight.actual_departure else None,
            actual_arrival=flight.actual_arrival if flight.actual_arrival else None
        )