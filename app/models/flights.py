from dataclasses import dataclass
from datetime import datetime
@dataclass
class Flights:
    flight_id: int
    route_no: str
    status: str
    scheduled_departure: datetime
    scheduled_arrival: datetime
    actual_departure: datetime
    actual_arrival: datetime

@dataclass
class FlightsDTO:
    flight_id: str
    route_no: str
    status: str
    scheduled_departure: str
    scheduled_arrival: str
    actual_departure: str
    actual_arrival: str

    @classmethod
    def convert_to_dto(cls, flight: Flights) -> 'FlightsDTO':
        return cls(
            flight_id=str(flight.flight_id),
            route_no=str(flight.route_no),
            status=str(flight.status),
            scheduled_departure=flight.scheduled_departure.isoformat(),
            scheduled_arrival=flight.scheduled_arrival.isoformat(),
            actual_departure=flight.actual_departure.isoformat(),
            actual_arrival=flight.actual_arrival.isoformat()
        )