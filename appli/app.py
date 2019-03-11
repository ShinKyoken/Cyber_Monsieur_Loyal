from flask import Flask
from flask_login import LoginManager
app = Flask(__name__)
login_manager=LoginManager()
login_manager.init_app(app)
from flask_bootstrap import Bootstrap
Bootstrap(app)
from flask_uikit import UIkit
UIkit(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

from flask_sqlalchemy import *
import pymysql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+pymysql://pandion:pandion@servinfo-mariadb/DBpandion')
db=SQLAlchemy(app)
app.config['SECRET_KEY'] = "3ec22ed8-06fd-455e-8132-94b9fc65ba51"
