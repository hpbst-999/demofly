from dataclasses import dataclass
from datetime import datetime
from typing import List, Any, Optional
@dataclass
class Table_dto_request:
    page:int
    search_query: Optional[str] = None

@dataclass
class Table_dto_search:
    offset: int
    limit: int
    search_query: Optional[str] = None

@dataclass
class Table_dto_response:
    data: List[Any]          
    columns: List[str]       
    has_next: bool = False   

@dataclass
class Main_dto_request:
    from_city:str
    to_city:str
    date_start:datetime
    date_end:datetime
    page:int

@dataclass
class Main_dto_search: 
    from_city:str
    to_city:str
    date_start:datetime
    date_end:datetime
    offset: int
    limit: int


