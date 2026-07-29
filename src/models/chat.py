from dataclasses import dataclass
from typing import Optional 
from datetime import datetime

@dataclass
class Chat:
    id: Optional[int] = None
    user_id: Optional[int] = None
    title: str = ""
    created_at: Optional[datetime] = None

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "created_at": self.created_at
        }

    @staticmethod
    def from_row(row: tuple) -> "Chat":
        return Chat(
            id = row["id"],
            user_id = row["user_id"],
            title = row["title"],
            created_at = row["created_at"]
        )