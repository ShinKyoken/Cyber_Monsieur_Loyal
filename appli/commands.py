import click
from .app import app, db, engine
from .models import *
import shutil

@app.cli.command()
def reloadbd() :

    tournois = get_All_Tournois()

    for tournoi in tournois:
        try:
            shutil.rmtree('./static/tournoi_' + tournoi.intituleT + "_" + str(tournoi.idT))
            print("Delete")
        except:
            pass
            print("Je peux pas")
    try:
        PARTICIPERPARTIE.__table__.drop(engine)
        print("Table PARTICIPERPARTIE supprimée")
        CONSTITUER.__table__.drop(engine)
        print("Table CONSTITUER supprimée")
        PHOTO.__table__.drop(engine)
        print("Table PHOTO supprimée")
        PARTIE.__table__.drop(engine)
        print("Table PARTIE supprimée")
        EQUIPE.__table__.drop(engine)
        print("Table EQUIPE supprimée")
        REGLE.__table__.drop(engine)
        print("Table REGLE supprimée")
        PARTICIPANT.__table__.drop(engine)
        print("Table PARTICIPANT supprimée")
        TOURNOI.__table__.drop(engine)
        print("Table TOURNOI supprimée")
        ADMIN.__table__.drop(engine)
        print("Table ADMIN supprimée")

        print("Toutes les tables sont supprimées")

        db.create_all()

        print("Tables créées")

        newAdmin1 = ADMIN(idAdmin = 1,
                         nomAdmin = 'PANDION',
                         mdpAdmin = 'motdepasse')


        newAdmin2 = ADMIN(nomAdmin = 'PAUTHIER',
                         mdpAdmin = 'motdepasse2')

        db.session.add(newAdmin1)
        db.session.add(newAdmin2)
        db.session.commit()
        print("Administrateurs ajoutés à la BD")
    except:
        print("Vérifiez la base de données, elle n'est sûrement pas pleine.")


@app.cli.command()
def createbd() :
    db.create_all()
    print("Base de données créée")
