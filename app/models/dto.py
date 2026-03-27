from dataclasses import dataclass
from typing import Optional
from datetime import datetime
@dataclass
class Table_dto_request:
    offset: int
    limit: int
    search_query: Optional[str] = None

@dataclass
class Table_dto_search:
    offset: int
    limit: int
    search_query: Optional[str] = None

@dataclass
class Main_dto_request:
    from_city:str
    to_city:str
    date_start:datetime
    date_end:datetime

@dataclass
class Main_dto_search: 
    from_city:str
    to_city:str
    date_start:datetime
    date_end:datetime

@dataclass
class Cud_dto:
    table_name:str
    row_id: dict

