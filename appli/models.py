from .app import db, login_manager
from flask_login import UserMixin, current_user
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from sqlalchemy import exc
import random
import datetime
import sys
import json
import os

class ADMIN(UserMixin,db.Model):
    idAdmin        = db.Column(db.Integer, primary_key = True)
    nomAdmin       = db.Column(db.String(100))
    mdpAdmin       = db.Column(db.String(100))
    def get_id(self) :
        return self.idAdmin

class TOURNOI(db.Model):
    idT               = db.Column(db.Integer, primary_key = True)
    idAdmin           = db.Column(db.Integer, db.ForeignKey("ADMIN.idAdmin"))
    dateT             = db.Column(db.Date)
    dateFinT          = db.Column(db.Date)
    intituleT         = db.Column(db.String(50))
    descT             = db.Column(db.String(100))
    etatT             = db.Column(db.Integer)
    nbEquipe          = db.Column(db.Integer)
    nbParticipantsMax = db.Column(db.Integer)
    disciplineT       = db.Column(db.String(30))
    stream            = db.Column(db.Text)
    lieuT             = db.Column(db.String(30))
    logoT             = db.Column(db.Text)

class REGLE(db.Model):
    idT     = db.Column(db.Integer, db.ForeignKey("TOURNOI.idT"), primary_key = True)
    nomFic  = db.Column(db.String(100))
    data    = db.Column(db.LargeBinary(length = 2**24-1))

class PARTICIPANT(db.Model):
    idP     = db.Column(db.Integer, primary_key = True)
    nomP    = db.Column(db.String(100))
    prenomP = db.Column(db.String(100))
    mailP   = db.Column(db.String(100))

class EQUIPE(db.Model):
    idE           = db.Column(db.Integer, primary_key = True, autoincrement=True)
    idT           = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"),primary_key = True, autoincrement=False)
    etatE         = db.Column(db.Integer)
    points        = db.Column(db.Integer, default = 0)
    nbParticipant = db.Column(db.Integer)
    idChefE       = db.Column(db.Integer, db.ForeignKey("PARTICIPANT.idP"))
    nomE          = db.Column(db.String(100))
    commandShell  = db.Column(db.String(100))

class PHOTO(db.Model):
    idPhoto   = db.Column(db.Integer, primary_key = True, autoincrement=True)
    idT       = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"),primary_key = True, autoincrement=False)
    Photo     = db.Column(db.LargeBinary(length=2**24-1))
    titrePhoto= db.Column(db.String(60))
    descPhoto = db.Column(db.String(100))
    datePhoto = db.Column(db.DateTime, default = datetime.datetime.now())

class CONSTITUER(db.Model):
    idP = db.Column(db.Integer, db.ForeignKey("PARTICIPANT.idP"),primary_key=True)
    idE = db.Column(db.Integer, db.ForeignKey("EQUIPE.idE"), primary_key=True)

class PARTIE(db.Model):
    idPartie      = db.Column(db.Integer, primary_key = True, autoincrement = True)
    idT           = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"), primary_key = True, autoincrement = False )
    cartePartie   = db.Column(db.String(100))
    datePartie    = db.Column(db.DateTime, default=datetime.datetime.now())
    etatPartie    = db.Column(db.Integer, default=0)

class PARTICIPERPARTIE(db.Model):
    idE      = db.Column(db.Integer, db.ForeignKey("EQUIPE.idE"),primary_key=True)
    idPartie = db.Column(db.Integer, db.ForeignKey("PARTIE.idPartie"),primary_key=True)
    idT      = db.Column(db.Integer, db.ForeignKey("TOURNOI.idT"),primary_key=True)

db.session.commit()
def get_All_Admins():
    """
    retourne la liste des Admins
    """
    return ADMIN.query.all()

def get_All_Tournois_Inactifs():
    """
    retourne la liste des tournois inactifs
    """
    return TOURNOI.query.filter_by(etatT = 0)

def get_All_Tournois_Actifs():
    """
    retourne la liste des tournois actifs
    """
    return TOURNOI.query.filter_by(etatT = 1)

