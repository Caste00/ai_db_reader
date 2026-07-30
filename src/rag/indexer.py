from rag.import_schema import import_all_tables, import_table
from rag.schema_enricher import enrich_table
from rag.vector_store import VectorStore
from utils.embedding import get_embedding

def index_table(table_name: str):
    table_schema, column_schemas = import_table(table_name)
    table_schema, column_schemas = enrich_table(table_schema, column_schemas)

    _upsert_table(table_schema)
    _upsert_columns(column_schemas)


def index_all_tables():
    all_schemas = import_all_tables()

    for table_schema, columns_schema in all_schemas:
        table_schema, columns_schema = enrich_table(table_schema, columns_schema)
        _upsert_table(table_schema)
        _upsert_columns(columns_schema)


def _upsert_table(table_schema):
    table_schema.embedding = get_embedding(table_schema.description or table_schema.table_name)
    id_, document, embedding, metadata = table_schema.to_chroma_entry()

    store = VectorStore("table_schemas")
    store.upsert(ids=[id_], documents=[document], embeddings=[embedding], metadatas=[metadata])


def _upsert_columns(column_schemas):
    if not column_schemas:
        return

    store = VectorStore("column_schemas")
    for column in column_schemas:
        column.embedding = get_embedding(column.description or column.column_name)
        id_, document, embedding, metadata = column.to_chroma_entry()
        store.upsert(ids=[id_], documents=[document], embeddings=[embedding], metadatas=[metadata])
