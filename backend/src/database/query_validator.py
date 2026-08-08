import sqlglot
from sqlglot import exp
from models.query_analysis import QueryAnalysis

_FORBIDDEN_NODE_TYPE = (
    exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Alter, exp.Create
)

class QueryValidationException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

def validate_query(query: str, allowed_tables: list[str] | None = None) -> QueryAnalysis:
    try: 
        parsed = sqlglot.parse_one(query)
    except Exception as e:
        raise QueryValidationException(f"Not valid query for sql: {e}")

    if not isinstance(parsed, exp.Select):
        raise QueryValidationException(f"Only SELECT query are allowed")

    for forbidden_type in _FORBIDDEN_NODE_TYPE:
        if parsed.find(forbidden_type):
            raise QueryValidationException(f"Query with not allowed operation (only SELECT is allowed)")

    tables = sorted({t.name for t in parsed.find_all(exp.Table)})

    if allowed_tables is not None:
        not_allowed = [t for t in tables not in allowed_tables]
        if not_allowed:
            raise QueryValidationException(f"Inssuficient permits for {', '.join(not_allowed)}")

    return QueryAnalysis(tables=tables, is_write=False)