import json 
import re
import logging

from llm.ollama import generate, LLMGenerationError
from rag.context_builder import build_prompt, build_schema_context
from rag.retriever import retrieve
from database.query_executor import execute_queries 
from database.query_result import QueryResult

MAX_ATTEMPTS = 5
logger = logging.getLogger(__name__)

def _extract_json(raw_response: str) -> dict | None:
    match = re.search(r"\{.*\}", raw_response, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def _build_answer_prompt(question: str, results: list[QueryResult]) -> list[dict]:
    """Builds the prompt that turns the raw query results into a natural language answer."""
    results_text = "\n\n".join(
        f"Query: {r.query}\nResult: {r.rows if r.success else f'ERROR: {r.error}'}"
        for r in results
    )

    system_prompt = f"""You are a helpful assistant. Answer the user's question in a clear, natural way,
    using ONLY the query results below. Do not mention SQL, tables, or columns unless the user asked about them.

    QUERY RESULTS:
    {results_text}"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]


def ask(question: str) -> tuple[str, list[QueryResult]]:
    schema_context = build_schema_context(retrieve(question))
    messages = build_prompt(question, schema_context)

    results: list[QueryResult] = []

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            raw_response = generate(messages)
        except LLMGenerationError as e:
            return f"LLM error: {e.message}", []

        parsed = _extract_json(raw_response)
        if parsed is None:
            logger.warning("Non-JSON response on attempt %d: %s", attempt, raw_response)
            messages.append({"role": "assistant", "content": raw_response})
            messages.append({
                "role": "user",
                "content": "The previous response was not valid JSON. Reply ONLY with the requested JSON, without any surrounding text or markdown."
            })
            continue

        queries = parsed.get("queries", [])

        if not queries:
            return parsed.get("explanation", ""), []

        results = execute_queries(queries)
        failed = [r for r in results if not r.success]

        if not failed:
            break

        if attempt == MAX_ATTEMPTS:
            break

        messages.append({"role": "assistant", "content": raw_response})
        messages.append({
            "role": "user",
            "content": (
                "One or more queries failed. Fix ONLY the failed queries, keeping the same "
                "JSON output format.\n\n" +
                "\n".join(f"Query: {r.query}\nError: {r.error}" for r in failed)
            )
        })

    if not results:
        return "Could not generate a valid query.", []

    try:
        answer = generate(_build_answer_prompt(question, results))
    except LLMGenerationError as e:
        logger.warning("LLM error while composing the final answer: %s", e.message)
        answer = ""

    return answer, results