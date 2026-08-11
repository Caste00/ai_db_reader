from memory.crud import get_all_messages
from utils.config import config

CONTEXT_WINDOW = config.message.context_window

def message_context_builder(question: str, chat_id: int):
    """Add the old message before the new one"""
    messages = get_all_messages(chat_id)
    enricher = "Old message:\n"

    for message in messages[-CONTEXT_WINDOW:]:
        text = f"User_role: {message.role}, message: {message.content}\n"
        enricher.join(text)
    enricher.join("New message:\n")

    return question.join(enricher)