import os
import sqlite3

import psycopg2
from dotenv import find_dotenv, load_dotenv
from psycopg2.extensions import connection as PGConnection
from psycopg2.extras import DictCursor

from utils.sqlite_extractor import SQLiteExtractor
from utils.postgres_saver import PostgresSaver

load_dotenv(find_dotenv('.env'))

POSTGRES_DSL: dict = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
}


def load_from_sqlite(
    sqlite_connection: sqlite3.Connection,
    pg_connection: PGConnection,
) -> None:
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_extractor = SQLiteExtractor(sqlite_connection)
    postgres_saver = PostgresSaver(pg_connection)

    data = sqlite_extractor.extract_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    with (
        sqlite3.connect('db.sqlite') as sqlite_conn,
        psycopg2.connect(**POSTGRES_DSL, cursor_factory=DictCursor) as pg_conn,
    ):
        load_from_sqlite(sqlite_conn, pg_conn)
