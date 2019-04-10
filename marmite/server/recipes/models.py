from django.db import models
from django.contrib.postgres.fields import JSONField
from rest_framework import serializers


class Ingredient(models.Model):

    class Meta:
        db_table = 'ingredients'

    name = models.CharField(max_length=1000)
    plural_name = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)
    tags = JSONField(blank=True, null=True)
    allergies = JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'plural_name', 'type', 'tags', 'allergies', 'created_at', 'last_updated_at')


class Recipe(models.Model):

    class Meta:
        db_table = 'recipes'

    name = models.CharField(max_length=1000)
    short_description = models.TextField(blank=True)
    type = models.CharField(max_length=1000)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    source = models.CharField(max_length=1000)
    preparation_time = models.PositiveIntegerField()  # in seconds
    cooking_time = models.PositiveIntegerField()  # in seconds
    instructions = models.TextField()
    image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    # owner = models.IntegerField(fore)


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'short_description', 'type', 'source', 'preparation_time', 'cooking_time', 'instructions', 'image', 'created_at', 'last_updated_at')


class Unit(models.Model):

    class Meta:
        db_table = 'units'

    name = models.CharField(max_length=1000)
    plural_name = models.CharField(max_length=1000)
    symbol = models.CharField(max_length=5)
    unit_system = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)


class UnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'name', 'plural_name', 'symbol', 'unit_system', 'created', 'last_updated_at')


class RecipeIngredient(models.Model):

    class Meta:
        db_table = 'recipe_ingredients'

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)


class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'recipe', 'ingredient', 'quantity', 'unit', 'created', 'last_updated_at')
