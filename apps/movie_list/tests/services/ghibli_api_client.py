from expects import *
import pytest

from apps.movie_list.services.ghibli_api_client import (
    get_films, get_people, film_id
)


def describe_get_films():

    @pytest.mark.vcr()
    def it_fetches_films():
        films = get_films()
        expect(len(films)).to(equal(20))
        expect(films[0]['title']).to(equal('Castle in the Sky'))


def describe_get_people():

    @pytest.mark.vcr()
    def it_fetches_people():
        people = get_people()
        expect(len(people)).to(equal(31))
        expect(people[0]['name']).to(equal('Ashitaka'))


def describe_film_id():

    def it_returns_film_id_for_valid_url():
        url = 'https://ghibliapi.herokuapp.com/films/030555b3-4c92-4fce-93fb-e70c3ae3df8b'
        expect(film_id(url)).to(equal('030555b3-4c92-4fce-93fb-e70c3ae3df8b'))

    def it_returns_none_for_invalid_url():
        url = 'https://foo.com/bar'
        expect(film_id(url)).to(equal(None))
