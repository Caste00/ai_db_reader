from dataclasses import dataclass, field
from typing import Optional 

@dataclass
class ColumnSchema:
    table_name: str
    column_name: str
    description: str
    data_type: str = ""
    embedding: Optional[list[float]] = None
    distance: Optional[float] = None

    @property
    def id(self) -> str:
        return f"{self.table_name}.{self.column_name}"

    def to_chroma_entry(self) -> tuple[str, str, list[float], dict]:
        metadata = {
            "table_name": self.table_name,
            "column_name": self.column_name,
            "data_type": self.data_type,
        }
        return self.id, self.description, self.embedding, metadata

    @staticmethod
    def from_chroma_result(id_: str, document: str, metadata: dict, embedding: Optional[list[float]] = None, distance: Optional[float] = None) -> "ColumnSchema":
        expected_id = f"{metadata['table_name']}.{metadata['column_name']}"
        assert id_ == expected_id, f"id/metadata disallineati: {id_} != {expected_id}"

        return ColumnSchema(
            table_name=metadata["table_name"],
            column_name=metadata["column_name"],
            description=document,
            data_type=metadata.get("data_type", ""),
            embedding=embedding,
            distance=distance,
        )