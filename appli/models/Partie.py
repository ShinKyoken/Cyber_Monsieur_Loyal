from appli.app import db, login_manager
import datetime

class PARTIE(db.Model):
    idPartie      = db.Column(db.Integer, primary_key = True, autoincrement = True)
    idT           = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"), primary_key = True, autoincrement = False )
    cartePartie   = db.Column(db.String(100))
    datePartie    = db.Column(db.DateTime, default=datetime.datetime.now())
    etatPartie    = db.Column(db.Integer, default=0)

def insert_partie(idTournoi):
    """
    param: idTournoi (int), identifiant d'un tournoi

    insert une partie dans la BD
    """
    newPartie = PARTIE(idT = idTournoi)
    db.session.add(newPartie)
    db.session.commit()
    return newPartie.idPartie

def get_All_partie_by_tournoi(idTournoi):
    """
    param: idTournoi (int), identifiant d'un tournoi

    retourne les partie d'un tournoi
    """
    return PARTIE.query.filter_by(idT = idTournoi, etatPartie = 0)

def set_Map(idPartie, mapPartie):
    """
    param : idPartie(int), l'identifiant d'une partie . mapPartie, une map.

    Ajoute une map à une partie
    """

    partie = get_Partie_by_id(idPartie)
    partie.cartePartie = mapPartie
    db.session.commit()

def set_Etat_Partie(idPartie):
    """
    param : idPartie(int), l'identifiant d'une partie.

    Change l'état de la partie
    """

    partie = get_Partie_by_id(idPartie)
    partie.etatPartie = 1
    db.session.commit()

def get_Partie_by_id(idPartie):
    """
    param : idPartie(int), l'identifiant d'une partie.

    Retourne la partie
    """

    return PARTIE.query.filter_by(idPartie = idPartie).one()

def get_All_Parties_Terminees(idTournoi):
    """
    param : idTournoi(int), l'identifiant du tournoi.

    Retourne les parties terminées du tournoi.
    """

    return PARTIE.query.filter_by(idT = idTournoi, etatPartie = 1).all()
