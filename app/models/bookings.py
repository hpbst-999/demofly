from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
    
@dataclass
class Bookings:
    book_ref: str
    ticket_no: str
    book_date: datetime
    total_amount: Decimal
    fare_conditions: str 
    passenger_id: str
    passenger_name: str
    flight_id: int
    price: Decimal
    outbound: bool

@dataclass
class BookingsDTO:
    book_ref: str
    ticket_no: str
    book_date: str
    total_amount: str
    fare_conditions: str 
    passenger_id: str
    passenger_name: str
    flight_id: str
    price: str
    outbound: str

    @classmethod
    def convert_to_dto(cls, booking: Bookings) -> 'BookingsDTO':
        return cls(
            book_ref=str(booking.book_ref),
            ticket_no=str(booking.ticket_no),
            book_date=booking.book_date.isoformat() if booking.book_date else "",
            total_amount=str(booking.total_amount),
            fare_conditions=str(booking.fare_conditions),
            passenger_id=str(booking.passenger_id),
            passenger_name=str(booking.passenger_name),
            flight_id=str(booking.flight_id),
            price=str(booking.price),
            outbound=str(booking.outbound)
        )

