from appli.app import db, login_manager
import datetime

class PARTIE(db.Model):
    idPartie      = db.Column(db.Integer, primary_key = True, autoincrement = True)
    idT           = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"), primary_key = True, autoincrement = False )
    cartePartie   = db.Column(db.String(100))
    datePartie    = db.Column(db.DateTime, default=datetime.datetime.now())
    etatPartie    = db.Column(db.Integer, default=0)
