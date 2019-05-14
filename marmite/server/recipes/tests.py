# from django.test import TestCase
import pytest

from django.test import Client
from django.urls import reverse

from .models import Recipe


def create_recipe(
    name,
    short_description,
    type_,
    source,
    preparation_time,
    cooking_time,
    instructions,
    image,
):

    return Recipe.objects.create(
        name=name,
        short_description=short_description,
        type=type_,
        source=source,
        preparation_time=preparation_time,
        cooking_time=cooking_time,
        instructions=instructions,
        image=image,
    )


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def setup_test_recipe():

    recipe = create_recipe(
        name="Recipes View - POST - Test Recipe",
        short_description="How, now, brown, cow",
        type_="self",
        source="self",
        preparation_time=30,
        cooking_time=45,
        instructions="Take a can of baked beans, open it and pour into a saucepan.",
        image="http://placekitten.com/g/200/300",
    )

    return recipe


@pytest.mark.django_db
def test_add_recipe(client):

    new_recipe_json = dict(
        name="Recipes View - POST - Test Recipe",
        short_description="How, now, brown, cow",
        type="self",
        source="self",
        preparation_time=30,
        cooking_time=45,
        instructions="Take a can of baked beans, open it and pour into a saucepan.",
        image="http://placekitten.com/g/200/300",
    )
    response = client.post(reverse("recipes_view"), new_recipe_json)

    assert response.status_code == 201

    recipe = response.json()

    assert recipe.get("id") is not None


@pytest.mark.django_db
def test_list_recipes(client, setup_test_recipe):

    recipe = setup_test_recipe
    response = client.get(reverse("recipes_view"))

    assert response.status_code == 200

    recipes = response.json()

    assert len(recipes) == 1
    assert recipes[0].get("id") == recipe.id


@pytest.mark.django_db
def test_get_recipe_by_id(client, setup_test_recipe):

    recipe = setup_test_recipe
    response = client.get(reverse("recipe_detail_view", args=[recipe.id]))

    assert response.status_code == 200

    recipe_json = response.json()

    assert recipe_json.get("id") == recipe.id


@pytest.mark.django_db
def test_update_recipe(client, setup_test_recipe):

    recipe = setup_test_recipe

    recipe_changes = dict(name="Some new name", preparation_time=60)

    response = client.put(
        reverse("recipe_detail_view", args=[recipe.id]),
        recipe_changes,
        content_type="application/json",
    )

    assert response.status_code == 200

    updated_recipe_json = response.json()

    assert updated_recipe_json.get("id") == recipe.id
    assert updated_recipe_json.get("name") == recipe_changes.get("name")
    assert updated_recipe_json.get("preparation_time") == recipe_changes.get(
        "preparation_time"
    )
