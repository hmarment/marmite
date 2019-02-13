# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

from flask import Blueprint

recipe = Blueprint('recipe', __name__,
                   static_folder="../../client/dist/static",
                   template_folder="../../client/dist")


@recipe.route('/')
def show():
    return 'Hello, World!'
