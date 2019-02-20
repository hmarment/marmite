# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

from flask import Blueprint, jsonify

from marmite.server import app, db
from marmite.server.ext import guardian
from marmite.server.recipes.models import Recipe, RecipeSchema

recipe = Blueprint('recipe', __name__,
                   static_folder="../../client/dist/static",
                   template_folder="../../client/dist")


@recipe.route('/')
def show():
    return 'Hello, World!'


@recipe.route('/api/ext/guardian/sync')
def sync_guardian_recipes():

    recipes = guardian.content.list_recipes()
    app.logger.debug(recipes)
    app.logger.info('Writing {} recipes to DB'.format(len(recipes)))
    for recipe in recipes:
        r = Recipe(external_id=recipe.id,
                   name=recipe.headline,
                   source='guardian.co.uk',
                   url=recipe.shortUrl,
                   body=recipe.bodyText,
                   image=recipe.main,
                   thumbnail=recipe.thumbnail,
                   created_at=recipe.webPublicationDate,
                   last_modified_at=recipe.lastModified)
        db.session.add(r)

    db.session.commit()

    return ('', 204)


@recipe.route('/api/ext/guardian/list')
def list_recipes():

    recipes = Recipe.query \
        .order_by(Recipe.created_at.desc()) \
        .all()

    # Serialize the data for the response
    recipe_schema = RecipeSchema(many=True)
    return jsonify(recipe_schema.dump(recipes).data)
