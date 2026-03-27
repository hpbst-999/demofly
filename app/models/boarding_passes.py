from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
    
@dataclass
class Boarding_passes:
    ticket_no: str
    flight_id: int
    boarding_no: int
    boarding_time: datetime
    seat_no: str
    fare_conditions: str 
    passenger_id: str
    passenger_name: str
    outbound: bool
    scheduled_departure: datetime
    scheduled_arrival: datetime
    duration: timedelta  
    departure_airport:str
    departure_city:str
    arrival_airport:str
    arrival_city:str

@dataclass
class Boarding_passesDTO:
    ticket_no: str
    flight_id: str
    boarding_no: str
    boarding_time: str
    seat_no: str
    fare_conditions: str 
    passenger_id: str
    passenger_name: str
    outbound: str
    scheduled_departure: str
    scheduled_arrival: str
    duration: str
    departure_airport:str
    departure_city:str
    arrival_airport:str
    arrival_city:str

    @classmethod
    def convert_to_dto(cls, boarding_pass: Boarding_passes) -> 'Boarding_passesDTO':
        total_seconds = int(boarding_pass.duration.total_seconds())
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        duration_str = f"{h:02d}:{m:02d}:{s:02d}"
        return cls(
        ticket_no=str(boarding_pass.ticket_no),
        flight_id=str(boarding_pass.flight_id),
        boarding_no=str(boarding_pass.boarding_no),
        boarding_time=boarding_pass.boarding_time.isoformat() if boarding_pass.boarding_time else "",
        seat_no=str(boarding_pass.seat_no),
        fare_conditions=str(boarding_pass.fare_conditions),
        passenger_id=str(boarding_pass.passenger_id),
        passenger_name=str(boarding_pass.passenger_name),
        outbound=str(boarding_pass.outbound),
        scheduled_departure=boarding_pass.scheduled_departure.isoformat() if boarding_pass.scheduled_departure else "",
        scheduled_arrival=boarding_pass.scheduled_arrival.isoformat() if boarding_pass.scheduled_arrival else "",
        duration=duration_str,
        departure_airport=boarding_pass.departure_airport,
        departure_city=boarding_pass.departure_city,
        arrival_airport=boarding_pass.arrival_airport,
        arrival_city=boarding_pass.arrival_city
        )


    

    

