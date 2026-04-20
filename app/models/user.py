from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    password_hash: str
    role: str  

@dataclass
class UserDTO:
    username: str
    password: str
    role: Optional[str] = 'user'