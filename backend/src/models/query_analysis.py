from dataclasses import dataclass, field

@dataclass
class QueryAnalysis:
    """
    Result of a query analysis performed directly by the database engine
    (e.g., via EXPLAIN), rather than by a text parser.

    tables: names of the "actual" tables accessed by the query (no aliases, no subqueries/CTEs resolved by internal names).
    is_write: True if the query involves even a single write operation (INSERT/UPDATE/DELETE/DDL...), regardless of how the query itself is written.
    """

    tables: list[str] = field(default_factory=list) 
    is_write: bool = False