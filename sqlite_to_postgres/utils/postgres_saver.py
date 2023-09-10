from dataclasses import astuple

from psycopg2.extensions import connection as PGConnection, cursor as PGCursor

from .schemas import Person, FilmWork, PersonFilmWork, GenreFilmWork, Genre


class PostgresSaver:
    def __init__(self, connection: PGConnection) -> None:
        self._connection = connection

    def save_all_data(self, data: tuple[
        list[Person],
        list[FilmWork],
        list[Genre],
        list[GenreFilmWork],
        list[PersonFilmWork],
    ]) -> None:
        with self._connection.cursor() as cursor:
            self._upsert_persons(cursor, data[0])
            self._upsert_film_works(cursor, data[1])
            self._upsert_genres(cursor, data[2])
            self._upsert_genre_film_works(cursor, data[3])
            self._upsert_person_film_works(cursor, data[4])

        self._connection.commit()

    def _upsert_persons(self, cursor: PGCursor, persons: list[Person]) -> None:
        statement = """
            INSERT INTO content.person (id, full_name, modified, created)
            VALUES (%s, %s, NOW(), NOW())
            ON CONFLICT (id) DO UPDATE SET modified = NOW();
        """

        for person in persons:
            cursor.execute(statement, (person.id, person.full_name))

    def _upsert_film_works(
        self,
        cursor: PGCursor,
        film_works: list[FilmWork],
    ) -> None:
        statement = """
            INSERT INTO content.film_work (
                id, title, description, rating, type, modified, created
            )
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            ON CONFLICT (id) DO UPDATE SET modified = NOW();
        """

        for film_work in film_works:
            cursor.execute(statement, astuple(film_work))

    def _upsert_genres(self, cursor: PGCursor, genres: list[Genre]) -> None:
        statement = """
            INSERT INTO content.genre (id, name, modified, created)
            VALUES (%s, %s, NOW(), NOW())
            ON CONFLICT (id) DO UPDATE SET modified = NOW();
        """

        for genre in genres:
            cursor.execute(statement, astuple(genre))

    def _upsert_genre_film_works(
        self,
        cursor: PGCursor,
        genre_film_works: list[GenreFilmWork],
    ) -> None:
        statement = """
            INSERT INTO content.genre_film_work (
                id, film_work_id, genre_id, created
            )
            VALUES (%s, %s, %s, NOW())
            ON CONFLICT (film_work_id, genre_id) DO NOTHING;
        """

        for genre_film_work in genre_film_works:
            cursor.execute(statement, astuple(genre_film_work))

    def _upsert_person_film_works(
        self,
        cursor: PGCursor,
        person_film_works: list[PersonFilmWork],
    ) -> None:
        statement = """
            INSERT INTO content.person_film_work (
                id, film_work_id, person_id, role, created
            )
            VALUES (%s, %s, %s, %s, NOW())
            ON CONFLICT (film_work_id, person_id) DO NOTHING;
        """

        for person_film_work in person_film_works:
            cursor.execute(statement, astuple(person_film_work))
