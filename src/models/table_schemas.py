from dataclasses import dataclass, field
from typing import Optional 

@dataclass
class TableSchemas:
    table_name: str = ""
    description: str = ""
    columns: list[str] = field(default_factory=list)
    foreign_keys: list[str] = field(default_factory=list)
    embedding: Optional[list[float]] = None
    distance: Optional[float] = None

    def to_chroma_entry(self) -> tuple[str, str, list[float], dict]:
        metadata = {
            "table_name": self.table_name,
            "columns": ",".join(self.column),
            "foreign_keys": ",".join(self.foreign_keys),
        }

        return self.table_name, self.description, self.embedding, metadata

    @staticmethod
    def from_chroma_result(id_: str, document: str, metadata: dict, embedding: Optional[list[float]] = None, distance: Optional[float] = None) -> "TableSchemas":
        assert id_ == metadata["table_name"], f"id/metadata misaligned: {id_} != {metadata['table_name']}"

        return TableSchemas(
            table_name = metadata["table_name"],
            description = document,
            columns = metadata["columns"].split(",") if metadata["columns"] else [],
            foreign_keys = metadata["foreign_keys"].split(",") if metadata["foreign_keys"] else [],
            embedding = embedding,
            distance = distance
        )