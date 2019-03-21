from appli.app import db, login_manager

class REGLE(db.Model):
    idT     = db.Column(db.Integer, db.ForeignKey("TOURNOI.idT"), primary_key = True)
    nomFic  = db.Column(db.String(100))

def insert_regle(regle, idTournoi):
    newRegle = REGLE(idT = idTournoi,
                     nomFic = regle.filename
                     )
    db.session.add(newRegle)
    db.session.commit()

def update_regle(regle, idTournoi):
    """
    param: regle (dictionnaire), représente une règle .
           idTournoi (int), identifiant d'un tournoi

    modifie une règle dans la BD
    """
    regleUp        = get_Regle_by_id(idTournoi)
    regleUp.nomFic = regle['nomFic']
    db.session.commit()

def get_Regle_by_id(idTournoi):
    return REGLE.query.filter_by(idT = idTournoi)[0]

def delete_regle(idTournoi):
    db.session.delete(get_Regle_by_id(idTournoi))
