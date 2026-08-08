import json
from llm.ollama import generate
from models.table_schemas import TableSchema
from models.column_schemas import ColumnSchema

ENRICH_PROMPT = """Given this SQL table, generate a description of the table and, for each column, a description plus possible synonyms/alternative terms that a user might use in natural language to refer to that column.

Table: {table_name}
Columns: {columns}
Foreign key: {foreign_keys}

Respond ONLY with a valid JSON in this format, nothing else (no markdown, no text outside the JSON):
{{
  "table_description": "...",
  "columns": {{
    "column_name": {{"description": "...", "synonyms": ["...", "..."]}}
  }}
}}
"""

def enrich_table(table_schema: TableSchema, column_schemas: list[ColumnSchema]) -> tuple[TableSchema, list[ColumnSchema]]:
    """return TableSchema and a list of ColumnSchema with the description"""
    prompt = ENRICH_PROMPT.format(
        table_name=table_schema.table_name,
        columns=table_schema.columns,
        foreign_keys=table_schema.foreign_keys,
    )

    raw_response = generate(prompt)

    try:
        enriched = json.loads(raw_response)
    except json.JSONDecodeError:
        # fallback: nessun arricchimento, gli oggetti restano con description vuota
        return table_schema, column_schemas

    table_schema.description = enriched.get("table_description", "")

    columns_data = enriched.get("columns", {})
    for column in column_schemas:
        col_info = columns_data.get(column.column_name, {})
        column.description = col_info.get("description", "")
        column.synonyms = col_info.get("synonyms", [])

    return table_schema, column_schemas
        