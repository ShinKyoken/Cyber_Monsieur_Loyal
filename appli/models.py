from .app import db

class Admin(db.Model):
    idAdmin     = db.Column(db.Integer, primary_key = True)
    nomAdmin    = db.Column(db.String(100))
    prenomAdmin = db.Column(db.String(100))
    mdpAdmin    = db.Column(db.String(100))
    mailAdmin   = db.Column(db.String(100))

class Book(db.Model):
    id        = db.Column(db.Integer, primary_key = True)
    price     = db.Column(db.Float)
    title     = db.Column(db.String(100))
    url       = db.Column(db.String(200))
    img       = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref = db.backref("books", lazy = "dynamic"))

def get_sample():
    return Book.query.limit(10).all()

def get_all():
    return Book.query.all()

def get_author(id):
    return Author.query.get(id)
