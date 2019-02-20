import click

from flask.cli import AppGroup
from marmite.server import db

admin = AppGroup('admin')


@admin.command('create-db')
# @click.argument()
def create_db():
    # Create the database
    db.create_all()


@admin.command('flush-db')
# @click.argument()
def flush_db():
    db.drop_all()
