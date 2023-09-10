import sqlite3

from .schemas import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


class SQLiteExtractor:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def extract_movies(self) -> tuple[
        list[Person],
        list[FilmWork],
        list[Genre],
        list[GenreFilmWork],
        list[PersonFilmWork],
    ]:
        persons = self._extract_persons()
        film_works = self._extract_film_works()
        genres = self._extract_genres()
        genre_film_works = self._extract_genre_film_works()
        person_film_works = self._extract_person_film_works()
        return persons, film_works, genres, genre_film_works, person_film_works

    def _extract_persons(self) -> list[Person]:
        persons = []
        statement = 'SELECT id, full_name FROM person'

        result = self._connection.execute(statement)
        for row in result.fetchall():
            persons.append(Person(*row))

        return persons

    def _extract_film_works(self) -> list[FilmWork]:
        film_works = []
        statement = (
            'SELECT id, title, description, rating, type FROM film_work'
        )

        result = self._connection.execute(statement)
        for row in result.fetchall():
            film_works.append(FilmWork(*row))

        return film_works

    def _extract_genres(self) -> list[Genre]:
        genres = []
        statement = 'SELECT id, name FROM genre'

        result = self._connection.execute(statement)
        for row in result.fetchall():
            genres.append(Genre(*row))

        return genres

    def _extract_genre_film_works(self) -> list[GenreFilmWork]:
        genre_film_works = []
        statement = 'SELECT id, film_work_id, genre_id FROM genre_film_work'

        result = self._connection.execute(statement)
        for row in result.fetchall():
            genre_film_works.append(GenreFilmWork(*row))

        return genre_film_works

    def _extract_person_film_works(self) -> list[PersonFilmWork]:
        person_film_works = []
        statement = (
            'SELECT id, film_work_id, person_id, role FROM person_film_work'
        )

        result = self._connection.execute(statement)
        for row in result.fetchall():
            person_film_works.append(PersonFilmWork(*row))

        return person_film_works
