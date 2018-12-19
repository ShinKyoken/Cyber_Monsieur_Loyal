from .app import app
from .models import *
from flask import render_template, redirect, url_for, request

@app.route("/")
def home():
    return render_template(
        "home.html")


@app.route("/creer_competition")
def creerCompetition():
    return render_template("creerCompetition.html")

@app.route("/test")
def test():
    return render_template("nouveauCreerCompetition.html")
    
@app.route("/confirmer_competition", methods={"POST"})
def confirmerTournoi():
    tournoi = {}
    tournoi['intituleT']         = request.form['intituleT']
    tournoi['regleT']            = request.form['regleT']
    tournoi['descT']             = request.form['descT']
    tournoi['dateT']             = request.form['dateT']
    tournoi['dureeT']            = request.form['dureeT']
    tournoi['typeT']             = request.form['typeT']
    tournoi['lieuT']             = request.form['lieuT']
    tournoi['disciplineT']       = request.form['disciplineT']
    tournoi['nbEquipe']          = request.form['nbEquipe']
    tournoi['nbParticipantsMax'] = request.form['nbParticipantsMax']
    tournoi['logoT']             = request.form['logoT']
    tournoi['stream']            = request.form['stream']
    tournoi['etatT']             = 1
    tournoi['idAdmin']           = 1
    insert_tournoi(tournoi)
    return render_template("confirmerTournoi.html")

@app.route("/tableau_de_bord/<int:id>/modifier_competition", methods={"POST"})
def modifierTournoi(id):
    tournoi = {}
    tournoi['intituleT']         = request.form['intituleT']
    tournoi['regleT']            = request.form['regleT']
    tournoi['descT']             = request.form['descT']
    tournoi['dateT']             = request.form['dateT']
    tournoi['dureeT']            = request.form['dureeT']
    tournoi['typeT']             = request.form['typeT']
    tournoi['lieuT']             = request.form['lieuT']
    tournoi['disciplineT']       = request.form['disciplineT']
    tournoi['nbEquipe']          = request.form['nbEquipe']
    tournoi['nbParticipantsMax'] = request.form['nbParticipantsMax']
    tournoi['logoT']             = request.form['logoT']
    tournoi['stream']            = request.form['stream']
    tournoi['etatT']             = 1
    tournoi['idAdmin']           = 1
    update_tournoi(tournoi,id)
    return render_template("modifierTournoi.html")


@app.route("/connexion")
def connect():
    return render_template(
        "connexion.html")

@app.route("/voir_competitions_actives")
def voirCompetitionsActives():
    return render_template(
        "voirCompetitionsActives.html",tournois = get_All_Tournois_Actifs(),
        dicoAdmin = get_nom_prenom_by_tournoi(1)
        )

@app.route("/voir_competitions_terminees")
def voirCompetitionsTerminees():
    return render_template(
        "voirCompetitionsTerminees.html", tournois = get_All_Tournois_Terminees(),
        dicoAdmin = get_nom_prenom_by_tournoi(2)
        )

@app.route("/tableau_de_bord")
def tableauDeBord():
    return render_template(
        "tableauDeBord.html", tournois= get_All_Tournois_Admin())

@app.route("/tableau_de_bord/<int:tournoi>"    )
def tournoi(tournoi):
    return render_template(
        "tournoi.html", tournoi=get_Tournoi_by_id(tournoi))

@app.route("/tableau_de_bord/<int:tournoi>/matchs")
def voirMatchs(tournoi):
    return render_template(
        "voirMatchs.html", tournoi=get_Tournoi_by_id(tournoi))

@app.route("/tableau_de_bord/<int:tournoi>/stream")
def voirStream(tournoi):
    return render_template(
        "stream.html", tournoi=get_Tournoi_by_id(tournoi))

@app.route("/tableau_de_bord/<int:tournoi>/photos")
def voirPhotos(tournoi):
    return render_template(
        "photo.html", tournoi=get_Tournoi_by_id(tournoi), photos=get_All_Photos(tournoi)
    )

@app.route("/tableau_de_bord/<int:tournoi>/equipes")
def equipe(tournoi):
    return render_template(
        "equipe.html", tournoi=tournoi)

@app.route("/tableau_de_bord/<int:tournoi>/parametres")
def paramètre(tournoi):
    return render_template(
        "parametres.html", tournoi=tournoi)

@app.route("/listeAdmins")
def listeAdmins():
    return render_template(
    "listeAdmin.html", listeAdmins = get_All_Admins()
    )

@app.route("/voir_competitions_actives/<string:tournoi>/equipes/creer_equipe")
def creerEquipe(tournoi):
    return render_template(
    "creerEquipe.html", tailleEquipe = 24, tournoi=get_Tournoi_by_id(tournoi))
