import logging 
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from dataclasses import dataclass, field

@dataclass
class QueryResult:
    query: str
    success: bool
    rows: list[dict] = field(default_factory=list)
    row_count: int = 0
    truncated: bool = False
    error: str | None = None