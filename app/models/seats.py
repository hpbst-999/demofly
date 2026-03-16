from dataclasses import dataclass
@dataclass
class Seats:
    airplane_code: str
    seat_no: str
    fare_conditions: str 

@dataclass
class SeatsDTO:
    airplane_code: str
    seat_no: str
    fare_conditions: str

    @classmethod
    def convert_to_dto(cls, seat: Seats) -> 'SeatsDTO':
        return cls(
            airplane_code=str(seat.airplane_code),
            seat_no=str(seat.seat_no),
            fare_conditions=str(seat.fare_conditions)
        )