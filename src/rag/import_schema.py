from database.connection import get_connector
from models.column_schemas import ColumnSchema
from models.table_schemas import TableSchema


def _build_schema_object(table_name: str, connector) -> tuple[TableSchema, list[ColumnSchema]]:
    raw = connector.get_table_schemas(table_name)

    table_schema = TableSchema(
        table_name = table_name,
        description = "",
        columns = [col["name"] for col in raw["columns"]],
        foreign_keys = raw["foreign_keys"],
    )

    column_schemas = [
        ColumnSchema(
            table_name = table_name,
            column_name = col["name"],
            description = "",
            data_type = col["type"]
        )
        for col in raw["columns"]
    ]

    return table_schema, column_schemas


def import_table(table_name: str) -> tuple[TableSchema, list[ColumnSchema]]:
    """Extraction of one table"""
    connector = get_connector()
    connector.connect()
    try:
        return _build_schema_object(table_name, connector)
    finally:
        connector.close()


def import_all_tables() -> list[tuple[TableSchema, list[ColumnSchema]]]:
    """Extraction of all table"""
    connector = get_connector()
    connector.connect()
    try:
        table_names = connector.get_table_names()
        return [_build_schema_object(name, connector) for name in table_names]
    finally:
        connector.close()