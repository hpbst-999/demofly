from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
@dataclass
class Bookings:
    book_res: str
    book_date: datetime
    total_amount: Decimal

@dataclass
class BookingsDTO:
    book_res: str
    book_date: str
    total_amount: str

    @classmethod
    def convert_to_dto(cls, booking: Bookings) -> 'BookingsDTO':
        return cls(
            book_res=str(booking.book_res),
            book_date=booking.book_date.isoformat(),
            total_amount=str(booking.total_amount)
        )
    