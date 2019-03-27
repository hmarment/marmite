from __future__ import with_statement, print_function, absolute_import

from sqlalchemy import func
from marmite.server import db, ma


class RecipeGuardian(db.Model):
    __tablename__ = "recipes_guardian"

    id = db.Column(db.String(length=1000), primary_key=True)
    section_id = db.Column(db.String(length=255))
    section_name = db.Column(db.String(length=255))
    web_publication_date = db.Column(db.DateTime)
    web_title = db.Column(db.String(length=1000))
    web_url = db.Column(db.String(length=1000))
    api_url = db.Column(db.String(length=1000))
    trail_text = db.Column(db.String(length=1000))
    headline = db.Column(db.String(length=1000))
    standfirst = db.Column(db.String(length=1000))
    body = db.Column(db.VARCHAR)
    main = db.Column(db.String(length=1000))
    production_office = db.Column(db.String(length=255))
    publication = db.Column(db.String(length=255))
    lang = db.Column(db.String(length=255))
    body_text = db.Column(db.VARCHAR)
    last_modified = db.Column(db.DateTime)
    short_url = db.Column(db.String(length=1000))
    thumbnail = db.Column(db.String(length=1000))
    wordcount = db.Column(db.BigInteger)
    byline = db.Column(db.String(length=1000))
    star_rating = db.Column(db.BigInteger)
    tags = db.Column(db.JSON)
    pillar_name = db.Column(db.String(length=255))
    pillar_id = db.Column(db.String(length=255))
    created_at = db.Column(db.DateTime, default=func.now())
    last_updated_at = db.Column(db.DateTime, onupdate=func.utc_timestamp())


class RecipeGuardianSchema(ma.ModelSchema):
    class Meta:
        model = RecipeGuardian
        sqla_session = db.session