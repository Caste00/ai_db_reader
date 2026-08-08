from sqlalchemy import create_engine, inspect, text
from database.database_connector_abc import DatabaseConnector

class SQLAlchemyConnector(DatabaseConnector):
    def __init__(self, db_config):
        self.url = db_config.url
        self.engine = None
        self.conn = None

    def connect(self):
        self.engine = create_engine(self.url)
        self.conn = self.engine.connect()

    def close(self):
        if self.conn:
            self.conn.close()
        if self.engine:
            self.engine.dispose()

    def get_table_names(self):
        return inspect(self.engine).get_table_names()

    def get_table_schemas(self, table_name):
        inspector = inspect(self.engine)

        columns = [
            {"name": col["name"], "type": str(col["type"])}
            for col in inspector.get_columns(table_name)
        ]

        foreign_keys = [
            {"column": local_col, "references_table": fk["referred_table"], "references_column": ref_col}
            for fk in inspector.get_foreign_keys(table_name)
            for local_col, ref_col in zip(fk["constrained_columns"], fk["referred_columns"])
        ]

        return {"columns": columns, "foreign_keys": foreign_keys}

    def execute_query(self, query: str, params: tuple = ()) -> list[dict]:
        result = self.conn.execute(text(query))
        return [dict(row) for row in result.mappings().all()]