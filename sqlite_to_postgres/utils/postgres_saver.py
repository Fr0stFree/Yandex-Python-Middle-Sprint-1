from dataclasses import astuple
import re

from psycopg2.extensions import connection as PGConnection

from .schemas import Model
from .utils import to_snake_case


class PostgresSaver:
    def __init__(self, connection: PGConnection) -> None:
        self._connection = connection

    def save_data(self, data: tuple[Model, ...]) -> None:
        table_name = to_snake_case(data[0].__class__.__name__)
        values = tuple(astuple(row) for row in data)
        index_pattern = re.compile(r'\((.*)\)')
        statement = f"""
            SELECT indexdef
            FROM pg_indexes
            WHERE tablename = \'{table_name}\';
        """

        with self._connection.cursor() as cursor:
            cursor.execute(statement)
            indexes_strings = cursor.fetchall()

            indexes = [
                index_pattern.search(index_string[0]).group(1).split(', ')
                for index_string in indexes_strings
            ]
            indexes.sort(key=len, reverse=True)

            statement = f"""
                INSERT INTO content.{table_name}
                VALUES ({', '.join(['%s'] * len(values[0]))})
                ON CONFLICT ({', '.join(indexes[0])}) DO NOTHING;
            """

            cursor.executemany(statement, values)