def get_All_Tournois_Terminees():
    """
    retourne la liste des tournois terminé
    """
    return TOURNOI.query.filter_by(etatT = 2)

def get_All_Tournois_Admin():
    """
    retourne la liste des tournois de l'admin connecté
    """
    return TOURNOI.query.filter_by(idAdmin = current_user.idAdmin)

def get_Tournoi_by_id(id):
    """
    param: id (int), identifiant d'un tournoi

    retourne un tournoi selon son identifiant
    """
    return TOURNOI.query.filter_by(idT = id)[0]

def get_All_Equipes(idT):
    """
    param: idT (int), identifiant d'un tournoi

    retourne les équipes d'un tournoi
    """
    return EQUIPE.query.filter_by(idT = idT)

def count_tournoi():
    """
    retourne le nombre de tournoi
    """
    return TOURNOI.query.count()

def count_equipe_by_tournoi(idTournoi):
    return EQUIPE.query.filter_by(idT = idTournoi).count()

def get_All_Photos(idTournoi):
    """
    param: idTournoi (int), identifiant d'un tournoi

    retourne les photos d'un tournoi
    """
    return PHOTO.query.filter_by(idT = idTournoi).all()

def get_equipe_by_tournoi(idTournoi):
    """
    param: idTournoi (int), identifiant d'un tournoi

    retourne les équipes d'un tournoi
    """
    return EQUIPE.query.filter_by(idT = idTournoi).all()

def get_equipe_by_id(id):
    """
    param: id (int), identifiant d'une équipe

    retourne une équipe selon un identifiant d'équipe
    """
    return EQUIPE.query.filter_by(idE = id)[0]

def get_All_Equipes_Classe(idT):  #à changer pour prendr les équipe d'un tournoi
    """
    param: idT (int), identifiant d'un tournoi

    retourne les équipe d'un tournoi, classé par points
    """
    return EQUIPE.query.order_by(EQUIPE.points.desc()).filter_by(idT = idT)

def get_All_partie_by_tournoi(idTournoi):
    """
    param: idTournoi (int), identifiant d'un tournoi

    retourne les partie d'un tournoi
    """
    return PARTIE.query.filter_by(idT = idTournoi, etatPartie = 0)

def get_All_Equipe_by_partie(parties):
    """
    param : liste parties
    """
    listeFinale = []
    for partie in parties:
        equipes = PARTICIPERPARTIE.query.filter_by(idPartie = partie.idPartie).all()
        liste = [partie]
        for i in range(len(equipes)):
            participant = PARTICIPERPARTIE.query.filter_by(idPartie = partie.idPartie, idE = equipes[i].idE).one()
            liste.append(EQUIPE.query.filter_by(idE = participant.idE).one())
        listeFinale.append(liste)
    return listeFinale

def get_equipe_by_partie(idPartie):
    liste = []
    participants = PARTICIPERPARTIE.query.filter_by(idPartie = idPartie).all()
    for equipe in participants:
        liste.append(EQUIPE.query.filter_by(idE = equipe.idE)[0])
    return liste


#def get_All_Equipes_Classe():
#    return EQUIPE.query.order_by(points)

#def get_Match_A_Venir():
#    return EQUIPE.query.order_by(points)

def get_nom_prenom_by_tournoi(etatT):
    """
    ???
    """
    dico = {}
    if etatT == 0:
        tournois = get_All_Tournois_Inactifs()
    if etatT == 1:
        tournois = get_All_Tournois_Actifs()
    elif etatT == 2:
        tournois = get_All_Tournois_Terminees()
    for tournoi in tournois:
        admin = ADMIN.query.filter_by(idAdmin=tournoi.idAdmin)[0]
        dico[tournoi.idT] = [tournoi.idAdmin,admin.nomAdmin]
    return dico

