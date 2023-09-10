import os
import sqlite3
from contextlib import closing
from pathlib import Path

import psycopg2
from dotenv import find_dotenv, load_dotenv
from psycopg2.extensions import connection as PGConnection

from utils.sqlite_extractor import SQLiteExtractor
from utils.postgres_saver import PostgresSaver
from utils.schemas import (
    FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork,
)

load_dotenv(find_dotenv('.env'))

POSTGRES_DSL = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
}
SQLITE_PATH = Path('./db.sqlite')


def load_from_sqlite(
    sqlite_connection: sqlite3.Connection,
    pg_connection: PGConnection,
) -> None:
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_extractor = SQLiteExtractor(sqlite_connection)
    postgres_saver = PostgresSaver(pg_connection)

    for model in (FilmWork, Person, Genre, GenreFilmWork, PersonFilmWork):
        for chunk in sqlite_extractor.extract_chunks(model, chunk_size=100):
            postgres_saver.save_data(chunk)
            pg_connection.commit()


if __name__ == '__main__':
    with (
        closing(sqlite3.connect(SQLITE_PATH)) as sqlite_connection,
        closing(psycopg2.connect(**POSTGRES_DSL)) as pg_connection,
    ):
        load_from_sqlite(sqlite_connection, pg_connection)

