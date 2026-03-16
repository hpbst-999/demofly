from dataclasses import dataclass
from typing import Optional

@dataclass
class Table_dto_request:
    table_name: str
    search_query: Optional[str] = None
    row_id: Optional[str] = None
    full_row: Optional[str] = None

@dataclass
class Table_dto_search:
    table_name: str
    columns: Optional[str] = None
    search_query: Optional[str] = None