def insert_tournoi(tournoi):
    """
    param: tournoi (dictionnaire), représante un tournoi

    insert un tournoi dans la BD
    """
    newTournoi = TOURNOI(idAdmin = tournoi['idAdmin'],
                         dateT = tournoi['dateT'],
                         dateFinT = tournoi['dateFinT'],
                         intituleT = tournoi['intituleT'],
                         descT = tournoi['descT'],
                         etatT = tournoi['etatT'],
                         nbEquipe = tournoi['nbEquipe'],
                         nbParticipantsMax = tournoi['nbParticipantsMax'],
                         disciplineT = tournoi['disciplineT'],
                         lieuT = tournoi['lieuT'],
                         logoT = tournoi['logoT'],
                         stream = tournoi['stream'])
    db.session.add(newTournoi)
    db.session.commit()

    newRegle = REGLE(idT = newTournoi.idT,
                     nomFic = tournoi['reglement'].filename,
                     data = tournoi['reglement'].read())
    db.session.add(newRegle)
    db.session.commit()
    id=newTournoi.idT
    return id

def insert_photo(photo):
    newPhoto=PHOTO(
        idT=photo["idT"],
        Photo=photo["Photo"],
        descPhoto=photo["descPhoto"],
        titrePhoto=photo["titrePhoto"]
    )
    db.session.add(newPhoto)
    db.session.commit()


def update_tournoi(tournoi,id):

    """
    param: tournoi (dictionnaire), représante un tournoi
           id (int), identifiant d'un tournoi

    modifie un tournoi dans la BD
    """

    tournoiUp                   = get_Tournoi_by_id(id)
    tournoiUp.intituleT         = tournoi['intituleT']
    tournoiUp.descT             = tournoi['descT']
    tournoiUp.dateT             = tournoi['dateT']
    tournoiUp.dateFinT          = tournoi['dateFinT']
    tournoiUp.lieuT             = tournoi['lieuT']
    tournoiUp.disciplineT       = tournoi['disciplineT']
    tournoiUp.nbEquipe          = tournoi['nbEquipe']
    tournoiUp.nbParticipantsMax = tournoi['nbParticipantsMax']
    tournoiUp.logoT             = tournoi['logoT']
    tournoiUp.stream            = tournoi['stream']
    db.session.commit()

def update_Equipe(equipe,id):

    equipeUp                        = get_equipe_by_id(id)
    equipeUp.idE                    = equipe.idE
    equipeUp.idT                    = equipe.idT
    equipeUp.etatE                  = equipe.etatE
    equipeUp.points                 = equipe.points
    equipeUp.nbParticipant          = equipe.nbParticipant
    equipeUp.idChefE                = equipe.idChefE
    equipeUp.nomE                   = equipe.nomE
    db.session.commit()


def update_regle(regle, idTournoi):
    regleUp        = get_Regle_by_id(idTournoi)
    regleUp.nomFic = regle['nomFic']
    regleUp.data   = regle['data']
    db.session.commit()

def get_Regle_by_id(idTournoi):
    return REGLE.query.filter_by(idT = idTournoi)[0]

def insert_participant(participant):
    """
    param: participant (dictionaire), représante un membre d'un groupe dans un tournoi

    insert un membre dans la BD
    """
    newParticipant = PARTICIPANT(nomP = participant['nomP'], prenomP = participant['prenomP'],
    mailP = participant['mailP'])
    db.session.add(newParticipant)
    db.session.commit()
    return newParticipant.idP

def update_participant(participant, idParticipant):
    """
    param: participant (dictionaire), représante un membre d'un groupe dans un tournoi
           idParticipant (int), identifiant d'un membre

    Modifie un membre dans la BD
    """
    participantUp = get_participant_by_id(idParticipant)
    participantUp.nomP = participant['nomP']
    participantUp.prenomP = participant['prenomP']
    participantUp.mailP = participant['mailP']
    db.session.commit()

