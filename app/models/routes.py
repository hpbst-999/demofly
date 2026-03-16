from dataclasses import dataclass
from typing import List
from datetime import datetime
@dataclass
class Routes:
    routes_no: str
    validity: List[datetime]
    departure_airport: str 
    arrival_airport:str
    airplane_code:str
    day_of_week:set[int]
    scheduled_time: datetime
    duration:datetime

@dataclass
class RoutesDTO:
    routes_no: str
    validity: str
    departure_airport: str 
    arrival_airport:str
    airplane_code:str
    day_of_week:str
    scheduled_time: str
    duration: str

    @classmethod
    def from_routes(cls, route: Routes) -> 'RoutesDTO':
        validity_str = ', '.join(dt.isoformat() for dt in route.validity)
        day_of_week_str = ', '.join(str(day) for day in sorted(route.day_of_week))
        duration_hours = route.duration.hour
        duration_minutes = route.duration.minute
        duration_seconds = route.duration.second
        duration_str = f"{duration_hours:02d}:{duration_minutes:02d}:{duration_seconds:02d}"

        return cls(
            routes_no=str(route.routes_no),
            validity=validity_str,
            departure_airport=str(route.departure_airport),
            arrival_airport=str(route.arrival_airport),
            airplane_code=str(route.airplane_code),
            day_of_week=day_of_week_str,
            scheduled_time=route.scheduled_time.isoformat(),
            duration=duration_str
        )