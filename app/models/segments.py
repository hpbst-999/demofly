from dataclasses import dataclass
from decimal import Decimal
@dataclass
class Segments:
    ticket_no: str
    flight_id: int
    fare_conditions: str 
    price: Decimal

@dataclass
class SegmentsDTO:
    ticket_no: str
    flight_id: str
    fare_conditions: str 
    price: str

    @classmethod
    def convert_to_dto(cls, segment: Segments) -> 'SegmentsDTO':
        return cls(
            ticket_no=str(segment.ticket_no),
            flight_id=str(segment.flight_id),
            fare_conditions=str(segment.fare_conditions),
            price=str(segment.price)
        )