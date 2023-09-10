import uuid
import datetime as dt
from dataclasses import dataclass
from typing import TypeVar, Type


@dataclass(frozen=True)
class FilmWork:
    updated_at: dt.datetime
    created_at: dt.datetime
    id: uuid.UUID
    title: str
    type: str
    description: str
    creation_date: dt.datetime
    rating: float


@dataclass(frozen=True)
class Person:
    updated_at: dt.datetime
    created_at: dt.datetime
    id: uuid.UUID
    full_name: str


@dataclass(frozen=True)
class Genre:
    updated_at: dt.datetime
    created_at: dt.datetime
    id: uuid.UUID
    name: str


@dataclass(frozen=True)
class GenreFilmWork:
    id: uuid.UUID
    created_at: dt.datetime
    film_work_id: uuid.UUID
    genre_id: uuid.UUID


@dataclass(frozen=True)
class PersonFilmWork:
    id: uuid.UUID
    created_at: dt.datetime
    role: str
    film_work_id: uuid.UUID
    person_id: uuid.UUID


Model = TypeVar(
    'Model',
    Type[FilmWork],
    Type[Genre],
    Type[GenreFilmWork],
    Type[Person],
    Type[PersonFilmWork],
)
