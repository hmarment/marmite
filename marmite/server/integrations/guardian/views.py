import logging

from django.http import HttpResponse
from rest_framework import viewsets

from .models import RecipeGuardian, RecipeGuardianSerializer
from . import service

logFormatter = "%(asctime)s - %(levelname)s - %(module)s:%(funcName)s " "- %(message)s"
logging.basicConfig(format=logFormatter, level=logging.WARNING)
logger = logging.getLogger(__name__)


def sync_guardian_recipes(request):
    """
    Fetch all recipes from Guardian API.
    """

    recipes = service.list_recipes()
    logger.info("Writing {} recipes to DB".format(len(recipes)))
    for recipe in recipes:
        if not service.exists(recipe):
            recipe.save()

    return HttpResponse(status=204)


# # @recipe.route("/api/ext/guardian/sync/<int:recipe_count>")
def sync_n_guardian_recipes(request, recipe_count):
    """
    Fetch a defined number of recipes from the Guardian API and
    persist to DB.
    """

    most_recent_recipe = service.most_recent_recipe()

    recipes = service.list_recipes(
        max_recipes=recipe_count, from_date=most_recent_recipe.web_publication_date
    )
    logger.info("Writing {} recipes to DB".format(len(recipes)))
    for recipe in recipes:
        if not service.exists(recipe):
            recipe.save()

    return HttpResponse(status=204)


# @recipe.route("/api/ext/guardian/list")
class ListRecipesViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list recipes.
    """

    queryset = RecipeGuardian.objects.all().order_by("-web_publication_date")
    serializer_class = RecipeGuardianSerializer
