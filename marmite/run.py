# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

from server import app

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG'))
