from dataclasses import dataclass
from datetime import datetime
    
@dataclass
class Boarding_passes:
    ticket_no: str
    boarding_no: int
    boarding_time: datetime
    seat_no: str
    fare_conditions: str 
    passenger_id: str
    passenger_name: str
    flight_id: int
    outbound: bool

@dataclass
class Boarding_passesDTO:
    ticket_no: str
    boarding_no: str
    boarding_time: str
    seat_no: str
    fare_conditions: str 
    passenger_id: str
    passenger_name: str
    flight_id: str
    outbound: str


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


    

    

