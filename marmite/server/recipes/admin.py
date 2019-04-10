from django.contrib import admin

from .models import Ingredient, Recipe, Unit, RecipeIngredient

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Unit)
admin.site.register(RecipeIngredient)