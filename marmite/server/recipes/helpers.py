from __future__ import with_statement, print_function, absolute_import

from sqlalchemy import func

from marmite.server import db

from .models import Recipe


def most_recent_recipe(source='guardian.co.uk'):
    """Return the most recent recipe for a given source"""
    return db.session.query(func.max(Recipe.created_at)).filter(Recipe.source == source).one()[0]


def exists(recipe, source='guardian.co.uk'):
    """
    Return True if recipe already in database.

    :param organization: Organization object (ads_attribution.server.organizations.models.Organization)
    """

    return db.session.query(
        db.exists().where(Recipe.external_id == recipe.external_id and Recipe.source == source)
    ).scalar()
