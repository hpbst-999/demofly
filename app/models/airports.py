from dataclasses import dataclass
from typing import Tuple
@dataclass
class Airports:
    airport_code: str
    airport_name: str
    city: str
    country: str
    coordinates:Tuple[float, float]
    timezone:str

@dataclass
class AirportsDTO:
    airport_code: str
    airport_name: str
    city: str
    country: str
    coordinates: str
    timezone: str
    
    @classmethod
    def convert_to_dto(cls, airport: Airports) -> 'AirportsDTO':
        
        return cls(
            airport_code=str(airport.airport_code),
            airport_name=str(airport.airport_name),
            city=str(airport.city),
            country=str(airport.country),
            coordinates=str(airport.coordinates),
            timezone=str(airport.timezone)
        )

