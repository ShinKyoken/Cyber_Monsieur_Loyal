from appli.app import db, login_manager

class PARTICIPANT(db.Model):
    idP     = db.Column(db.Integer, primary_key = True)
    nomP    = db.Column(db.String(100))
    prenomP = db.Column(db.String(100))
    mailP   = db.Column(db.String(100))

def insert_participant(participant):
    """
    param: participant (dictionnaire), représente un membre d'une équipe dans un tournoi

    insert un membre dans la BD
    """
    newParticipant = PARTICIPANT(nomP = participant['nomP'], prenomP = participant['prenomP'],
    mailP = participant['mailP'])
    db.session.add(newParticipant)
    db.session.commit()
    return newParticipant.idP

def update_participant(participant, idParticipant):
    """
    param: participant (dictionnaire), représente un membre d'une équipe dans un tournoi
           idParticipant (int), identifiant d'un membre

    Modifie un membre dans la BD
    """
    participantUp = get_participant_by_id(idParticipant)
    participantUp.nomP = participant['nomP']
    participantUp.prenomP = participant['prenomP']
    participantUp.mailP = participant['mailP']
    db.session.commit()

def delete_chef(id):
    """
    param : id(int), l'identifiant d'un chef.

    Supprime le chef d'équipe
    """

    chef = PARTICIPANT.query.filter_by(idP = id)[0]
    db.session.delete(chef)
    db.session.commit()

def get_participant_by_id(idParticipant):
    """
    param: idParticipant(int), identifiant d'un participant

    retourne un participant a partir de son identifiant
    """
    return PARTICIPANT.query.filter_by(idP = idParticipant)[0]
