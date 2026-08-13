import json
from rag.indexer import index_table, index_all_tables
from llm.chat import ask

def launch_cli():
    running = True

    while running:
        user_message = str(input(">>> ")).strip()

        if user_message[0] == "\\":
            message = user_message[1:].split(" ")
            if len(message) == 2 and message[0] == "index":
                print(f"Indexing {message[1]}\nThis operation may take some minutes")
                index_table(message[1])
                print("Finish")
            elif user_message[1:] == "index all tables":
                print("Indexing all tables\nThis operation may take several minutes")
                index_all_tables()
                print("Finish")
            elif message[0] == "bye" or message[0] == "exit":
                running = False
            else:
                print("Command:\n\\help -> list of command\n\\bye -> exit\n\\index all tables-> index all tables\n\\index table_name -> index of table_name")
        else:
            answer, result = ask(user_message)

            print(f"\n{answer}\n")