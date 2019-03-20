from appli.app import db, login_manager

class EQUIPE(db.Model):
    idE           = db.Column(db.Integer, primary_key = True, autoincrement=True)
    idT           = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"),primary_key = True, autoincrement=False)
    etatE         = db.Column(db.Integer)
    points        = db.Column(db.Integer, default = 0)
    nbParticipant = db.Column(db.Integer)
    idChefE       = db.Column(db.Integer, db.ForeignKey("PARTICIPANT.idP"))
    nomE          = db.Column(db.String(100))
    machineE      = db.Column(db.String(100), unique = True)

def insert_equipe(equipe):
    """
    param: equipe (dictionnaire), représente une équipe dans un tournoi

    insert une equipe dans la BD
    """
    newEquipe = EQUIPE(etatE = 0, nbParticipant = equipe['tailleEquipe'], idChefE = equipe['capitaine'],
    nomE = equipe['nom_equipe'], idT = equipe['idTournoi'], machineE = equipe['machineE'])
    db.session.add(newEquipe)
    db.session.commit()
    return newEquipe.idE

def update_Equipe(equipe,id):
    """
    param: equipe (dictionnaire), représente une équipe .
           id (int), identifiant d'un tournoi

    modifie une équipe dans la BD
    """

    equipeUp               = get_equipe_by_id(id)
    equipeUp.idE           = equipe.idE
    equipeUp.idT           = equipe.idT
    equipeUp.etatE         = equipe.etatE
    equipeUp.points        = equipe.points
    equipeUp.nbParticipant = equipe.nbParticipant
    equipeUp.idChefE       = equipe.idChefE
    equipeUp.nomE          = equipe.nomE
    equipeUp.machineE      = equipe.machineE
    db.session.commit()

def count_equipe_by_tournoi(idTournoi):
    """
    param : idTournoi (int), l'identifiant du tounoi.

    Retourne le nombre d'équipe inscrites à un tournoi.
    """

    return EQUIPE.query.filter_by(idT = idTournoi).count()

def get_equipe_by_tournoi(idTournoi):
    """
    param: idTournoi (int), identifiant d'un tournoi

    retourne les équipes d'un tournoi
    """
    return EQUIPE.query.filter_by(idT = idTournoi).all()

def get_equipe_by_id(idEquipe):
    """
    param: id (int), identifiant d'une équipe

    retourne une équipe selon un identifiant d'équipe
    """
    return EQUIPE.query.filter_by(idE = idEquipe)[0]

def get_All_Equipes_Classe(idT):
    """
    param: idT (int), identifiant d'un tournoi

    retourne les équipe d'un tournoi, classé par points
    """
    return EQUIPE.query.order_by(EQUIPE.points.desc()).filter_by(idT = idT)

def setPointsbyIdEquipe(idEquipe,score):
    """
    param : idEquipe(int), l'identifiant d'une partie. score(string), le score d'une équipe.

    Ajoute ce score au score initial de l'équipe
    """

    equipe = get_equipe_by_id(idEquipe)
    equipe.points += int(score)
    db.session.commit()

def nbEquipeByMachine(nomMachine,idTournoi):
    a=EQUIPE.query.filter_by(machineE = nomMachine, idT=idTournoi).count()
    return a

def nbEquipeByNomEquipe(nom,idTournoi):
    a=EQUIPE.query.filter_by(nomE = nom, idT=idTournoi).count()
    return a
