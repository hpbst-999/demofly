from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
@dataclass
class Bookings:
    book_ref: str
    book_date: datetime
    total_amount: Decimal

@dataclass
class BookingsDTO:
    book_ref: str
    book_date: str
    total_amount: str

    @classmethod
    def convert_to_dto(cls, booking: Bookings) -> 'BookingsDTO':
        return cls(
            book_ref=str(booking.book_ref),
            book_date=booking.book_date.isoformat(),
            total_amount=str(booking.total_amount)
        )
    