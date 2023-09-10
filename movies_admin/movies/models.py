from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from config.mixins import TimeStampedMixin, UUIDMixin


class Genre(UUIDMixin, TimeStampedMixin):
    class Meta:
        db_table = '"content"."genre"'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name


class FilmWork(UUIDMixin, TimeStampedMixin):
    class Meta:
        db_table = '"content"."film_work"'
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    title = models.CharField(_('title'), max_length=255)
    type = models.CharField(_('type'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'))
    rating = models.FloatField(
        verbose_name=_('rating'),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    genres = models.ManyToManyField(
        to=Genre,
        through='GenreFilmWork',
        related_name='film_works',
        verbose_name=_('genres'),
    )

    def __str__(self):
        return f'{self.title}'


class GenreFilmWork(UUIDMixin):
    class Meta:
        db_table = '"content"."genre_film_work"'

    created = models.DateTimeField(_('created'), auto_now_add=True)
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.film_work} - {self.genre}'
