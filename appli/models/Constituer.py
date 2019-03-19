from appli.app import db, login_manager

class CONSTITUER(db.Model):
    idP = db.Column(db.Integer, db.ForeignKey("PARTICIPANT.idP"),primary_key=True)
    idE = db.Column(db.Integer, db.ForeignKey("EQUIPE.idE"), primary_key=True)

def insert_constituer(idEquipe, idParticipant):
    """
    param: idEquipe (int), identifiant d'une équipe
           idParticipant (int), identifiant d'un participant

    insert dans la BD le fait qu'un membre est dans une équipe
    """
    newConstituer = CONSTITUER(idP = idParticipant, idE = idEquipe)
    db.session.add(newConstituer)
    db.session.commit()

def get_constituer(idP, idE):
    return CONSTITUER.query.filter_by(idP = idP, idE = idE)[0]

def get_membres_constituer(idEquipe):
    """
    param: idEquipe (int), identifiant d'une équipes

    retourne une instance de la table constituer
    """
    return CONSTITUER.query.filter_by(idE = idEquipe).all()
