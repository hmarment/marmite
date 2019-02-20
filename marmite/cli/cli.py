# cli.py

from marmite.server import app
from marmite.cli.commands.admin import admin


app.cli.add_command(admin)
