import logging

from django.db import transaction

from apps.movie_list.models.character import Character
from apps.movie_list.models.etl_log import mark_as_run
from apps.movie_list.models.movie import Movie
from apps.movie_list.services.ghibli_api_client import (
    get_films, get_people, film_id
)


logger = logging.getLogger(__name__)

NAME = 'Ghibli ETL'

def run():
    '''Fetch data from the Ghibli API and save in the database'''
    try:
        # Assuming here that the responses are small;
        # no pagination, results fit in memory
        movies = get_films()
        characters = get_people()
    except Exception as exc:
        logger.error('Error while accessing Ghibli API: %s', exc)
    else:
        with transaction.atomic():
            Movie.objects.all().delete()
            Character.objects.all().delete()

            for movie in movies:
                Movie.objects.create(
                    external_id=movie['id'],
                    title=movie['title'],
                )
            for character in characters:
                instance = Character.objects.create(
                    external_id=character['id'],
                    name=character['name'],
                )
                instance.movies.set([
                    Movie.objects.get(external_id=film_id(film_url))
                    for film_url in character['films']
                ])

            mark_as_run(NAME)
