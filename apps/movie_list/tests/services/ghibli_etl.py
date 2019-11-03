from unittest.mock import patch
from expects import *
import pytest

from apps.movie_list.models.character import Character
from apps.movie_list.models.etl_log import delay_since_last_run
from apps.movie_list.models.movie import Movie
from apps.movie_list.services import ghibli_etl


def describe_run():

    characters_data = [
        {
            'id': 'c1',
            'name': 'Character 1',
            'films': [
                'https://ghibliapi.herokuapp.com/films/m1'
            ]
        },
        {
            'id': 'c2',
            'name': 'Character 2',
            'films': [
                'https://ghibliapi.herokuapp.com/films/m1'
            ]
        },
    ]

    films_data = [
        {
            'id': 'm1',
            'title': 'Movie 1',
        },
        {
            'id': 'm2',
            'title': 'Movie 2',
        }
    ]

    @pytest.mark.django_db
    @patch(
        'apps.movie_list.services.ghibli_etl.get_films',
        return_value=films_data
    )
    @patch(
        'apps.movie_list.services.ghibli_etl.get_people',
        return_value=characters_data
    )
    def it_fetches_and_saves_movies_and_characters(
            mock_get_people,
            mock_get_films
    ):
        expect(Movie.objects.count()).to(equal(0))
        expect(Character.objects.count()).to(equal(0))
        expect(delay_since_last_run(ghibli_etl.NAME)).to(be_none)

        ghibli_etl.run()

        expect(Movie.objects.count()).to(equal(2))
        expect(Character.objects.count()).to(equal(2))
        expect(
            Movie.objects.get(title='Movie 1').characters.count()
        ).to(equal(2))
        expect({
            character.name
            for character in
            Movie.objects.get(title='Movie 1').characters.all()
        }).to(equal({'Character 1', 'Character 2'}))
        expect(
            Movie.objects.get(title='Movie 2').characters.count()
        ).to(equal(0))
        expect(delay_since_last_run(ghibli_etl.NAME)).to_not(be_none)


    # TODO Test handling API errors
