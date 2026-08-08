from utils.config import config
from database.sqlite_connector import SQLiteConnector
from database.database_connector_abc import DatabaseConnector

_CONNECTORS = {
    "sqlite3": SQLiteConnector,
    #"postgrest": PostgrestConnector, ...
}

def get_connector() -> DatabaseConnector:
    db_type = config.target_database.type
    connector_class = _CONNECTORS.get(db_type)
    if connector_class is None:
        raise ValueError(f"Not supported database: {db_type}")
    return connector_class(config.target_database)