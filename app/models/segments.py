from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class Segment:
    ticket_no: str
    flight_id: int
    fare_conditions: str
    price: Decimal
    scheduled_departure: Optional[datetime] = None
    departure_airport: Optional[str] = ""
    arrival_airport: Optional[str] = ""

@dataclass
class SegmentDTO:
    ticket_no: str
    flight_id: str
    fare_conditions: str
    price: str
    scheduled_departure: Optional[str] = ""
    departure_airport: Optional[str] = ""
    arrival_airport: Optional[str] = ""

    @classmethod
    def convert_to_dto(cls, segment: Segment) -> 'SegmentDTO':
        return cls(
            ticket_no=str(segment.ticket_no),
            flight_id=str(segment.flight_id),
            fare_conditions=str(segment.fare_conditions),
            price=f"{segment.price:.2f}" if segment.price is not None else "0.00",
            scheduled_departure=segment.scheduled_departure.strftime('%d.%m.%Y %H:%M') if segment.scheduled_departure else "",
            departure_airport=str(segment.departure_airport),
            arrival_airport=str(segment.arrival_airport)
        )