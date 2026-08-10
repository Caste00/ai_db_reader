from rag.vector_store import VectorStore
from utils.embedding import get_embedding


store_table = VectorStore("table_schemas")
store_column = VectorStore("column_schemas")

def retrieve(question: str) -> dict:
    embedding_question = get_embedding(question)

    result_tables = store_table.query(embedding_question)
    result_columns = store_column.query(embedding_question)

    selected_names = {m["table_name"] for m in result_tables["metadatas"][0]}
    already_added = set()

    for col_meta, col_distance in zip(result_columns["metadatas"][0], result_columns["distances"][0]):
        table_name = col_meta["table_name"]

        if table_name in selected_names or table_name in already_added:
            continue

        missing = store_table.get(ids=[table_name])
        if not missing["metadatas"]:
            continue

        result_tables["metadatas"][0].append(missing["metadatas"][0])
        result_tables["documents"][0].append(missing["documents"][0])
        result_tables["distances"][0].append(col_distance)
        already_added.add(table_name)

    return {
        "tables": result_tables,
        "columns": result_columns
    }
