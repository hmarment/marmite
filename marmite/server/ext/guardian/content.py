import requests
import datetime

from urllib.parse import urlparse

from marmite.server import app
from marmite.server.ext import throttle
from marmite.server.ext.guardian import BASE_URL, Endpoints
from marmite.server.ext.guardian.models import GuardianRecipe

API_KEY = app.config.get("GUARDIAN_API_KEY")


@throttle
def get_json(url, http_method="GET"):

    with requests.Session() as session:
        with session.request(http_method, url) as response:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                app.logger.error(
                    "{} - {} - {} {}".format(
                        response.status_code, response.reason, http_method, url
                    )
                )
            else:
                return response.json()


def deserialize(recipe_json):
    """Deserialize Guardian API json response to a Recipe object."""

    id_ = recipe_json.get("id")
    pillar_id = recipe_json.get("fields", {}).get("pillaId")
    section_id = recipe_json.get("sectionId")
    publication_date = datetime.datetime.strptime(
        recipe_json.get("webPublicationDate"), "%Y-%m-%dT%H:%M:%SZ"
    )
    headline = recipe_json.get("fields", {}).get("headline")
    short_url = recipe_json.get("fields", {}).get("headline")
    last_modified = datetime.datetime.strptime(
        recipe_json.get("fields", {}).get("lastModified"), "%Y-%m-%dT%H:%M:%SZ"
    )
    main = recipe_json.get("fields", {}).get("main")
    thumbnail = recipe_json.get("fields", {}).get("thumbnail")
    body_text = recipe_json.get("fields", {}).get("bodyText")
    tags = recipe_json.get("tags")

    return GuardianRecipe(
        id_,
        pillar_id,
        section_id,
        publication_date,
        headline,
        short_url,
        last_modified,
        main,
        thumbnail,
        body_text,
        tags,
    )


def get_recipe(recipe_id):
    """Fetch recipe from Guardian API by recipe ID."""
    url = urlparse(
        BASE_URL
        + Endpoints.GetRecipe.value.format(API_KEY=API_KEY, RECIPE_ID=recipe_id)
    ).geturl()

    response = get_json(url)

    return deserialize(response.get("response", {}).get("content"))


def get_page(page_number, page_size=50, order_by='oldest', from_date=None):
    """Fetch a page of recipes from Guardian content API."""
    
    url_str = BASE_URL + Endpoints.ListRecipes.value.format(
        API_KEY=API_KEY, page=page_number, page_size=page_size, order_by=order_by)

    if from_date:
        url_str += '&from-date={}'.format(from_date.strftime('%Y-%m-%d'))
    url = urlparse(url_str).geturl()

    return get_json(url)


def list_recipes(max_recipes=None, from_date=None):
    """
    Get recipes from Guardian API. Iterates through
    pages.
    """
    results = list()
    page_number = 1

    app.logger.debug("Fetching first page of recipes")
    first_page = get_page(page_number, from_date=from_date)
    last_page_number = first_page.get("response", {}).get("pages")

    results += first_page.get("response", {}).get("results", [])

    for page in range(page_number + 1, last_page_number):

        if max_recipes and len(results) >= max_recipes:
            continue

        app.logger.debug("Fetching page {} / {}".format(page, last_page_number))
        next_page = get_page(page, from_date=from_date)
        results += next_page.get("response", {}).get("results", [])

    recipes = list()
    for result in results:
        recipe = get_recipe(result.get("id"))
        recipes.append(recipe)
    return recipes


def _recipe_publication_dates(recipe_jsons):

    return [recipe_json.get("webPublicationDate") for recipe_json in recipe_jsons]


def _any_new_recipes(last_published_date, recipe_jsons):

    recipe_dates = _recipe_publication_dates(recipe_jsons)

    return any(
        [publication_date > last_published_date for publication_date in recipe_dates]
    )


def list_new_recipes(last_published_date):
    """
    Fetch only new recipes. Requires the published date of most recent
    recipe as input for reference.

    :param last_published_date: datetime of most recent recipe.
    """

    results = list()
    page_number = 1

    app.logger.debug("Fetching first page of recipes")
    first_page = get_page(page_number)
    page_results = first_page.get("response", {}).get("results", [])

    while _any_new_recipes(last_published_date, page_results):
        results += page_results
        page_number += 1
        next_page = get_page(page_number)
        page_results = next_page.get("response", {}).get("results", [])

    recipes = list()
    for result in results:
        recipe = get_recipe(result.get("id"))
        recipes.append(recipe)
    return recipes
