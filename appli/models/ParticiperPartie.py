from appli.app import db, login_manager


class PARTICIPERPARTIE(db.Model):
    idE      = db.Column(db.Integer, db.ForeignKey("EQUIPE.idE"),primary_key=True)
    idPartie = db.Column(db.Integer, db.ForeignKey("PARTIE.idPartie"),primary_key=True)
    idT      = db.Column(db.Integer, db.ForeignKey("TOURNOI.idT"),primary_key=True)

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

def get_All_ParticiperParties_by_id_tournoi(idTournoi):
    """
    param : idTournoi(int), l'identifiant d'un tournoi.

    Retourne les participerPartie correspondant au tournoi.
    """

    return PARTICIPERPARTIE.query.filter_by(idT = idTournoi).all()
