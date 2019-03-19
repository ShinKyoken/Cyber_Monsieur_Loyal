from appli.app import db, login_manager

class EQUIPE(db.Model):
    idE           = db.Column(db.Integer, primary_key = True, autoincrement=True)
    idT           = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"),primary_key = True, autoincrement=False)
    etatE         = db.Column(db.Integer)
    points        = db.Column(db.Integer, default = 0)
    nbParticipant = db.Column(db.Integer)
    idChefE       = db.Column(db.Integer, db.ForeignKey("PARTICIPANT.idP"))
    nomE          = db.Column(db.String(100))
    machineE      = db.Column(db.String(100))
