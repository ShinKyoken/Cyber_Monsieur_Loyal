from .app import db


def get_sample():
    return Book.query.limit(10).all()

def get_all():
    return Book.query.all()

def get_author(id):
    return Author.query.get(id)
