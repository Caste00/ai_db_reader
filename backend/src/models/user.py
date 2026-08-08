from dataclasses import dataclass
from typing import Optional 
from datetime import datetime

@dataclass
class User:
    id: Optional[int] = None
    name: str = ""
    password_hash: str = ""
    role: str = ""
    created_at: datetime = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password_hash": self.password_hash,
            "role": self.role,
            "created_at": self.created_at
        }

    @staticmethod
    def from_row(row: tuple) -> "User":
        return User(
            id = row["id"],
            name = row["name"],
            password_hash = row["password_hash"],
            role = row["role"],
            created_at = row["created_at "]
        )