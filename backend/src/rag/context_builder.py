from typing import Any
from utils.config import config
from utils.prompt import get_prompt
from database.query_result import QueryResult


def _filter_by_distance(metadatas: list[dict], documents: list[str], distances: list[float], threshold: float) -> tuple[list[dict], list[str]]:
    keep_meta, keep_doc = [], []

    for meta, doc, dist in zip(metadatas, documents, distances):
        if dist <= threshold:
            keep_meta.append(meta)
            keep_doc.append(doc)
    return keep_meta, keep_doc


def build_schema_context(retrieval_result: dict[str, Any]) -> str:
    """Cleans and merges the results of tables and columns into a compact, readable DB‑schema block to pass to the LLM"""

    threshold = config.vector_store.distance_threshold

    table_meta = retrieval_result["tables"]["metadatas"][0]
    table_docs = retrieval_result["tables"]["documents"][0]
    col_meta = retrieval_result["columns"]["metadatas"][0]

    table_meta, table_docs = _filter_by_distance(
        retrieval_result["tables"]["metadatas"][0],
        retrieval_result["tables"]["documents"][0],
        retrieval_result["tables"]["distances"][0],
        threshold,
    )

    col_meta, _ = _filter_by_distance(
        retrieval_result["columns"]["metadatas"][0],
        retrieval_result["columns"]["documents"][0],
        retrieval_result["columns"]["distances"][0],
        threshold,
    )


    extra_by_table: dict[str, list[str]] = {}
    for meta in col_meta:
        extra_by_table.setdefault(meta["table_name"], []).append(
            f"{meta['column_name']} ({meta['data_type']})"
        )

    if not table_meta:
        return ""

    blocks = []
    for meta, doc in zip(table_meta, table_docs):
        table_name = meta["table_name"]
        lines = [f"### Table: {table_name}"]
        if doc.strip():
            lines.append(f"Description: {doc.strip()}")
        lines.append(f"Columns: {meta['columns']}")
        lines.append(f"Foreign keys: {meta['foreign_keys'] or 'none'}")
        if table_name in extra_by_table:
            lines.append(f"Relevant columns: {', '.join(extra_by_table[table_name])}")
        blocks.append("\n".join(lines))

    return "\n\n".join(blocks)


def build_prompt(question: str, schema_context: str) -> list[dict]:
    """Builder of message (system + user) for the query generation"""
    system_prompt = get_prompt("sql_generation.system", target_database=config.target_database.type , schema_context=schema_context)
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]


def build_answer_prompt(question: str, results: list["QueryResult"]) -> list[dict]:
    successful = [r for r in results if r.success]

    if not successful:
        errors = "\n".join(r.error for r in results if r.error)
        data_block = f"None of the queries succeeded:\n{errors}"
    else:
        data_block = "\n\n".join(
            f"Query: {r.query}\nResults ({r.row_count} rows): {r.rows}"
            for r in successful
        )

    system_prompt = get_prompt("answer_synthesis.system", data_block=data_block)

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]