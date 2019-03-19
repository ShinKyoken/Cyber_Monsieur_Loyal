from appli.app import db, login_manager
import os

class TOURNOI(db.Model):
    idT               = db.Column(db.Integer, primary_key = True)
    idAdmin           = db.Column(db.Integer, db.ForeignKey("ADMIN.idAdmin"))
    dateT             = db.Column(db.Date)
    dateFinT          = db.Column(db.Date)
    intituleT         = db.Column(db.String(100))
    descT             = db.Column(db.String(100))
    etatT             = db.Column(db.Integer)
    nbEquipe          = db.Column(db.Integer)
    nbParticipantsMax = db.Column(db.Integer)
    disciplineT       = db.Column(db.String(30))
    stream            = db.Column(db.Text)
    lieuT             = db.Column(db.String(30))
    logoT             = db.Column(db.Text)
    cheminMaps        = db.Column(db.String(200))
    cheminScript      = db.Column(db.String(200))
    dossierPhotos     = db.Column(db.String(200))
    dossierReglement  = db.Column(db.String(200))
    nbTours           = db.Column(db.Integer, default = 0)

def insert_tournoi(tournoi):
    """
    param: tournoi (dictionnaire), représente un tournoi

    insert un tournoi dans la BD
    """
    newTournoi = TOURNOI(
        idAdmin           = tournoi['idAdmin'],
        dateT             = tournoi['dateT'],
        dateFinT          = tournoi['dateFinT'],
        intituleT         = tournoi['intituleT'],
        descT             = tournoi['descT'],
        etatT             = tournoi['etatT'],
        nbEquipe          = tournoi['nbEquipe'],
        nbParticipantsMax = tournoi['nbParticipantsMax'],
        disciplineT       = tournoi['disciplineT'],
        lieuT             = tournoi['lieuT'],
        logoT             = tournoi['logoT'],
        stream            = tournoi['stream'],
        nbTours           = tournoi['nbTours'],
        cheminScript      = tournoi['cheminScript'],
        cheminMaps        = tournoi['cheminMaps'],
    )
    db.session.add(newTournoi)
    db.session.commit()

    # newRegle = REGLE(idT = newTournoi.idT,
    #                  nomFic = tournoi['reglement'].filename,
    #                  data = tournoi['reglement'].read())
    # db.session.add(newRegle)
    # db.session.commit()
    id = newTournoi.idT

    return id

def update_tournoi(tournoi,id):

    """
    param: tournoi (dictionnaire), représente un tournoi
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
    tournoiUp.nbTours           = tournoi['nbTours']
    tournoiUp.cheminMaps        = tournoi['cheminMaps']
    tournoiUp.cheminScript      = tournoi['cheminScript']
    db.session.commit()

def get_All_Tournois_by_Etat(etatTournoi):
    """
    retourne la liste des tournois inactifs
    """
    return TOURNOI.query.filter_by(etatT = etatTournoi)

def get_Tournoi_by_id(id):
    """
    param: id (int), identifiant d'un tournoi

    retourne un tournoi selon son identifiant
    """
    return TOURNOI.query.filter_by(idT = id)[0]

def count_tournoi():
    """
    retourne le nombre de tournoi
    """
    return TOURNOI.query.count()

def insert_cheminPhotos(cheminPhotos, idT):
    tournoi = get_Tournoi_by_id(idT)
    tournoi.dossierPhotos = cheminPhotos
    db.session.commit()

def insert_cheminReglement(cheminReglement, idT):
    tournoi = get_Tournoi_by_id(idT)
    tournoi.dossierReglement = cheminReglement
    db.session.commit()

def get_All_Maps(idTournoi):
    """
    param : idTournoi(int), l'identifiant d'un tournoi.

    Retourne une liste de maps
    """

    tournoi = get_Tournoi_by_id(idTournoi)
    listeMaps = os.listdir(tournoi.cheminMaps)
    return listeMaps

def getRechercheAllTournois(recherche):
    """
    param: recherche (str), ce que l'utilisateur a entré dans la barre de rechercheTournois

    recherche dans les tournois
    """
    t=get_All_Tournois_Admin()
    return t.filter(TOURNOI.intituleT.like(recherche +"%")).all()

def getRechercheTournois(recherche, etatTournoi):
    """
    param: recherche (str), ce que l'utilisateur a entré dans la bar de rechercheTournois

    recherche dans les tournois inactifs
    """
    t = get_All_Tournois_by_Etat(etatTournoi)
    return t.filter(TOURNOI.intituleT.like(recherche +"%"))
