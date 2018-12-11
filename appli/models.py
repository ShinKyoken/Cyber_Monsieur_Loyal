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
    intituleT        = db.Column(db.String(50))
    descT            = db.Column(db.String(100))
    typeT            = db.Column(db.String(30))
    etatT            = db.Column(db.Integer)
    nbEquipe         = db.Column(db.Integer)
    nbParticipantsMax = db.Column(db.Integer)
    disciplineT      = db.Column(db.String(30))
    lieuT            = db.Column(db.String(30))
    logoT            = db.Column(db.Text)

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
    idT           = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"),primary_key = True)

class PHOTO(db.Model):
    idPhoto   = db.Column(db.Integer, primary_key = True)
    idT       = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"),primary_key = True)
    Photo     = db.Column(db.Text)
    descPhoto = db.Column(db.String(100))
    datePhoto = db.Column(db.Date)

class CONSTITUER(db.Model):
    idP = db.Column(db.Integer, db.ForeignKey("PARTICIPANT.idP"),primary_key=True)
    idE = db.Column(db.Integer, db.ForeignKey("EQUIPE.idE"), primary_key=True)

class PARTIE(db.Model):
    idPartie   = db.Column(db.Integer, primary_key=True)
    carteParie = db.Column(db.String(100))

class PARTICIPERPARTIE(db.Model):
    idE      = db.Column(db.Integer, db.ForeignKey("EQUIPE.idE"),primary_key=True)
    idPartie = db.Column(db.Integer, db.ForeignKey("PARTIE.idPartie"),primary_key=True)
    idT      = db.Column(db.Integer, db.ForeignKey("TOURNOI.idT"),primary_key=True)

def get_All_Admins():
    return ADMIN.query.all()

def get_All_Tournois_Actifs():
    return TOURNOI.query.filter_by(etatT = 1)

def get_All_Tournois_Terminees():
    return TOURNOI.query.filter_by(etatT = 2)

def get_All_Tournois_Admin():
    return TOURNOI.query.filter_by(idAdmin = 1)

def get_Tournoi_by_id(id):
    return TOURNOI.query.filter_by(idT = idT)

def count_tournoi():
    return TOURNOI.query.count()

def insert_tournoi(tournoi):
    newTournoi = TOURNOI(idAdmin = 1, regleT = tournoi['regleT'], dateT = tournoi['dateT'],
    dureeT = tournoi['dureeT'], intituleT = tournoi['intituleT'], descT = tournoi['descT'],
    typeT = tournoi['typeT'],etatT = tournoi['etatT'], nbEquipe = tournoi['nbEquipe'],
    nbParticipantsMax = tournoi['nbParticipantsMax'],disciplineT = tournoi['disciplineT'],
    lieuT = tournoi['lieuT'], logoT = tournoi['logoT'])
    db.session.add(newTournoi)
    db.session.commit()
