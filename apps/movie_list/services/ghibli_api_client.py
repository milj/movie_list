import re
import requests


BASE_URL = r'https://ghibliapi.herokuapp.com'

def _get(endpoint):
    url = f'{BASE_URL}{endpoint}'
    return requests.get(url).json()

def get_films():
    '''Fetch films'''
    return _get('/films')

def get_people():
    '''Fetch people'''
    return _get('/people')

def film_id(film_url):
    '''Utility function to extract the film id from the film URL'''
    regex = r'^' + BASE_URL + r'/films/(?P<id>.+)$'
    match = re.search(regex, film_url)
    return match.group('id') if match else None
