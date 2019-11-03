import datetime
from expects import *
from freezegun import freeze_time
import pytest

from django.utils import timezone

from apps.movie_list.models.etl_log import (
    delay_since_last_run, mark_as_run, EtlLog
)
from apps.movie_list.tests.change import change


@pytest.fixture
def etl_name():
    return 'Test ETL'

@pytest.fixture
def past():
    return timezone.now() - timezone.timedelta(days=1)


def describe_mark_as_run():

    @pytest.mark.django_db
    def it_creates_the_etl_log_if_not_exists(etl_name):
        expect(
            lambda: mark_as_run(etl_name)
        ).to(change(EtlLog.objects.all().count, 1))

    @pytest.mark.django_db
    def it_updates_timestamp_if_etl_log_exists(etl_name, past):
        with freeze_time(past):
            mark_as_run(etl_name)
        expect(EtlLog.objects.get().last_run_at).to(equal(past))
        expect(
            lambda: mark_as_run(etl_name)
        ).to_not(change(EtlLog.objects.all().count))
        expect(EtlLog.objects.get().last_run_at).to(be_above(past))


def describe_delay_since_last_run():

    @pytest.mark.django_db
    def it_returns_none_if_the_etl_log_not_exists(etl_name):
        expect(delay_since_last_run(etl_name)).to(equal(None))

    @pytest.mark.django_db
    def it_returns_delay_since_last_run_if_the_etl_log_exists(etl_name, past):
        with freeze_time(past):
            mark_as_run(etl_name)
        with freeze_time(past + timezone.timedelta(days=1)):
            expect(delay_since_last_run(etl_name)). \
                to(equal(datetime.timedelta(days=1)))


# Not testing EtlLog.objects.create since it is not meant to be directly used
