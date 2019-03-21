from appli.app import db, login_manager
import datetime
import os

class PHOTO(db.Model):
    idPhoto   = db.Column(db.Integer, primary_key = True, autoincrement=True)
    idT       = db.Column(db.Integer,db.ForeignKey("TOURNOI.idT"),primary_key = True, autoincrement=False)
    nomPhoto  = db.Column(db.String(60))
    descPhoto = db.Column(db.String(100))
    datePhoto = db.Column(db.DateTime, default = datetime.datetime.now())

def get_All_Photos(idTournoi):
    """
    param: idTournoi (int), identifiant d'un tournoi

    retourne les photos d'un tournoi
    """
    return PHOTO.query.filter_by(idT = idTournoi).all()

def insert_photo(photo, tournoi):
    """
    param : photo(dictionnaire), une photo . tournoi, l'identifiant du tournoi.

    Ajoute une photo dans la BD
    """
    newPhoto=PHOTO(
    idT = tournoi,
    nomPhoto = photo.filename
    )
    db.session.add(newPhoto)
    db.session.commit()
<<<<<<< HEAD

def delete_All_Photos(idTournoi):
    photos = get_All_Photos(idTournoi)
    for photo in photos:
        db.session.delete(photo)
        db.session.commit()
=======
    return newPhoto

def get_photo_by_id(idPhoto) :
    """
    param: idPhoto (int), identifiant d'une photo
    Retourne une photo
    """

    return PHOTO.query.filter_by(idPhoto = idPhoto).one()
>>>>>>> 4a512061ba1567f93a7505d2250abedbde64f4e3
