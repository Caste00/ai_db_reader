from abc import ABC, abstractmethod

class DatabaseConnector(ABC):
    """Common interface for every supported database engine."""

    @abstractmethod
    def connect(self) -> None:
        """Opens the database connection"""

    @abstractmethod
    def close(self) -> None:
        """Close the database connection"""

    @abstractmethod
    def get_table_names(self) -> list[str]:
        """Returns the list of all tables name in the database"""

    @abstractmethod
    def get_table_schemas(self, table_name) -> dict:
        """
        Returns the schema of a table, including columns and foreign keys.

        Format: 
        "columns": [
            {"name": ..., "type": ...}
        ],
        "foreign_keys": [
            {"column": ..., "references_table": ..., "references_column": ...}
        ]
        """

    @abstractmethod
    def execute_query(self, query: str, params: tuple = ()) -> list[dict]:
        """Execute a SELECT query and return the rows as a list of dictionaries"""