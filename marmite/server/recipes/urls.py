from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'recipes/list', views.ListRecipesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('guardian/sync/<int:recipe_count>', views.sync_n_guardian_recipes, name='sync_n_guardian_recipes')
]
