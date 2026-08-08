from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Message:
    id: Optional[int] = None
    chat_id: Optional[int] = None
    role: str = ""
    content: str = ""
    created_at: Optional[datetime] = None

    def to_dict(self):
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at
        }

    @staticmethod
    def from_row(row: tuple) -> "Message":
        return Message(
            id = row["id"],
            chat_id = row["chat_id"],
            role = row["role"],
            content = row["content"],
            created_at = row["created_at"]
        )