import logging

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Ingredient, Recipe, Unit, RecipeIngredient
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    RecipeDetailSerializer,
    RecipeIngredientSerializer,
    UnitSerializer,
)

logFormatter = "%(asctime)s - %(levelname)s - %(module)s:%(funcName)s " "- %(message)s"
logging.basicConfig(format=logFormatter, level=logging.WARNING)
logger = logging.getLogger(__name__)


@api_view(["GET", "POST"])
def recipes_view(request):
    if request.method == "GET":
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            recipe = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def recipe_detail_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == "GET":
        serializer = RecipeDetailSerializer(recipe)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = RecipeDetailSerializer(recipe, data=request.data, partial=True)
        if serializer.is_valid():
            recipe = serializer.save()
            return Response(RecipeDetailSerializer(recipe).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        recipe.delete()
        return Response("Recipe deleted", status=status.HTTP_204_NO_CONTENT)
