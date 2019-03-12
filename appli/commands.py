import click
from .app import app, db, engine
from .models import *

@app.cli.command()
def reloadBD() :

    PARTICIPERPARTIE.__table__.drop(engine)
    CONSTITUER.__table__.drop(engine)
    PHOTO.__table__.drop(engine)
    PARTIE.__table__.drop(engine)
    EQUIPE.__table__.drop(engine)
    REGLE.__table__.drop(engine)
    PARTICIPANT.__table__.drop(engine)
    TOURNOI.__table__.drop(engine)
    ADMIN.__table__.drop(engine)

    db.create_all()

    newAdmin1 = ADMIN(idAdmin = 1,
                     nomAdmin = 'PANDION',
                     mdpAdmin = 'motdepasse')

    newAdmin2 = ADMIN(nomAdmin = 'PAUTHIER',
                     mdpAdmin = 'motdepasse2')

    db.session.add(newAdmin1)
    db.session.add(newAdmin2)
    db.session.commit()


@app.cli.command()
def createBD() :
    db.create_all()
