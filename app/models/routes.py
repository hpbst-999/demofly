from dataclasses import dataclass, field
from datetime import  time, timedelta
from typing import List, Optional
from psycopg2.extras import DateTimeTZRange

@dataclass
class Routes:
    route_no: str
    departure_airport: str
    arrival_airport: str
    airplane_code: str
    days_of_week: List[int]
    scheduled_time: time
    duration: timedelta
    validity: Optional[DateTimeTZRange]=None
    departure_airport_name: str = ""
    arrival_airport_name: str = ""
    departure_city: str = ""
    arrival_city: str = ""
    model: str = ""


@dataclass
class RoutesDTO:
    route_no: str
    departure_airport: str
    arrival_airport: str
    airplane_code: str
    days_of_week: str
    scheduled_time: str
    duration: str
    validity: str = ""
    departure_airport_name: str = ""
    arrival_airport_name: str = ""
    departure_city: str = ""
    arrival_city: str = ""
    model: str = ""
    v_start:str = ""
    v_end:str = ""

    @classmethod
    def convert_to_dto(cls, route: Routes) -> 'RoutesDTO':
        lower = route.validity.lower.isoformat() if route.validity and route.validity.lower else "-∞"
        upper = route.validity.upper.isoformat() if route.validity and route.validity.upper else "∞"
        validity_str = f"[{lower},{upper})"
        
        days_str = ','.join(map(str, route.days_of_week))
        
        total_seconds = int(route.duration.total_seconds())
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        duration_str = f"{h:02d}:{m:02d}:{s:02d}"
        
        scheduled_time_str = route.scheduled_time.strftime('%H:%M:%S') if route.scheduled_time else ""

        return cls(
            route_no=route.route_no,
            validity=validity_str,
            departure_airport=route.departure_airport,
            departure_airport_name=route.departure_airport_name,
            arrival_airport=route.arrival_airport,
            arrival_airport_name=route.arrival_airport_name,
            airplane_code=route.airplane_code,
            days_of_week=days_str,
            scheduled_time=scheduled_time_str,
            duration=duration_str,
            departure_city=route.departure_city,
            arrival_city=route.arrival_city,
            model=route.model,
            v_start = "",
            v_end = ""
        )