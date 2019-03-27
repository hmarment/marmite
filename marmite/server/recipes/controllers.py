# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

from flask import Blueprint, jsonify

from marmite.server import app, db
from marmite.server.recipes.ext import guardian
from marmite.server.recipes.ext.guardian.models import RecipeGuardian, RecipeGuardianSchema
from marmite.server.recipes.models import Recipe, RecipeSchema


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

    recipes = guardian.service.list_recipes()
    app.logger.info("Writing {} recipes to DB".format(len(recipes)))
    for recipe in recipes:
        if not guardian.service.exists(recipe):
            db.session.add(recipe)

    db.session.commit()

    return ("", 204)


@recipe.route("/api/ext/guardian/sync/<int:recipe_count>")
def sync_n_guardian_recipes(recipe_count):
    """
    Fetch a defined number of recipes from the Guardian API and
    persist to DB.
    """

    most_recent_recipe = guardian.service.most_recent_recipe()

    recipes = guardian.service.list_recipes(max_recipes=recipe_count, from_date=most_recent_recipe)
    app.logger.info("Writing {} recipes to DB".format(len(recipes)))
    for recipe in recipes:
        if not guardian.service.exists(recipe):
            db.session.add(recipe)

    db.session.commit()

    return ("", 204)


@recipe.route("/api/ext/guardian/list")
def list_recipes():

    recipes = RecipeGuardian.query.order_by(RecipeGuardian.web_publication_date.desc()).all()

    # Serialize the data for the response
    recipe_schema = RecipeGuardianSchema(many=True)
    return jsonify(recipe_schema.dump(recipes).data)