def insert_equipe(equipe):
    """
    param: equipe (dictionaire), représante un groupe dans un tournoi

    insert une equipe dans la BD
    """
    newEquipe = EQUIPE(etatE = 0, nbParticipant = equipe['tailleEquipe'], idChefE = equipe['capitaine'],
    nomE = equipe['nom_equipe'], idT = equipe['idTournoi'], commandShell = equipe['shell'])
    db.session.add(newEquipe)
    db.session.commit()
    return newEquipe.idE

def insert_constituer(idEquipe, idParticipant):
    """
    param: idEquipe (int), identifiant d'une équipe
           idParticipant (int), identifiant d'un participant

    insert dans la BD le fait qu'un membre est dans une équipe
    """
    newConstituer = CONSTITUER(idP = idParticipant, idE = idEquipe)
    db.session.add(newConstituer)
    db.session.commit()

@login_manager.user_loader
def load_user(username):
    """
    param: username (str), le nom d'un admin

    recherche un admin qui a le nom recherché
    """
    return ADMIN.query.get(username)

def insert_partie(idTournoi):
    """
    param: idTournoi (int), identifiant d'un tournoi

    insert une partie dans la BD
    """
    newPartie = PARTIE(cartePartie = "Nuketown", idT = idTournoi)
    db.session.add(newPartie)
    db.session.commit()
    return newPartie.idPartie

def insert_participer_partie(idEquipe, idP, idTournoi):
    """
    param: idEquipe (int), identifiant d'une equipe
           idP (int), identifiant d'une partie
           idTournoi (int), identifiant d'un tournoi

    insert une participation d'une équipe à un tournoi
    """
    newParticiperPartie = PARTICIPERPARTIE(idE = idEquipe, idPartie = idP, idT = idTournoi)
    db.session.add(newParticiperPartie)
    db.session.commit()


def automatique_match(idTournoi,nbMatchs,nbParticipants):
    """
    param: nbParticipants (int), nombre de d'équipe par match
           nbMatchs (int), nompre de match par équipe
           idTournoi (int), identifiant d'un tournoi

    crée les match d'un tournoi
    """
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
            except exc.IntegrityError:
                delete_All_Parties_by_id_tournoi(idTournoi)
                res = "bug"
    if res == "bug":
        automatique_match(idTournoi,nbMatchs,nbParticipants)
    return res

def delete_All_Parties_by_id_tournoi(idTournoi):
    db.session.rollback()
    parties = get_All_partie_by_tournoi(idTournoi)
    allParticiper = get_All_ParticiperParties_by_id_tournoi(idTournoi)
    for participer in allParticiper:
        db.session.delete(participer)
        db.session.commit()
    for partie in parties:
        db.session.delete(partie)
        db.session.commit()


def lancer_match(idPartie):
    equipes = get_equipe_by_partie(idPartie)
    dico = {"equipes" : {},
            "idPartie": idPartie}
    scoreMax = None
    gagnant = None
    for equipe in equipes:
        dico["equipes"][equipe.idE] = None
    with open("parametres.json","w") as json_file:
        json.dump(dico, json_file, indent=4)
    os.system("python3 code_test.py > resultat.json")

def arreterMatch_setScore():
    res_dico = {}
    with open("resultat.json","r") as json_res:
        resultat = json.load(json_res)
        for id,score in resultat["equipes"].items():
            setPointsbyIdEquipe(id,score)
            res_dico[get_equipe_by_id(id)] = score
    set_Etat_Partie(resultat["idPartie"])
    return res_dico


def get_All_ParticiperParties_by_id_tournoi(idTournoi):
    return PARTICIPERPARTIE.query.filter_by(idT = idTournoi)

def set_Etat_Partie(idPartie):
    partie = get_Partie_by_id(idPartie)
    partie.etatPartie = 1
    db.session.commit()

def get_All_Parties_Terminees(idTournoi):
    return PARTIE.query.filter_by(idT = idTournoi, etatPartie = 1).all()

def get_Partie_by_id(idPartie):
    return PARTIE.query.filter_by(idPartie = idPartie).one()

def setPointsbyIdEquipe(idEquipe,score):
    equipe = get_equipe_by_id(idEquipe)
    equipe.points += int(score)
    db.session.commit()

