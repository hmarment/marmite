# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

# Define the WSGI application object
app = Flask(__name__,
            static_folder="../client/dist/static",
            template_folder="../client/dist")

# Load config for current environment (Development / Production)
app.config.from_object(os.environ['CONFIG_PROFILE'])

# enable CORS
CORS(app)

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Marshmallow
ma = Marshmallow(app)

import marmite.server.recipes
from marmite.server.recipes.controllers import recipe

# Flush database first
db.drop_all()

# Create the database
db.create_all()

app.register_blueprint(recipe)
