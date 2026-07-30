from rag.vector_store import VectorStore
from utils.embedding import get_embedding


store_table = VectorStore("table_schemas")
store_column = VectorStore("column_schemas")

def retrieve(question: str) -> dict:
    embedding_question = get_embedding(question)

    result_tables = store_table.query(embedding_question)
    result_columns = store_column.query(embedding_question)

    return {
        "tables": result_tables,
        "columns": result_columns
    }
