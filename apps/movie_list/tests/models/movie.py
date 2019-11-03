from expects import *
import pytest

from apps.movie_list.models.movie import Movie
from apps.movie_list.tests.change import change


def describe_create():

    def with_valid_attributes():

        @pytest.mark.django_db
        def it_creates_the_movie(movie_attrs):
            expect(
                lambda: Movie.objects.create(**movie_attrs)
            ).to(change(Movie.objects.all().count, 1))

        @pytest.mark.django_db
        def it_sets_movie_title(movie_attrs):
            Movie.objects.create(**movie_attrs)
            expect(Movie.objects.first().title). \
                to(equal(movie_attrs['title']))
