from appli.app import db, login_manager
import datetime

class PHOTO(db.Model):
    idPhoto   = db.Column(db.Integer, primary_key = True, autoincrement=True)
    idT       = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"),primary_key = True, autoincrement=False)
    nomPhoto  = db.Column(db.String(60))
    descPhoto = db.Column(db.String(100))
    datePhoto = db.Column(db.DateTime, default = datetime.datetime.now())
