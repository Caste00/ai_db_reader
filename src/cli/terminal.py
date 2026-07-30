from rag.indexer import index_table, index_all_tables
from llm.ollama import generate, LLMGenerationError
from rag.context_builder import build_prompt, build_schema_context
from rag.retriever import retrieve

def launch_cli():
    running = True

    while running:
        user_message = str(input(">>>")).strip()

        if (user_message == "/help"):
            print("Command:\n/help -> list of command\n/bye -> exit\n/index all tables-> index all tables\n/index table_name -> index of table_name")
        elif(user_message == "/index all tables"):
            print("inidicizzazione di tutte le tabelle\nQuesta operazione potrebbe richiedere diversi minuti")
            index_all_tables()
            print("Completato")
        #elif(user_message.startswith("/index ")):
            # TODO
            #print("Funzione ancora da implementare")
        elif(user_message == "/bye" or user_message == "/exit"):
            running = False
        else:
            schema_context = build_schema_context(retrieve(user_message))
            messages = build_prompt(user_message, schema_context)

            try:
                raw_response = generate(messages)
            except LLMGenerationError as e:
                print(f"Errore LLM: {e.message}")
                continue

            print(raw_response)