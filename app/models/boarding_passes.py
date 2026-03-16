from dataclasses import dataclass
from datetime import datetime
@dataclass
class Boarding_passes:
    ticket_no: str
    flight_id: str
    seat_no: str
    boarding_no: str
    boarding_time: datetime

@dataclass
class Boarding_passesDTO:
    ticket_no: str
    flight_id: str
    seat_no: str
    boarding_no: str
    boarding_time: str

    @classmethod
    def convert_to_dto(cls, boarding_pass: Boarding_passes) -> 'Boarding_passesDTO':
        return cls(
            ticket_no=str(boarding_pass.ticket_no),
            flight_id=str(boarding_pass.flight_id),
            seat_no=str(boarding_pass.seat_no),
            boarding_no=str(boarding_pass.boarding_no),
            boarding_time=boarding_pass.boarding_time.isoformat()
        )
    