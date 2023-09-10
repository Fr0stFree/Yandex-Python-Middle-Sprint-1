import sqlite3
from typing import Generator

from .schemas import Model
from .utils import to_snake_case


class SQLiteExtractor:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def extract_chunks(
        self,
        model: Model,
        chunk_size: int = 100,
    ) -> Generator[tuple[Model, ...], None, None]:
        """Генератор для извлечения данных из SQLite"""
        table_name = to_snake_case(model.__name__)
        fields_to_fetch = list(model.__dataclass_fields__.keys())
        statement = f'SELECT {", ".join(fields_to_fetch)} FROM {table_name}'

        result = self._connection.execute(statement)

        while True:
            if not (chunk := result.fetchmany(chunk_size)):
                break

            yield tuple(model(*row) for row in chunk)
