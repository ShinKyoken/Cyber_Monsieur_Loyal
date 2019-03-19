from appli.app import db, login_manager

class REGLE(db.Model):
    idT     = db.Column(db.Integer, db.ForeignKey("TOURNOI.idT"), primary_key = True)
    nomFic  = db.Column(db.String(100))
    data    = db.Column(db.LargeBinary(length = 2**24-1))
