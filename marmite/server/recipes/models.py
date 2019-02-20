# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

from datetime import datetime
from sqlalchemy import func
from marmite.server import db, ma


class Recipe(db.Model):
    __tablename__ = "recipe"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=255))
    source = db.Column(db.String(length=255))
    url = db.Column(db.VARCHAR)
    body = db.Column(db.VARCHAR)
    image = db.Column(db.VARCHAR)
    thumbnail = db.Column(db.VARCHAR)
    created_at = db.Column(db.DateTime, default=func.now())
    last_modified_at = db.Column(db.DateTime,
                                 onupdate=func.utc_timestamp())


class RecipeSchema(ma.ModelSchema):
    class Meta:
        model = Recipe
        sqla_session = db.session
