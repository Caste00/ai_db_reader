from rag.context_builder import build_schema_context, build_prompt
from rag.retriever import retrieve
from rag.indexer import index_all_tables
from llm.providers.ollama import generate

def main():
    domanda = "Che nome ha l'artista con id 191?"
    a = retrieve(domanda)
    b = build_schema_context(a)
    c = build_prompt(domanda, b)

    print(b)
    print(c)


if __name__ == "__main__":
    main()