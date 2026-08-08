#esecuzione con limit/timeout, cattura errore per retry
import logging 
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from database.query_validator import validate_query, QueryValidationException
from database.connection import get_connector
from database.database_connector_abc import DatabaseConnector
from database.query_result import QueryResult

logger = logging.getLogger(__name__)

DEFAULT_MAX_ROWS = 200
DEFALUT_TIMEOUT_SECONDS = 5.0

def execute_queries (queries: list[str], connector: DatabaseConnector | None = None, max_rows: int = DEFAULT_MAX_ROWS, timeout_seconds: float = DEFALUT_TIMEOUT_SECONDS, allowed_tables: list[str] | None = None) -> list[QueryResult]:
    own_connector = connector is None
    if own_connector: 
        connector = get_connector()
        connector.connect()

    try: 
        return [_execute_single(connector, q, max_rows, timeout_seconds, allowed_tables) for q in queries]
    finally:
        if own_connector:
            connector.close()

def _execute_single(connector: DatabaseConnector, query: str, max_rows: int, timeout_seconds: float, allowed_tables: list[str] | None = None) -> QueryResult:
    query = query.strip().rstrip(";")
    if not query:
        return QueryResult(query=query, success=False, error="Empty query")

    try:
        validate_query(query, allowed_tables=allowed_tables)
    except QueryValidationException as e:
        logger.warning(f"Query rejected: {e.message}")
        return QueryResult(query=query, success=False, error=e.message)

    with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(connector.execute_query, query)
            try:
                rows = future.result(timeout=timeout_seconds)
            except FutureTimeoutError:
                logger.warning(f"Query timed out ({timeout_seconds}): {query}")
                return QueryResult(query=query, success=False, error=f"Timeout: the query execeeded the execution time (execution time: {timeout_seconds}s).",
                )
            except Exception as e:
                logger.warning("Error while executing the query: '%s': %s", query, e)
                return QueryResult(query=query, success=False, error=str(e))

    truncated = len(rows) > max_rows
    if truncated:
        rows = rows[:max_rows]

    return QueryResult(
        query=query,
        success=True,
        rows=rows,
        row_count=len(rows),
        truncated=truncated,
    )