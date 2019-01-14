from .app import db, login_manager
from flask_login import UserMixin

class ADMIN(db.Model, UserMixin):
    idAdmin        = db.Column(db.Integer, primary_key = True)
    nomAdmin       = db.Column(db.String(100))
    prenomAdmin    = db.Column(db.String(100))
    dateNaissAdmin = db.Column(db.Date)
    mdpAdmin       = db.Column(db.String(100))

class TOURNOI(db.Model):
    idT               = db.Column(db.Integer, primary_key = True)
    idAdmin           = db.Column(db.Integer, db.ForeignKey("ADMIN.idAdmin"))
    regleT            = db.Column(db.String(100))
    dateT             = db.Column(db.Date)
    dureeT            = db.Column(db.String(5))
    intituleT         = db.Column(db.String(50))
    descT             = db.Column(db.String(100))
    typeT             = db.Column(db.String(30))
    etatT             = db.Column(db.Integer)
    nbEquipe          = db.Column(db.Integer)
    nbParticipantsMax = db.Column(db.Integer)
    disciplineT       = db.Column(db.String(30))
    stream            = db.Column(db.Text)
    lieuT             = db.Column(db.String(30))
    logoT             = db.Column(db.Text)

class PARTICIPANT(db.Model):
    idP     = db.Column(db.Integer, primary_key = True)
    nomP    = db.Column(db.String(100))
    prenomP = db.Column(db.String(100))
    mailP   = db.Column(db.String(100))

class EQUIPE(db.Model):
    idE           = db.Column(db.Integer, primary_key = True,  autoincrement = True)
    idT           = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"), primary_key = True, autoincrement = False)
    etatE         = db.Column(db.Integer)
    points        = db.Column(db.Integer)
    nbParticipant = db.Column(db.Integer)
    idChefE       = db.Column(db.Integer, db.ForeignKey("PARTICIPANT.idP"))
    nomE          = db.Column(db.String(100))
    idT           = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"))

class PHOTO(db.Model):
    idPhoto   = db.Column(db.Integer, primary_key = True)
    idT       = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"),primary_key = True,)
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

def get_All_Tournois_Inactifs():
    return TOURNOI.query.filter_by(etatT = 0)

def get_All_Tournois_Admin():
    return TOURNOI.query.filter_by(idAdmin = 1)

def get_Tournoi_by_id(id):
    return TOURNOI.query.filter_by(idT = id)[0]

def get_All_Equipes():
    return EQUIPE.query.all()

def get_All_Participants():
    return PARTICIPANT.query.all()

def get_membres_constituer(idEquipe):
    return CONSTITUER.query.filter_by(idE = idEquipe)

def get_participant_by_id_equipe(idEquipe):
    membres = []
    listeParticipants = get_membres_constituer(idEquipe)
    for participant in listeParticipants:
        membres.append(PARTICIPANT.query.filter_by(idP = participant.idP).all()[0])
    return membres

def count_tournoi():
    return TOURNOI.query.count()

def get_All_Photos(idTournoi):
    return PHOTO.query.filter_by(idT = idTournoi)

def get_equipe_by_tournoi(idTournoi):
    return EQUIPE.query.filter_by(idT = idTournoi)

def get_equipe_by_id(id):
    return EQUIPE.query.filter_by(idE = id)[0]

def get_All_Equipes_Classe(idT):  #à changer pour prendr les équipe d'un tournoi
    return EQUIPE.query.order_by(EQUIPE.points).filter_by(idT = idT)

#def get_Match_A_Venir():
#    return EQUIPE.query.order_by(points)

def get_nom_prenom_by_tournoi(etatT):
    dico = {}
    if etatT == 1:
        tournois = get_All_Tournois_Actifs()
    elif etatT == 2:
        tournois = get_All_Tournois_Terminees()
    elif etatT == 0:
        tournois = get_All_Tournois_Inactifs()
    for tournoi in tournois:
        admin = ADMIN.query.filter_by(idAdmin=tournoi.idAdmin)[0]
        dico[tournoi.idT] = [tournoi.idAdmin,admin.nomAdmin,admin.prenomAdmin]
    return dico

def insert_tournoi(tournoi):
    newTournoi = TOURNOI(idAdmin = 1, regleT = tournoi['regleT'], dateT = tournoi['dateT'],
    dureeT = tournoi['dureeT'], intituleT = tournoi['intituleT'], descT = tournoi['descT'],
    typeT = tournoi['typeT'],etatT = tournoi['etatT'], nbEquipe = tournoi['nbEquipe'],
    nbParticipantsMax = tournoi['nbParticipantsMax'],disciplineT = tournoi['disciplineT'],
    lieuT = tournoi['lieuT'], logoT = tournoi['logoT'], stream = tournoi['stream'])
    db.session.add(newTournoi)
    db.session.commit()

def update_tournoi(tournoi,id):
    tournoiUp=get_Tournoi_by_id(id)
    tournoiUp.intituleT=tournoi['intituleT']
    tournoiUp.regleT=tournoi['regleT']
    tournoiUp.descT=tournoi['descT']
    tournoiUp.dateT=tournoi['dateT']
    tournoiUp.dureeT=tournoi['dureeT']
    tournoiUp.typeT=tournoi['typeT']
    tournoiUp.lieuT=tournoi['lieuT']
    tournoiUp.disciplineT=tournoi['disciplineT']
    tournoiUp.nbEquipe=tournoi['nbEquipe']
    tournoiUp.nbParticipantsMax=tournoi['nbParticipantsMax']
    tournoiUp.logoT=tournoi['logoT']
    tournoiUp.stream=tournoi['stream']
    db.session.commit()

def insert_participant(participant):
    newParticipant = PARTICIPANT(nomP = participant['nomP'], prenomP = participant['prenomP'],
    mailP = participant['mailP'])
    db.session.add(newParticipant)
    db.session.commit()
    return newParticipant.idP

def insert_equipe(equipe):
    newEquipe = EQUIPE(etatE = 0, nbParticipant = equipe['tailleEquipe'], idChefE = equipe['capitaine'],
    nomE = equipe['nom_equipe'], idT = equipe['idTournoi'])
    # print(newEquipe.__dict__)
    db.session.add(newEquipe)
    db.session.commit()
    return newEquipe.idE

def insert_constituer(idEquipe, idParticipant):
    newConstituer = CONSTITUER(idP = idParticipant, idE = idEquipe)
    db.session.add(newConstituer)
    db.session.commit()

@login_manager.user_loader
def load_user(username):
        return ADMIN.query.get(username)
