import click
from .app import app, db
from .models import *

@app.cli.command()
def syncdb():
    db.create_all()
