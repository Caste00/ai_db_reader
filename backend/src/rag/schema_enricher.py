import json
from llm.providers.ollama import generate
from models.table_schemas import TableSchema
from models.column_schemas import ColumnSchema
from utils.json_parsing import strip_code_fences
from utils.prompt import get_prompt


def enrich_table(table_schema: TableSchema, column_schemas: list[ColumnSchema]) -> tuple[TableSchema, list[ColumnSchema]]:
    """return TableSchema and a list of ColumnSchema with the description"""
    prompt = get_prompt("schema_enrichment.user",
        table_name=table_schema.table_name,
        columns=table_schema.columns,
        foreign_keys=table_schema.foreign_keys,
    )

    raw_response = strip_code_fences(generate(prompt, json_mode=True))

    try:
        enriched = json.loads(raw_response)
    except json.JSONDecodeError:
        # fallback: nessun arricchimento, gli oggetti restano con description vuota
        print(f"Error with {table_schema.table_name}: raw response was {raw_response}")
        return table_schema, column_schemas

    table_schema.description = enriched.get("table_description", "")

    columns_data = enriched.get("columns", {})
    for column in column_schemas:
        col_info = columns_data.get(column.column_name, {})
        column.description = col_info.get("description", "")
        column.synonyms = col_info.get("synonyms", [])

    return table_schema, column_schemas