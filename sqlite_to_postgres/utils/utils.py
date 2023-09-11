import re
from psycopg2.extensions import cursor as PGCursor

def to_snake_case(string: str) -> str:
    """Преобразует строку в snake_case"""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


def locate_table_indexes(cursor: PGCursor, table_name: str) -> list[list[str], ...]:
    """Возвращает список индексов таблицы, отсортированный по количеству полей ASC"""
    index_pattern = re.compile(r'\((.*)\)')
    statement = f"""
        SELECT indexdef
        FROM pg_indexes
        WHERE tablename = \'{table_name}\';
    """

    cursor.execute(statement)
    indexes_strings = cursor.fetchall()
    indexes = [
        index_pattern.search(index_string[0]).group(1).split(', ')
        for index_string in indexes_strings
    ]
    indexes.sort(key=len, reverse=True)
    return indexes
