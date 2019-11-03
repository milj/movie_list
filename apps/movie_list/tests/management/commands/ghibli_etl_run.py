from unittest.mock import patch
from expects import *

from django.core.management import call_command

from apps.movie_list.services import ghibli_etl


def describe_ghibli_etl_run():

    def it_runs_ghibli_etl():
        with patch.object(ghibli_etl, 'run') as mock_method:
            call_command('ghibli_etl_run')

        expect(mock_method.call_count).to(equal(1))
