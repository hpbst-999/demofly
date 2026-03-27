from dataclasses import dataclass
@dataclass
class Airplanes:
    airplane_code: str
    model: str
    range: int
    speed: int

@dataclass
class AirplanesDTO:
    airplane_code: str
    model: str
    range: str
    speed: str
    
    @classmethod
    def convert_to_dto(cls, airplane: Airplanes) -> 'AirplanesDTO':
        return cls(
            airplane_code=str(airplane.airplane_code),
            model=str(airplane.model),
            range=str(airplane.range),
            speed=str(airplane.speed)
        )