import datetime
import pytest

# from django.test import TestCase

from .models import RecipeGuardian


@pytest.mark.django_db(transaction=True)
def test_get_recipe():
    # most_recent = service.most_recent_recipe()
    recipe = RecipeGuardian.objects.first()
    assert type(recipe) == RecipeGuardian
