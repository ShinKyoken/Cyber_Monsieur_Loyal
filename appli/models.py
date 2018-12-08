from .app import db

class ADMIN(db.Model):
    idAdmin        = db.Column(db.Integer, primary_key = True)
    nomAdmin       = db.Column(db.String(100))
    prenomAdmin    = db.Column(db.String(100))
    dateNaissAdmin = db.Column(db.Date)
    mdpAdmin       = db.Column(db.String(100))

class TOURNOI(db.Model):
    idT              = db.Column(db.Integer, primary_key = True)
    idAdmin          = db.Column(db.Integer, db.ForeignKey("ADMIN.idAdmin"))
    regleT           = db.Column(db.String(100))
    dateT            = db.Column(db.Date)
    dureeT           = db.Column(db.String(5))
    intituleT        = db.Column(db.String(30))
    descT            = db.Column(db.String(30))
    typeT            = db.Column(db.String(30))
    etatT            = db.Column(db.Integer)
    nbEquipe         = db.Column(db.Integer)
    nbParicipantsMax = db.Column(db.Integer)
    disciplineT      = db.Column(db.String(30))
    lieuT            = db.Column(db.String(30))

class PARTICIPANT(db.Model):
    idP     = db.Column(db.Integer, primary_key = True)
    nomP    = db.Column(db.String(100))
    prenomP = db.Column(db.String(100))
    mailP   = db.Column(db.String(100))

class EQUIPE(db.Model):
    idE           = db.Column(db.Integer, primary_key = True)
    etatE         = db.Column(db.Integer)
    nbParticipant = db.Column(db.Integer)
    idChefE       = db.Column(db.Integer, db.ForeignKey("PARTICIPANT.idP"), unique=True)
    nomE          = db.Column(db.String(100))

class PHOTO(db.Model):
    idPhoto   = db.Column(db.Integer, primary_key = True)
    idT       = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"),primary_key = True)
    Photo     = db.Column(db.String(100))
    descPhoto = db.Column(db.String(100))
    datePhoto = db.Column(db.Date)

class CONSTITUER(db.Model):
    idP = db.Column(db.Integer, db.ForeignKey("PARTICIPANT.idP"),primary_key=True)
    idE = db.Column(db.Integer, db.ForeignKey("EQUIPE.idE"), primary_key=True)

class INSCRIRE(db.Model):
    idT = db.Column(db.Integer, db.ForeignKey("TOURNOI.idT"), primary_key=True)
    idE = db.Column(db.Integer, db.ForeignKey("EQUIPE.idE"),primary_key=True)

class PARTIE(db.Model):
    idPartie   = db.Column(db.Integer, primary_key=True)
    carteParie = db.Column(db.String(100))

class PARTICIPERPARTIE(db.Model):
    idE      = db.Column(db.Integer, db.ForeignKey("EQUIPE.idE"),primary_key=True)
    idPartie = db.Column(db.Integer, db.ForeignKey("PARTIE.idPartie"),primary_key=True)
    idT      = db.Column(db.Integer, db.ForeignKey("TOURNOI.idT"),primary_key=True)

def get_All_Admin():
    return ADMIN.query.all()
