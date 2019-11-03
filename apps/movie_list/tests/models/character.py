from expects import *
import pytest

from apps.movie_list.models.character import Character
from apps.movie_list.tests.change import change


def describe_create():

    def with_valid_attributes():

        @pytest.mark.django_db
        def it_creates_the_character(character_attrs):
            expect(
                lambda: Character.objects.create(**character_attrs)
            ).to(change(Character.objects.all().count, 1))

        @pytest.mark.django_db
        def it_sets_character_name(character_attrs):
            Character.objects.create(**character_attrs)
            expect(Character.objects.first().name). \
                to(equal(character_attrs['name']))
