import pytest


@pytest.fixture
def character_attrs():
    return {
        'external_id': 'c1',
        'name': 'Character 1',
    }

@pytest.fixture
def movie_attrs():
    return {
        'external_id': 'm1',
        'title': 'Movie 1',
    }
