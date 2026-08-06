#esecuzione con limit/timeout, cattura errore per retry
import logging 
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from dataclasses import dataclass, field
from database.connection import get_connector
from database.database_connector_abc import DatabaseConnector
from database.query_result import QueryResult

logger = logging.getLogger(__name__)

DEFAULT_MAX_ROWS = 200
DEFALUT_TIMEOUT_SECONDS = 5.0

def execute_queries (queries: list[str], connector: DatabaseConnector | None = None, max_rows: int = DEFAULT_MAX_ROWS, timeout_seconds: float = DEFALUT_TIMEOUT_SECONDS) -> list[QueryResult]:
    own_connector = connector is None
    if own_connector: 
        connector = get_connector()
        connector.connect()

    try: 
        return [_execute_single(connector, q, max_rows, timeout_seconds) for q in queries]
    finally:
        if own_connector:
            connector.close()

def _execute_single(connector: DatabaseConnector, query: str, max_rows: int, timeout_seconds: float) -> QueryResult:
    query = query.strip().rstrip(";")
    if not query:
        return QueryResult(query=query, success=False, error="Empty query")

    try:
        analysis = connector.analyze_query(query)
    except Exception as e:
        logger.warning(f"Analysis of failed query ({e}); executing it anyway: {query}")
        analysis = None

    if analysis is not None and analysis.is_write:
        logger.warning(f"Write query blocked: {query}")
        return QueryResult(query=query, success=False, error="Only read-only queries (SELECT) are permitted at this stage.")

    with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(connector.execute_query, query)
            try:
                rows = future.result(timeout=timeout_seconds)
            except FutureTimeoutError:
                logger.warning(f"Query timed out ({timeout_seconds}): {query}")
                return QueryResult(query=query, success=False, error=f"Timeout: the query execeeded the execution time (execution time: {timeout_seconds}s).",
                )
            except Exception as e:
                logger.warning("Errore durante l'esecuzione della query '%s': %s", query, e)
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