def getRechercheAllTournois(recherche):
    """
    param: recherche (str), ce que l'utilisateur a entré dans la barre de rechercheTournois

    recherche dans les tournois
    """
    t=get_All_Tournois_Admin()
    return t.filter(TOURNOI.intituleT.like(recherche +"%")).all()

def getRechercheTournoisInactif(recherche):
    """
    param: recherche (str), se que l'utilisateur a entré dans la bar de rechercheTournois

    recherche dans les tournois inactifs
    """
    t = get_All_Tournois_Inactifs()
    return t.filter(TOURNOI.intituleT.like(recherche +"%"))

def getRechercheTournoisActif(recherche):
    """
    param: recherche (str), se que l'utilisateur a entré dans la bar de rechercheTournois

    recherche dans les tournois actifs
    """
    t = get_All_Tournois_Actifs()
    return t.filter(TOURNOI.intituleT.like(recherche +"%"))

def getRechercheTournoisTerminee(recherche):
    """
    param: recherche (str), se que l'utilisateur a entré dans la bar de rechercheTournois

    recherche dans les tournois terminé
    """
    t = get_All_Tournois_Terminees()
    return t.filter(TOURNOI.intituleTdb.session.commit().like(recherche +"%"))

def get_constituer(idP, idE):
    return CONSTITUER.query.filter_by(idP = idP, idE = idE)[0]

def delete_chef(id):
    chef = PARTICIPANT.query.filter_by(idP = id)[0]
    db.session.delete(chef)
    db.session.commit()

def delete_equipe(idEquipe):
    membres = get_participant_by_id_equipe(idEquipe)
    if len(membres) > 1 :
        membres = membres[1:]
        i=0
        for m in membres :
            i+=1
            delete_membre(idEquipe,m.idP)
    chef = get_participant_by_id_equipe(idEquipe)
    chef = chef[0]
    constituer = get_constituer(chef.idP,idEquipe)
    db.session.delete(constituer)
    db.session.commit()
    a = get_equipe_by_id(idEquipe)
    db.session.delete(a)
    db.session.commit()
    delete_chef(chef.idP)


def get_participant_by_id(idParticipant):
    """
    param: idParticipant, identifiant d'un participant

    retourne un participant a partir de son identifiant
    """
    return PARTICIPANT.query.filter_by(idP = idParticipant)[0]

def get_membres_constituer(idEquipe):
    """
    param: idEquipe (int), identifiant d'une équipes

    retourne une instance de la table constituer
    """
    return CONSTITUER.query.filter_by(idE = idEquipe).all()


def get_participant_by_id_equipe(idEquipe):
    """
    param: idEquipe (int), identifiant d'une équipes

    retourne la liste des membre d'une équipe
    """
    membres = []
    listeParticipants = get_membres_constituer(idEquipe)
    for participant in listeParticipants:
        membres.append(PARTICIPANT.query.filter_by(idP = participant.idP).all()[0])
    return membres

def delete_membre(idEquipe, idParticipant):
    """
    param: idEquipe (int), identifiant d'une équipes
           idParticipant, identifiant d'un participant

    supprime un membre d'une équipe
    """
    c = get_constituer(idParticipant ,idEquipe)
    db.session.delete(c)
    db.session.commit()
    p = get_participant_by_id(idParticipant)
    db.session.delete(p)
    db.session.commit()

def get_chef_by_id_equipe(idEquipe):
    """
    param: idEquipe (int), identifiant d'une équipes
db.session.commit()
    retourne le chef de l'équipe passé en paramètre
    """
    e = get_equipe_by_id(idEquipe)
    idChef = e.idChefE
    participant_chef = get_participant_by_id(idChef)
    return participant_chef

def get_admin_by_id(id):
    t=get_Tournoi_by_id(id)
    admin = ADMIN.query.filter_by(idAdmin = t.idAdmin)[0]
    return admin

def ajouter_participant(participant,e):
    p = insert_participant(participant)
    insert_constituer(e, p)
