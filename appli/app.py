from flask import Flask
app = Flask(__name__)
from flask_bootstrap import Bootstrap
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

import os.path
def mkpath(p):
        return os.path.normpath(
                os.path.join(
                        os.path.dirname(__file__),
                        p))

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('./books.db'))
db=SQLAlchemy(app)
app.config['SECRET_KEY'] = "3ec22ed8-06fd-455e-8132-94b9fc65ba51"