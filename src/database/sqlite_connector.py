import sqlite3
from database.database_connector_abc import DatabaseConnector
from models.query_analysis import QueryAnalysis

_READ_OPCODES = {"OpenRead"}
_WRITE_OPCODES = {"OpenWrite"}


class SQLiteConnector(DatabaseConnector):
    def __init__(self, db_config):
        self.db_path = db_config.path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
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

    def analyze_query(self, query: str) -> QueryAnalysis:
        explain_rows = self.conn.execute(f"EXPLAIN {query}").fetchall()

        root_pages = {
            row["rootpage"]: row["tbl_name"]
            for row in self.conn.execute(
                "SELECT tbl_name, rootpage FROM sqlite_master "
                "WHERE type IN ('table', 'index') AND rootpage > 0"
            )
        }

        tables: set[str] = set()
        is_write = False

        for row in explain_rows:
            opcode = row["opcode"]

            if opcode in _WRITE_OPCODES:
                is_write = True

            if opcode in _READ_OPCODES or opcode in _WRITE_OPCODES:
                table_name = root_pages.get(row["p2"])
                if table_name:
                    tables.add(table_name)

        return QueryAnalysis(tables=sorted(tables), is_write=is_write)