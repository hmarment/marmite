from django.urls import path

from . import views

urlpatterns = [
    path('', views.recipes_view, name='recipes_view'),
    path('<int:recipe_id>', views.recipe_detail_view, name='recipe_detail_view')
    # path('guardian/sync/<int:recipe_count>', views.sync_n_guardian_recipes, name='sync_n_guardian_recipes')
]
