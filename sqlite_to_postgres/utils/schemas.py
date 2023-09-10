import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class FilmWork:
    id: uuid.UUID
    title: str
    description: str
    rating: float
    type: str


@dataclass(frozen=True)
class Person:
    id: uuid.UUID
    full_name: str


@dataclass(frozen=True)
class Genre:
    id: uuid.UUID
    name: str


@dataclass(frozen=True)
class GenreFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID


@dataclass(frozen=True)
class PersonFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
