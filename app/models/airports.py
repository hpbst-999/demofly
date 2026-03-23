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
            airport_name=str(airport.airport_name.get('en', 'N/A')),
            city=str(airport.city.get('en', 'N/A')),
            country=str(airport.country.get('en', 'N/A')),
            coordinates=str(airport.coordinates),
            timezone=str(airport.timezone)
        )