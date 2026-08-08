from typing import Any

def build_schema_context(retrieval_result: dict[str, Any]) -> str:
    """Cleans and merges the results of tables and columns into a compact, readable DB‑schema block to pass to the LLM"""

    table_meta = retrieval_result["tables"]["metadatas"][0]
    table_docs = retrieval_result["tables"]["documents"][0]
    col_meta = retrieval_result["columns"]["metadatas"][0]

    extra_by_table: dict[str, list[str]] = {}
    for meta in col_meta:
        extra_by_table.setdefault(meta["table_name"], []).append(
            f"{meta['column_name']} ({meta['data_type']})"
        )

    blocks = []
    for meta, doc in zip(table_meta, table_docs):
        table_name = meta["table_name"]
        lines = [f"### Table: {table_name}"]
        if doc.strip():
            lines.append(f"Description: {doc.strip()}")
        lines.append(f"Columns: {meta['columns']}")
        lines.append(f"Foreign keys: {meta['foreign_keys'] or 'none'}")
        if table_name in extra_by_table:
            lines.append(f"Type of relevant columns: {', '.join(extra_by_table[table_name])}")
        blocks.append("\n".join(lines))

    return "\n\n".join(blocks)

# TODO fare in modo che risponda solo a domande sul database 
def build_prompt(question: str, schema_context: str) -> list[dict]:
    """Builder of message (system + user) for the query generation"""
    system_prompt = f"""You are an SQ    L expert. Generate one or more valid SQL queries to answer
    the user's question, based ONLY on the database schema below. Do not invent tables or columns 
    that are not listed.

    DATABASE SCHEMA:
    {schema_context}

    Output rules:

    1) Respond ONLY with valid JSON, without markdown or backticks:
        {{"queries": ["<query1>", "<query2>", ...], "explanation": "<short explanation>"}}

    2) Table/column names in the queries must remain exactly as in the schema (standard SQL).

    3) The "explanation" field must be written in the SAME language as the user's question.

    4) If the question is ambiguous or cannot be answered with the provided schema, explain
        the reason in "explanation" and leave "queries" empty."""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]