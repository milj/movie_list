from django.core.management.base import BaseCommand

from apps.movie_list.services import ghibli_etl


class Command(BaseCommand):
    help = 'Runs the Ghibli movie list ETL'

    def handle(self, *args, **options):
        ghibli_etl.run()
