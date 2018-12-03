import click
from .app import app, db
from .models import *

@app.cli.command()
def syncdb():
    db.create_all()


@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    db.create_all()

    import yaml
    books = yaml.load(open(filename))

    authors = {}
    for b in books:
        a = b["author"]
        if a not in authors:
            o = Author(name=a)
            db.session.add(o)
            authors[a] = o
    db.session.commit()

    for b in books:
        a = authors[b["author"]]
        o = Book(price = b["price"],
                 title = b["title"],
                 url   = b["url"],
                 img   = b["img"],
                 author_id = a.id)
        db.session.add(o)
    db.session.commit()
