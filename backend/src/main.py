import json
from rag.context_builder import build_schema_context, build_prompt, build_answer_prompt
from rag.retriever import retrieve
from database.query_executor import execute_queries
from llm.providers.ollama import generate
from utils.json_parsing import strip_code_fences

def main():
    domanda = "Quali gruppi hanno fatto uscire canzoni del genere metal?"  

    a = retrieve(domanda)
    b = build_schema_context(a)
    messages = build_prompt(domanda, b)

    raw_response = generate(messages, json_mode=True)
    parsed = json.loads(strip_code_fences(raw_response))
    print("Query generate:", parsed["queries"])

    results = execute_queries(parsed["queries"])
    print("Risultati:", results)

    answer_prompt = build_answer_prompt(domanda, results)
    final_answer = generate(answer_prompt)
    print("\nRisposta finale:", final_answer)

if __name__ == "__main__":
    main()