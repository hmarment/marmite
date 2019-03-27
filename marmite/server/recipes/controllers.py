# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

from flask import Blueprint, jsonify

from marmite.server import app, db
from marmite.server.ext import guardian
from marmite.server.recipes.models import Recipe, RecipeSchema

from . import helpers

recipe = Blueprint(
    "recipe",
    __name__,
    static_folder="../../client/dist/static",
    template_folder="../../client/dist",
)


@recipe.route("/")
def show():
    return "Hello, World!"


@recipe.route("/api/ext/guardian/sync")
def sync_guardian_recipes():
    """
    Fetch all recipes from Guardian API.
    """

    recipes = guardian.content.list_recipes()
    app.logger.info("Writing {} recipes to DB".format(len(recipes)))
    for recipe in recipes:
        r = Recipe(
            external_id=recipe.id,
            name=recipe.headline,
            source="guardian.co.uk",
            url=recipe.shortUrl,
            body=recipe.bodyText,
            image=recipe.main,
            thumbnail=recipe.thumbnail,
            created_at=recipe.webPublicationDate,
            last_modified_at=recipe.lastModified,
        )
        db.session.add(r)

    db.session.commit()

    return ("", 204)


@recipe.route("/api/ext/guardian/sync/<int:recipe_count>")
def sync_n_guardian_recipes(recipe_count):
    """
    Fetch a defined number of recipes from the Guardian API and
    persist to DB.
    """

    most_recent_recipe = helpers.most_recent_recipe(source='guardian.co.uk')

    recipes = guardian.content.list_recipes(max_recipes=recipe_count, from_date=most_recent_recipe)
    app.logger.info("Writing {} recipes to DB".format(len(recipes)))
    for recipe in recipes:
        r = Recipe(
            external_id=recipe.id,
            name=recipe.headline,
            source="guardian.co.uk",
            url=recipe.shortUrl,
            body=recipe.bodyText,
            image=recipe.main,
            thumbnail=recipe.thumbnail,
            created_at=recipe.webPublicationDate,
            last_modified_at=recipe.lastModified,
        )

        if not helpers.exists(r, source='guardian.co.uk'):
            db.session.add(r)

    db.session.commit()

    return ("", 204)


@recipe.route("/api/ext/guardian/list")
def list_recipes():

    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()

    # Serialize the data for the response
    recipe_schema = RecipeSchema(many=True)
    return jsonify(recipe_schema.dump(recipes).data)
