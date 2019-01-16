from .app import db, login_manager
from flask_login import UserMixin, current_user
import random
import datetime

class ADMIN(UserMixin,db.Model):
    idAdmin        = db.Column(db.Integer, primary_key = True)
    nomAdmin       = db.Column(db.String(100))
    prenomAdmin    = db.Column(db.String(100))
    dateNaissAdmin = db.Column(db.Date)
    mdpAdmin       = db.Column(db.String(100))
    def get_id(self) :
        return self.idAdmin

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
    idE           = db.Column(db.Integer, primary_key = True, autoincrement=True)
    idT           = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"),primary_key = True, autoincrement=False)
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
    idPartie      = db.Column(db.Integer, primary_key = True, autoincrement = True)
    idT           = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"), primary_key = True, autoincrement = False )
    cartePartie   = db.Column(db.String(100))
    datePartie    = db.Column(db.DateTime, default=datetime.datetime.now())
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
    return TOURNOI.query.filter_by(idAdmin = current_user.idAdmin)

def get_Tournoi_by_id(id):
    return TOURNOI.query.filter_by(idT = id)[0]

def get_All_Equipes(idT):
    return EQUIPE.query.filter_by(idT = idT)

def insert_regle(fichier):
    newFile = TOURNOI(regleT = fichier.read())

def count_tournoi():
    return TOURNOI.query.count()

def get_All_Photos(idTournoi):
    return PHOTO.query.filter_by(idT = idTournoi)

def get_equipe_by_tournoi(idTournoi):
    return EQUIPE.query.filter_by(idT = idTournoi).all()

def get_equipe_by_id(id):
    return EQUIPE.query.filter_by(idE = id)[0]

def get_All_Equipes_Classe(idT):  #à changer pour prendr les équipe d'un tournoi
    return EQUIPE.query.order_by(EQUIPE.points).filter_by(idT = idT)

def get_All_partie_by_tournoi(idTournoi):
    return PARTIE.query.filter_by(idT = idTournoi)

def get_All_Equipe_by_partie(parties):
    listeFinale = []
    for partie in parties:
        equipes = PARTICIPERPARTIE.query.filter_by(idPartie = partie.idPartie).all()
        liste = [partie]
        for i in range(len(equipes)):
            participant = PARTICIPERPARTIE.query.filter_by(idPartie = partie.idPartie, idE = equipes[i].idE).one()
            liste.append(EQUIPE.query.filter_by(idE = participant.idE).one())
        listeFinale.append(liste)
    return listeFinale

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
    newTournoi = TOURNOI(idAdmin = current_user.idAdmin, regleT = tournoi['regleT'], dateT = tournoi['dateT'],
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

def update_participant(participant, idparticipant):
    participantUp = get_participant_by_id(idParticipant)
    participantUp.nomP = participant['nomP']
    participantUp.prenomP = participant['prenomP']
    participantUp.mailP = participant['mailP']
    db.session.commit()

def insert_equipe(equipe):
    newEquipe = EQUIPE(etatE = 0, nbParticipant = equipe['tailleEquipe'], idChefE = equipe['capitaine'],
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

def insert_partie(idTournoi):
    newPartie = PARTIE(cartePartie = "Nuketown", idT = idTournoi)
    db.session.add(newPartie)
    db.session.commit()
    return newPartie.idPartie

def insert_participer_partie(idEquipe, idP, idTournoi):
    newParticiperPartie = PARTICIPERPARTIE(idE = idEquipe, idPartie = idP, idT = idTournoi)
    db.session.add(newParticiperPartie)
    db.session.commit()


def automatique_match(idTournoi,nbMatchs,nbParticipants):
    listeEquipe = get_equipe_by_tournoi(idTournoi)
    t=get_Tournoi_by_id(idTournoi)
    t.etatT=1
    db.session.commit()
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
            listeIdPartie.append(insert_partie(idTournoi))
    else:
        for i in range(((len(listeEquipe)*nbMatchs)//nbParticipants)):
            listeIdPartie.append(insert_partie(idTournoi))

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
    t=get_All_Tournois_Admin()
    return t.filter(TOURNOI.intituleT.like(recherche +"%")).all()

def getRechercheTournoisInactif(recherche):
    t = get_All_Tournois_Inactifs()
    return t.filter(TOURNOI.intituleT.like(recherche +"%"))

def getRechercheTournoisActif(recherche):
    t = get_All_Tournois_Actifs()
    return t.filter(TOURNOI.intituleT.like(recherche +"%"))

def getRechercheTournoisTerminee(recherche):
    t = get_All_Tournois_Terminees()
    return t.filter(TOURNOI.intituleT.like(recherche +"%"))

def get_constituer(idP, idE):
    return TOURNOI.query.filter_by(idP = idP, idE = idE)

def delete_equipe(idEquipe):
    return None

def get_participant_by_id(idParticipant):
    return PARTICIPANT.query.filter_by(idP = idParticipant)[0]

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

def get_chef_by_id_equipe(idEquipe):
    e = get_equipe_by_id(idEquipe)
    idChef = e.idChefE
    participant_chef = get_participant_by_id(idChef)
    return participant_chef
