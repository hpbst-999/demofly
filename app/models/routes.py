from dataclasses import dataclass
from typing import List, Optional
from datetime import time, timedelta
from psycopg2.extras import DateTimeTZRange

@dataclass
class Routes:
    route_no: str
    validity: DateTimeTZRange  
    departure_airport: str 
    arrival_airport: str
    airplane_code: str
    days_of_week: List[int]    
    scheduled_time: time       
    duration: timedelta     

@dataclass
class RoutesDTO:
    route_no: str
    validity: str
    departure_airport: str 
    arrival_airport: str
    airplane_code: str
    days_of_week: str
    scheduled_time: str
    duration: str

    @classmethod
    def convert_to_dto(cls, route: Routes) -> 'RoutesDTO':
        lower = route.validity.lower.isoformat() if route.validity.lower else "-∞"
        upper = route.validity.upper.isoformat() if route.validity.upper else "∞"
        validity_str = f"[{lower}, {upper})"

        
        days_str = ", ".join(map(str, sorted(route.days_of_week)))

        
        total_seconds = int(route.duration.total_seconds())
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        duration_str = f"{h:02d}:{m:02d}:{s:02d}"

        return cls(
            route_no=str(route.route_no),
            validity=validity_str,
            departure_airport=str(route.departure_airport),
            arrival_airport=str(route.arrival_airport),
            airplane_code=str(route.airplane_code),
            days_of_week=days_str,
            scheduled_time=route.scheduled_time.strftime("%H:%M:%S"),
            duration=duration_str
        )