import requests
import logging
import datetime

from urllib.parse import urlparse

from marmite.server import app
from marmite.server.ext.guardian import BASE_URL, Endpoints
from marmite.server.ext.guardian.models import GuardianRecipe

logger = logging.getLogger('marmite.server.ext.guardian.content')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_handler.setFormatter(formatter)
logger.addHandler(c_handler)

API_KEY = app.config.get('GUARDIAN_API_KEY')


def get_json(url, http_method='GET'):

    with requests.Session() as session:
        with session.request(http_method, url) as response:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                logger.error('{} - {} - {} {}'
                                 .format(response.status_code, response.reason,
                                         http_method, url))
            else:
                return response.json()


def deserialize(recipe_json):

    id_ = recipe_json.get('id')
    pillar_id = recipe_json.get('fields', {}).get('pillaId')
    section_id = recipe_json.get('sectionId')
    publication_date = datetime.datetime.strptime(
        recipe_json.get('webPublicationDate'), '%Y-%m-%dT%H:%M:%SZ')
    headline = recipe_json.get('fields', {}).get('headline')
    short_url = recipe_json.get('fields', {}).get('headline')
    last_modified = datetime.datetime.strptime(
        recipe_json.get('fields', {}).get('lastModified'),
        '%Y-%m-%dT%H:%M:%SZ')
    main = recipe_json.get('fields', {}).get('main')
    thumbnail = recipe_json.get('fields', {}).get('thumbnail')
    body_text = recipe_json.get('fields', {}).get('bodyText')
    tags = recipe_json.get('tags')

    return GuardianRecipe(id_, pillar_id, section_id, publication_date,
                          headline, short_url, last_modified, main, thumbnail,
                          body_text, tags)


def get_recipe(recipe_id):

    url = urlparse(BASE_URL + Endpoints.GetRecipe.value
                   .format(API_KEY=API_KEY, RECIPE_ID=recipe_id)).geturl()

    response = get_json(url)

    return deserialize(response.get('response', {}).get('content'))


def list_recipes():

    url = urlparse(BASE_URL + Endpoints.ListRecipes.value
                   .format(API_KEY=API_KEY)).geturl()

    response = get_json(url)

    recipes = list()
    for result in response.get('response', {}).get('results', []):
        recipe = get_recipe(result.get('id'))
        recipes.append(recipe)
    return recipes
