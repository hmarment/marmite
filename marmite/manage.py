# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function, absolute_import

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from server import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
