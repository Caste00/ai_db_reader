# stato sessione corrente (id conversazione attiva, tabelle già selezionate nei turni precedenti)
from memory.crud import get_all_messages
from utils.config import config

CONTEXT_WINDOW = config.message.context_window

def message_context_builder(question: str, chat_id: int):
    """Add the old message before the new one"""
    messages = get_all_messages(chat_id)
    lines = ["Old messages: "]
    for message in messages[-CONTEXT_WINDOW:]:
        lines.append(f"{message.role}: {message.content}")
    lines.append(f"New message:\n{question}")

    return "\n".join(lines)