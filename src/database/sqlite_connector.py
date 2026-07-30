import sqlite3
from database.database_connector_abc import DatabaseConnector


class SQLiteConnector(DatabaseConnector):
    def __init__(self, db_config):
        self.db_path = db_config.path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()

    def get_table_names(self) -> list[str]:
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )

        return [row["name"] for row in cursor.fetchall()]

    def get_table_schemas(self, table_name: str) -> dict:
        columns = [
            {"name": row["name"], "type": row["type"]}
            for row in self.conn.execute(f"PRAGMA table_info({table_name})")
        ]

        foreign_keys = [
            {"column": row["from"], "references_table": row["table"], "references_column": row["to"]}
            for row in self.conn.execute(f"PRAGMA foreign_key_list({table_name})")
        ]

        return {"columns": columns, "foreign_keys": foreign_keys}

    def execute_query(self, query: str, params: tuple = ()) -> list[dict]:
        cursor = self.conn.execute(query, params)
        
        return [dict(row) for row in cursor.fetchall()]