import logging

from django.views.generic.base import TemplateView

from apps.movie_list.models.etl_log import delay_since_last_run
from apps.movie_list.models.movie import Movie
from apps.movie_list.services import ghibli_etl


logger = logging.getLogger(__name__)

ETL_DELAY_ERROR_THRESHOLD = 90 # in seconds

def etl_check():
    '''This is a simple monitoring mechanism in case the crontab job
    is not running for some reason
    '''
    delay = delay_since_last_run(ghibli_etl.NAME)
    if not delay:
        logger.error('Ghibli ETL did not yet run')
        ghibli_etl.run()
    elif delay.seconds > ETL_DELAY_ERROR_THRESHOLD:
        # Not running the ETL here because the delay may be caused
        # by the broken external API
        logger.error('Ghibli ETL stopped working')


class MovieIndexView(TemplateView):
    template_name = 'movie_list/movies/index.html'

    def get_context_data(self, *args, **kwargs):
        etl_check()
        movies = Movie.objects.prefetch_related('characters').all()
        context = {
            'movies': [
                {
                    'title': movie.title,
                    'characters': [
                        character.name for character in movie.characters.all()
                    ],
                }
                for movie in movies
            ]
        }
        return context
