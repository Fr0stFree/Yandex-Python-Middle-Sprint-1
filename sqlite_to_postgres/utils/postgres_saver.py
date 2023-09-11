from dataclasses import astuple

from psycopg2.extensions import connection as PGConnection

from psycopg2.extras import execute_batch

from .schemas import Model
from .utils import to_snake_case, locate_table_indexes


class PostgresSaver:
    def __init__(self, connection: PGConnection) -> None:
        self._connection = connection

    def save_data(self, data: tuple[Model, ...]) -> None:
        table_name = to_snake_case(data[0].__class__.__name__)
        values = tuple(astuple(row) for row in data)

        with self._connection.cursor() as cursor:
            indexes = locate_table_indexes(cursor, table_name)
            statement = f"""
                INSERT INTO content.{table_name}
                VALUES ({', '.join(['%s'] * len(values[0]))})
                ON CONFLICT ({', '.join(indexes[0])}) DO NOTHING;
            """

            execute_batch(cursor, statement, values, page_size=len(values))

        self._connection.commit()
