from .Admin import *
from .Tournoi import *
from .Regle import *
from .Participant import *
from .Equipe import *
from .Photo import *
from .Constituer import *
from .Partie import *
from .ParticiperPartie import *
import shutil
from sqlalchemy import exc
import json
import random

def get_equipe_by_partie(idPartie):
    """
    param : idPartie(int), l'identifiant d'une partie.

    Retourne les équipes participant à la partie
    """
    liste = []
    participants = PARTICIPERPARTIE.query.filter_by(idPartie = idPartie).all()
    for equipe in participants:
        liste.append(EQUIPE.query.filter_by(idE = equipe.idE)[0])
    return liste


def get_admin_by_tournoi(etatT):
    """
    param : etatT(int) , l'état d'un tournoi

    Retourne un dictionnaire ayant pour clé l'id d'un tournoi et pour valeur l'id de l'admin et son nom.
    """
    dico = {}
    tournois = get_All_Tournois_by_Etat(etatT)
    for tournoi in tournois:
        admin = ADMIN.query.filter_by(idAdmin=tournoi.idAdmin)[0]
        dico[tournoi.idT] = [tournoi.idAdmin,admin.nomAdmin]
    return dico

def get_admin_by_id(idTournoi):
    """
    param : idTournoi(int), l'identifiant d'un tournoi

    retourne un admin
    """

    tournoi = get_Tournoi_by_id(idTournoi)
    admin = ADMIN.query.filter_by(idAdmin = tournoi.idAdmin)[0]
    return admin

def get_All_Tournois_Admin():
    """
    retourne la liste des tournois de l'admin connecté
    """
    return TOURNOI.query.filter_by(idAdmin = current_user.idAdmin).all()

def get_All_Tournois_Admin_Function():
    """
    retourne la liste des tournois de l'admin connecté
    """
    return TOURNOI.query.filter_by(idAdmin = current_user.idAdmin)

def get_All_Equipes(idT):
    """
    param: idT (int), identifiant d'un tournoi

    retourne les équipes d'un tournoi
    """
    return EQUIPE.query.filter_by(idT = idT)

def get_All_Equipe_by_partie(parties):
    """
    param : liste parties

    Retourne une liste contenant les équipes qui participent aux parties passés en paramètre.
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

def get_admin_by_tournoi(etatTournoi):
    """
    param : etatT(int) , l'état d'un tournoi

    Retourne un dictionnaire ayant pour clé l'id d'un tournoi et pour valeur l'id de l'admin et son nom.
    """
    dico = {}
    tournois = get_All_Tournois_by_Etat(etatTournoi)
    for tournoi in tournois:
        admin = ADMIN.query.filter_by(idAdmin=tournoi.idAdmin)[0]
        dico[tournoi.idT] = [tournoi.idAdmin,admin.nomAdmin]
    return dico

def automatique_match(idTournoi,nbMatchs,nbParticipants):
    """
    param: nbParticipants (int), nombre de d'équipe par match
           nbMatchs (int), nompre de match par équipe
           idTournoi (int), identifiant d'un tournoi

    crée les match d'un tournoi
    """
    listeEquipe = get_equipe_by_tournoi(idTournoi)
    t = get_Tournoi_by_id(idTournoi)
    t.etatT = 1
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
        automatique_match(idTournoi,nbMatchs,nbParticipants, listeMaps)
    return res

def delete_All_Parties_by_id_tournoi(idTournoi):
    """
    param : idTournoi(int), l'identifiant d'un tournoi.

    supprime toutes les parties d'un tournoi.
    """

    db.session.rollback()
    parties = get_All_partie_by_tournoi(idTournoi)
    allParticiper = get_All_ParticiperParties_by_id_tournoi(idTournoi)
    for participer in allParticiper:
        db.session.delete(participer)
        db.session.commit()
    for partie in parties:
        db.session.delete(partie)
        db.session.commit()
    print("Parties supprimées")

def lancer_match(idPartie, mapPartie):
    """
    param : idPartie(int), l'identifiant d'une partie. mapPartie, une map.

    Lance une partie
    """
    equipes = get_equipe_by_partie(idPartie)
    set_Map(idPartie, mapPartie)
    partie = get_Partie_by_id(idPartie)
    tournoi = get_Tournoi_by_id(partie.idT)
    dico = {"equipes" : {},
            "parametres": {
                "map" : tournoi.cheminMaps + partie.cartePartie,
                "n_tours" : tournoi.nbTours,
                "idPartie": idPartie
                }
            }
    for equipe in equipes:
        dico["equipes"][equipe.idE] = {"machine" : equipe.machineE}
    with open("parametres.json","w") as json_file:
        json.dump(dico, json_file, indent=4)
    os.system("python3 " + tournoi.cheminScript + "< parametres.json > resultat.json")

def arreterMatch_setScore(idPartie):
    """
    param : idPartie(int), l'identifiant d'une partie.

    Arrete la partie
    """

    res_dico = {}
    with open("resultat.json","r") as json_res:
        resultat = json.load(json_res)
        for id,score in resultat["equipes"].items():
            setPointsbyIdEquipe(id,score)
            res_dico[get_equipe_by_id(id)] = score
    set_Etat_Partie(idPartie)
    return res_dico

def delete_equipe(idEquipe):
    """
    param : idEquipe (int), l'identifiant d'une équipe.

    Supprime l'équipe
    """

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
           idParticipant(int), identifiant d'un participant

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

    retourne le chef de l'équipe passé en paramètre
    """
    e = get_equipe_by_id(idEquipe)
    idChef = e.idChefE
    participant_chef = get_participant_by_id(idChef)
    return participant_chef

def ajouter_participant(participant,e):
    """
    param : participant (dictionnaire), un participant. e(dictionnaire), une équipe.

    ajoute un participant
    """

    p = insert_participant(participant)
    insert_constituer(e, p)

def getRechercheAllTournois(recherche):
    """
    param: recherche (str), ce que l'utilisateur a entré dans la barre de rechercheTournois

    recherche dans les tournois
    """
    t = get_All_Tournois_Admin_Function()
    return t.filter(TOURNOI.intituleT.like(recherche +"%")).all()

def getRechercheTournois(recherche, etatTournoi):
    """
    param: recherche (str), ce que l'utilisateur a entré dans la bar de rechercheTournois

    recherche dans les tournois inactifs
    """
    t = get_All_Tournois_by_Etat_Function(etatTournoi)
    return t.filter(TOURNOI.intituleT.like(recherche +"%")).all()

def delete_tournoi(idTournoi):
    delete_All_Parties_by_id_tournoi(idTournoi)
    equipes = get_equipe_by_tournoi(idTournoi)
    for equipe in equipes:
        delete_equipe(equipe.idE)
    delete_All_Photos(idTournoi)
    delete_regle(idTournoi)
    tournoi = get_Tournoi_by_id(idTournoi)
    try:
        shutil.rmtree(tournoi.dossierPhotos)
    except:
        pass
    try:
        shutil.rmtree("appli/" + tournoi.dossierReglement)
    except:
        pass
    try:
        shutil.rmtree("tournoi_" + tournoi.intituleT + "_" + str(tournoi.idT))
    except:
        pass

    db.session.delete(tournoi)
    db.session.commit()


def delete_photo(idPhoto) :
    """
    param idPhoto (int), identifiant d'une photo
    Supprime la photo dans la BD
    """
    photo = get_photo_by_id(idPhoto)
    tournoi = get_Tournoi_by_id(photo.idT)
    os.remove(tournoi.dossierPhotos + str(photo.idPhoto) + "_" + photo.nomPhoto)

    db.session.delete(photo)
    db.session.commit()
