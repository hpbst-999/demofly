from dataclasses import dataclass
from datetime import datetime
from typing import Optional
@dataclass
class Boarding_passes:
    ticket_no: str
    boarding_no: int
    boarding_time: datetime
    seat_no: str
    flight_id: int
    fare_conditions: Optional[str] = None
    passenger_id: Optional[str] = None
    passenger_name: Optional[str] = None
    outbound: Optional[bool] = True

@dataclass
class Boarding_passesDTO:
    ticket_no: str
    boarding_no: str
    boarding_time: str
    seat_no: str
    flight_id: str
    fare_conditions: Optional[str] = None
    passenger_id: Optional[str] = None
    passenger_name: Optional[str] = None
    outbound: Optional[str] = None


    @classmethod
    def convert_to_dto(cls, boarding_pass: Boarding_passes) -> 'Boarding_passesDTO':
        return cls(
        ticket_no=str(boarding_pass.ticket_no),
        boarding_no=str(boarding_pass.boarding_no),
        boarding_time=boarding_pass.boarding_time.isoformat() if boarding_pass.boarding_time else "",
        seat_no=str(boarding_pass.seat_no),
        fare_conditions=str(boarding_pass.fare_conditions),
        passenger_id=str(boarding_pass.passenger_id),
        passenger_name=str(boarding_pass.passenger_name),
        flight_id=str(boarding_pass.flight_id),
        outbound=str(boarding_pass.outbound)
        )


    

    

