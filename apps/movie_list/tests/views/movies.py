from unittest.mock import patch, Mock
from expects import *
import pytest

from django.test.client import Client
from django.urls import reverse

from apps.movie_list.models.character import Character
from apps.movie_list.models.movie import Movie
from apps.movie_list.services import ghibli_etl


def describe_get_movies():

    @pytest.mark.django_db
    @patch(
        'apps.movie_list.views.movies.delay_since_last_run',
        return_value=Mock(seconds=0),
    )
    def it_displays_the_movie_index(
        mock_delay_since_last_run,
        movie_attrs,
        character_attrs,
    ):
        client = Client()

        # TODO Use mocks instead of hitting the database:
        character = Character.objects.create(**character_attrs)
        movie = Movie.objects.create(**movie_attrs)
        movie.characters.set([character])

        response = client.get(reverse('movie_index'))
        expect(response.status_code).to(equal(200))
        content = response.content.decode('utf-8')
        expect(content).to(contain(
            'Movie list',
            'Movie 1',
            'Character 1'
        ))

    @pytest.mark.django_db
    @patch(
        'apps.movie_list.views.movies.delay_since_last_run',
        return_value=None,
    )
    def it_runs_etl_if_never_run(mock_delay_since_last_run):
        client = Client()
        with patch.object(ghibli_etl, 'run') as mock_method:
            response = client.get(reverse('movie_index'))
        expect(mock_method.call_count).to(equal(1))
