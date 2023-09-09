from django.contrib import admin
from django.conf import settings

from .models import Genre, FilmWork, GenreFilmWork


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    extra = 2
    verbose_name = 'Жанр'
    verbose_name_plural = 'Жанры'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'total_movies')
    search_fields = ('name',)
    list_filter = ('modified',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY

    def total_movies(self, obj: Genre) -> int:
        return obj.film_works.count()

    total_movies.short_description = 'Количество фильмов в жанре'


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'description', 'creation_date', 'rating')
    search_fields = ('title', 'type')
    list_filter = ('creation_date', 'rating')
    empty_value_display = settings.EMPTY_VALUE_DISPLAY
    inlines = (GenreFilmWorkInline,)
