import logging

from django.http import HttpResponse
from rest_framework import viewsets

from .models import Ingredient, Recipe, Unit, RecipeIngredient, IngredientSerializer, RecipeSerializer, UnitSerializer, RecipeIngredientSerializer


logFormatter = "%(asctime)s - %(levelname)s - %(module)s:%(funcName)s " "- %(message)s"
logging.basicConfig(format=logFormatter, level=logging.WARNING)
logger = logging.getLogger(__name__)


class ListRecipesViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list recipes.
    """
    queryset = Recipe.objects.all().order_by('-created_at')
    serializer_class = RecipeSerializer