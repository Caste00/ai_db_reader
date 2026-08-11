import json
from database.query_executor import execute_queries
from database.query_result import QueryResult
from rag.retriever import retrieve
from rag.context_builder import build_prompt, build_schema_context, build_answer_prompt
from llm.providers.ollama import generate, LLMGenerationError
from utils.json_parsing import strip_code_fences
from utils.config import config


def ask(question: str, allowed_tables: list[str] | None = None) -> tuple[str, list[QueryResult]]:
    retrieval = retrieve(question)
    schema_context = build_schema_context(retrieval)
    message = build_prompt(question, schema_context)

    queries, explanation, raw_response = _generate_queries(message)

    if not queries:
        return explanation or "I was unable to generate a valid query for this question.", []

    result = execute_queries(queries, allowed_tables=allowed_tables)
    attempt = 1

    while any(not r.success for r in result) and attempt < config.ask.max_attempts:
        failed = [r for r in result if not r.success]
        message.append({"role": "assistant", "content": raw_response})
        message.append({"role": "user", "content": _build_correction_message(failed)})

        queries, explanation, raw_response = _generate_queries(message)
        if not queries:
            break

        result = execute_queries(queries, allowed_tables=allowed_tables)
        attempt += 1

    return _summarize_results(question, result), result


def _generate_queries(message: list[dict]) -> tuple[list[str], str, str]:
    """Return queries, explanation, raw_response"""
    try:
        raw_response = generate(message, json_mode=True)
    except LLMGenerationError as e:
        return [], f"Error of the model: {e.message}", ""

    try:
        parsed = json.loads(strip_code_fences(raw_response))
    except json.JSONDecodeError:
        return [], "The response from the model isn't valid", raw_response

    return parsed.get("queries", []), parsed.get("explanation", ""), raw_response


def _build_correction_message(failed_result: list[QueryResult]) -> str:
    lines = ["Some queries failed. Correct them and return ONLY the requested JSON again.", ""]
    for r in failed_result:
        lines.append(f"Query: {r.query}\nError: {r.error}")
    return "\n\n".join(lines)


def _summarize_results(question: str, results: list[QueryResult]) -> str:
    message = build_answer_prompt(question, results)
    try:
        return generate(message)
    except LLMGenerationError as e:
        return f"The queries were executed, but I was unable to formulate a response: {e.message}"