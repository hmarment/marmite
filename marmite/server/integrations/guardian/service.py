import requests
import datetime
import logging
import pytz

from urllib.parse import urlparse

from integrations.utils import throttle
from . import BASE_URL, Endpoints
from .apps import GuardianConfig
from .models import RecipeGuardian

API_KEY = GuardianConfig.API_KEY

logFormatter = "%(asctime)s - %(levelname)s - %(module)s:%(funcName)s " "- %(message)s"
logging.basicConfig(format=logFormatter, level=logging.WARNING)
logger = logging.getLogger(__name__)


@throttle
def get_json(url, http_method="GET"):

    with requests.Session() as session:
        with session.request(http_method, url) as response:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                logger.error(
                    "{} - {} - {} {}".format(
                        response.status_code, response.reason, http_method, url
                    )
                )
            else:
                return response.json()


def deserialize(recipe_json):
    """Deserialize Guardian API json response to a Recipe object."""

    id_ = recipe_json.get("id")
    pillar_id = recipe_json.get("pillarId")
    pillar_name = recipe_json.get("pillarName")
    section_id = recipe_json.get("sectionId")
    section_name = recipe_json.get("sectionName")
    web_publication_date = pytz.utc.localize(
        datetime.datetime.strptime(
            recipe_json.get("webPublicationDate"), "%Y-%m-%dT%H:%M:%SZ"
        )
    )
    web_title = recipe_json.get("webTitle")
    web_url = recipe_json.get("webUrl")
    api_url = recipe_json.get("apiUrl")
    trail_text = recipe_json.get("fields", {}).get("trailText")
    headline = recipe_json.get("fields", {}).get("headline")
    standfirst = recipe_json.get("fields", {}).get("standfirst")
    byline = recipe_json.get("fields", {}).get("byline")
    short_url = recipe_json.get("fields", {}).get("shortUrl")
    production_office = recipe_json.get("fields", {}).get("productionOffice")
    publication = recipe_json.get("fields", {}).get("publication")
    lang = recipe_json.get("fields", {}).get("lang")
    last_modified = pytz.utc.localize(
        datetime.datetime.strptime(
            recipe_json.get("fields", {}).get("lastModified"), "%Y-%m-%dT%H:%M:%SZ"
        )
    )
    main = recipe_json.get("fields", {}).get("main")
    thumbnail = recipe_json.get("fields", {}).get("thumbnail")
    body = recipe_json.get("fields", {}).get("body")
    body_text = recipe_json.get("fields", {}).get("bodyText")
    word_count = recipe_json.get("fields", {}).get("wordcount")
    star_rating = recipe_json.get("fields", {}).get("starRating")
    tags = recipe_json.get("tags")

    return RecipeGuardian(
        id=id_,
        section_id=section_id,
        section_name=section_name,
        web_publication_date=web_publication_date,
        web_title=web_title,
        web_url=web_url,
        api_url=api_url,
        trail_text=trail_text,
        headline=headline,
        standfirst=standfirst,
        body=body,
        main=main,
        production_office=production_office,
        publication=publication,
        lang=lang,
        body_text=body_text,
        last_modified=last_modified,
        short_url=short_url,
        thumbnail=thumbnail,
        wordcount=int(word_count) if word_count else None,
        byline=byline,
        star_rating=int(star_rating) if star_rating else None,
        tags=tags,
        pillar_name=pillar_name,
        pillar_id=pillar_id,
    )


def get_recipe(recipe_id):
    """Fetch recipe from Guardian API by recipe ID."""
    url = urlparse(
        BASE_URL
        + Endpoints.GetRecipe.value.format(API_KEY=API_KEY, RECIPE_ID=recipe_id)
    ).geturl()

    response = get_json(url)

    return deserialize(response.get("response", {}).get("content"))


def get_page(page_number, page_size=50, order_by="oldest", from_date=None):
    """Fetch a page of recipes from Guardian content API."""

    url_str = BASE_URL + Endpoints.ListRecipes.value.format(
        API_KEY=API_KEY, page=page_number, page_size=page_size, order_by=order_by
    )

    if from_date:
        url_str += "&from-date={}".format(from_date.strftime("%Y-%m-%d"))
    url = urlparse(url_str).geturl()

    return get_json(url)


def list_recipes(max_recipes=None, from_date=None):
    """
    Get recipes from Guardian API. Iterates through
    pages.
    """
    results = list()
    page_number = 1

    logger.debug("Fetching first page of recipes")
    first_page = get_page(page_number, from_date=from_date)
    last_page_number = first_page.get("response", {}).get("pages")

    results += first_page.get("response", {}).get("results", [])

    for page in range(page_number + 1, last_page_number):

        if max_recipes and len(results) >= max_recipes:
            continue

        logger.debug("Fetching page {} / {}".format(page, last_page_number))
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

    logger.debug("Fetching first page of recipes")
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


def most_recent_recipe():
    """Return the most recent recipe for a given source"""
    most_recent = RecipeGuardian.objects.latest(
        "web_publication_date"
    ).web_publication_date
    print(most_recent)
    return RecipeGuardian.objects.filter(web_publication_date=most_recent).first()


def exists(recipe):
    """
    Return True if Guardian recipe already in database.

    :param recipe: RecipeGuardian object
    """
    return RecipeGuardian.objects.filter(id=recipe.id).exists()
