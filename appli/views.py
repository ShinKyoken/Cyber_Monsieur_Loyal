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


@app.route("/connexion")
def connect():
    return render_template(
        "connexion.html")

@app.route("/voir_competitions_actives")
def voirCompetitionsActives():
    return render_template(
        "voirCompetitionsActives.html",tournois = get_All_Tournois_Actifs(),
        dicoAdmin = get_nom_prenom_tournois_actifs()
        )

@app.route("/voir_competitions_terminees")
def voirCompetitionsTerminees():
    return render_template(
        "voirCompetitionsTerminees.html", tournois = get_All_Tournois_Terminees(),
        dicoAdmin = get_nom_prenom_tournois_terminees()
        )

@app.route("/tableau_de_bord")
def tableauDeBord():
    return render_template(
        "tableauDeBord.html", tournoi= get_All_Tournois_Admin())

@app.route("/voir_competitions_actives/<int:tournoi>")
@app.route("/voir_competitions_terminees/<int:tournoi>")
def tournoi(tournoi):
    return render_template(
        "tournoi.html", tournoi=tournoi)

@app.route("/voir_competitions_actives/<int:tournoi>/voir_les_matchs")
@app.route("/voir_competitions_terminees/<int:tournoi>/voir_les_matchs")
def voirMatchs(tournoi):
    return render_template(
        "voirMatchs.html", tournoi=tournoi)

@app.route("/voir_competitions_actives/<int:tournoi>/stream")
@app.route("/voir_competitions_terminees/<int:tournoi>/stream")
def voirStream(tournoi):
    return render_template(
        "stream.html", tournoi=tournoi)

@app.route("/voir_competitions_actives/<int:tournoi>/photos")
@app.route("/voir_competitions_terminees/<int:tournoi>/photos")
def voirPhotos(tournoi):
    return render_template(
        "photo.html", tournoi=tournoi, photos=[{"img":"https://parismatch.be/app/uploads/2018/04/Macaca_nigra_self-portrait_large-e1524567086123-1100x715.jpg", "desc":"une image d'un singe content"},
        {"img":"https://helpx.adobe.com/content/dam/help/en/stock/how-to/visual-reverse-image-search/_jcr_content/main-pars/image/visual-reverse-image-search-v2_1000x560.jpg", "desc":"une image d'un papillon"}]
    )

@app.route("/voir_competitions_actives/<int:tournoi>/Equipes")
@app.route("/voir_competitions_terminees/<int:tournoi>/Equipes")
def equipe(tournoi):
    return render_template(
        "equipe.html", tournoi=tournoi)

@app.route("/voir_competitions_actives/<int:tournoi>/paramètres")
@app.route("/voir_competitions_terminees/<int:tournoi>/paramètres")
def paramètre(tournoi):
    return render_template(
        "paramètres.html", tournoi=tournoi)

@app.route("/listeAdmins")
def listeAdmins():
    return render_template(
    "listeAdmin.html", listeAdmins = get_All_Admins()
    )
