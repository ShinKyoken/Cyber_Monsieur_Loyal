from .app import db, login_manager
from flask_login import UserMixin
import random
import datetime

class ADMIN(db.Model):
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
    idE           = db.Column(db.Integer, primary_key = True)
    idT           = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"),primary_key = True)
    etatE         = db.Column(db.Integer)
    points        = db.Column(db.Integer)
    nbParticipant = db.Column(db.Integer)
    idChefE       = db.Column(db.Integer, db.ForeignKey("PARTICIPANT.idP"))
    nomE          = db.Column(db.String(100))

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
    cartePartie = db.Column(db.String(100))
    datePartie = db.Column(db.DateTime, default=datetime.datetime.now())
    gagnantPartie = db.Column(db.Integer, db.ForeignKey("EQUIPE.idE"))

class PARTICIPERPARTIE(db.Model):
    idE      = db.Column(db.Integer, db.ForeignKey("EQUIPE.idE"),primary_key=True)
    idPartie = db.Column(db.Integer, db.ForeignKey("PARTIE.idPartie"),primary_key=True)
    idT      = db.Column(db.Integer, db.ForeignKey("TOURNOI.idT"),primary_key=True)

def get_All_Admins():
    return ADMIN.query.all()

def get_All_Tournois_Inactifs():
    return TOURNOI.query.filter_by(etatT = 0)

def get_All_Tournois_Actifs():
    return TOURNOI.query.filter_by(etatT = 1)

def get_All_Tournois_Terminees():
    return TOURNOI.query.filter_by(etatT = 2)

def get_All_Tournois_Admin():
    return TOURNOI.query.filter_by(idAdmin = 1)

def get_Tournoi_by_id(id):
    return TOURNOI.query.filter_by(idT = id)[0]

def get_All_Equipes(idT):
    return EQUIPE.query.filter_by(idT = idT)

def count_tournoi():
    return TOURNOI.query.count()

def get_All_Photos(idTournoi):
    return PHOTO.query.filter_by(idT = idTournoi)

def get_equipe_by_tournoi(idTournoi):
    return EQUIPE.query.filter_by(idT = idTournoi).all()

def get_equipe_by_id(id):
    return EQUIPE.query.filter_by(idE = id)

def get_All_Equipes_Classe(idT):  #à changer pour prendr les équipe d'un tournoi
    return EQUIPE.query.order_by(EQUIPE.points).filter_by(idT = idT)
#def get_All_Equipes_Classe():
#    return EQUIPE.query.order_by(points)

#def get_Match_A_Venir():
#    return EQUIPE.query.order_by(points)

def get_nom_prenom_by_tournoi(etatT):
    dico = {}
    if etatT == 0:
        tournois = get_All_Tournois_Inactifs()
    if etatT == 1:
        tournois = get_All_Tournois_Actifs()
    elif etatT == 2:
        tournois = get_All_Tournois_Terminees()
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
    newEquipe = EQUIPE(etatE = 0, nbParticipant = 3, idChefE = equipe['capitaine'],
    nomE = equipe['nom_equipe'], idT = equipe['idTournoi'])
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

def insert_partie():
    newPartie = PARTIE(cartePartie = "Nuketown")
    db.session.add(newPartie)
    db.session.commit()
    return newPartie.idPartie

def insert_participer_partie(idEquipe, idP, idTournoi):
    newParticiperPartie = PARTICIPERPARTIE(idE = idEquipe, idPartie = idP, idT = idTournoi)
    db.session.add(newParticiperPartie)
    db.session.commit()


def automatique_match(idTournoi,nbMatchs,nbParticipants):
    listeEquipe = get_equipe_by_tournoi(idTournoi)
    listeId = []
    listeIdPartie = []
    listeIdPerMatchs = []
    res = "Votre tournoi a été crée sans problème."

    for equipe in listeEquipe:
        listeId.append(equipe.idE)

    for i in range(nbMatchs):
        liste = listeId.copy()
        listeIdPerMatchs.append(liste)

    if ((len(listeEquipe)*nbMatchs)/nbParticipants) > ((len(listeEquipe)*nbMatchs)//nbParticipants):
        for i in range(((len(listeEquipe)*nbMatchs)//nbParticipants)+1):
            listeIdPartie.append(insert_partie())
    else:
        for i in range(((len(listeEquipe)*nbMatchs)//nbParticipants)):
            listeIdPartie.append(insert_partie())

    for partie in listeIdPartie:
        for i in range (nbParticipants):
            try:
                nb = random.randint(0,len(listeIdPerMatchs[0])-1)
                insert_participer_partie(listeIdPerMatchs[0][nb],partie,idTournoi)
                del listeIdPerMatchs[0][nb]
                if len(listeIdPerMatchs[0]) == 0:
                    del listeIdPerMatchs[0]
            except IndexError:
                res = "Votre tournoi à bien été crée, cependant un match ne sera pas complet"
                break
    return res

def getRechercheAllTournois(recherche):
    return TOURNOI.query.filter(
        TOURNOI.intituleT.like(recherche +"%")
    ).all()

def getRechercheTournoisActif(recherche):
    t = get_All_Tournois_Actifs()
    return t.filter(TOURNOI.intituleT.like(recherche +"%"))

def get_constituer(idP, idE):
    return TOURNOI.query.filter_by(idP = idP, idE = idE)

def delete_equipe(idEquipe):
    return None

def get_participant_by_id(idP):
    return TOURNOI.query.filter_by(idP = idP)

def get_membres_constituer(idEquipe):
    return CONSTITUER.query.filter_by(idE = idEquipe)

def get_participant_by_id_equipe(idEquipe):
    membres = []
    listeParticipants = get_membres_constituer(idEquipe)
    for participant in listeParticipants:
        membres.append(PARTICIPANT.query.filter_by(idP = participant.idP).all()[0])
    return membres

def delete_membre(idEquipe, idParticipant):
    c = get_constituer(idEquipe, idParticipant)
    db.session.delete(c)
    p = get_participant_by_id(idParticipant)
    db.session.delete(p)
