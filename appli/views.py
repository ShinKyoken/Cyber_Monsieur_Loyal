from .app import app
from .models import *
from flask import render_template, redirect, url_for

@app.route("/")
def home():
    return render_template(
        "home.html")


@app.route("/creer_competition")
def creerCompetition():
    return render_template("creerCompetition.html")

@app.route("/confirmer_tournoi")
def confirmer_tournoi():
    return render_template("confirmerTournoi.html")

@app.route("/connexion")
def connect():
    return render_template(
        "connexion.html")

@app.route("/voir_competitions_actives")
def voirCompetitionsActives():
    return render_template(
        "voirCompetitionsActives.html",tournois = get_All_Tournois_Actifs())

@app.route("/voir_competitions_terminees")
def voirCompetitionsTerminees():
    return render_template(
        "voirCompetitionsTerminees.html",tournois = get_All_Tournois_Terminees())

@app.route("/tableau_de_bord")
def tableauDeBord():
    return render_template(
        "tableauDeBord.html", tournoi=["Pétanque","Concours informatique","Football"])

@app.route("/voir_competitions_actives/<string:tournoi>")
@app.route("/voir_competitions_terminees/<string:tournoi>")
def tournoi(tournoi):
    return render_template(
        "tournoi.html", tournoi=tournoi)

@app.route("/voir_competitions_actives/<string:tournoi>/voir_les_matchs")
@app.route("/voir_competitions_terminees/<string:tournoi>/voir_les_matchs")
def voirMatchs(tournoi):
    return render_template(
        "voirMatchs.html", tournoi=tournoi)

@app.route("/voir_competitions_actives/<string:tournoi>/stream")
@app.route("/voir_competitions_terminees/<string:tournoi>/stream")
def voirStream(tournoi):
    return render_template(
        "stream.html", tournoi=tournoi)

@app.route("/voir_competitions_actives/<string:tournoi>/photos")
@app.route("/voir_competitions_terminees/<string:tournoi>/photos")
def voirPhotos(tournoi):
    return render_template(
        "photo.html", tournoi=tournoi, photos=[{"img":"https://parismatch.be/app/uploads/2018/04/Macaca_nigra_self-portrait_large-e1524567086123-1100x715.jpg", "desc":"une image d'un singe content"},
        {"img":"https://helpx.adobe.com/content/dam/help/en/stock/how-to/visual-reverse-image-search/_jcr_content/main-pars/image/visual-reverse-image-search-v2_1000x560.jpg", "desc":"une image d'un papillon"}]
    )

@app.route("/voir_competitions_actives/<string:tournoi>/Equipes")
@app.route("/voir_competitions_terminees/<string:tournoi>/Equipes")
def equipe(tournoi):
    return render_template(
        "equipe.html", tournoi=tournoi)

@app.route("/voir_competitions_actives/<string:tournoi>/paramètres")
@app.route("/voir_competitions_terminees/<string:tournoi>/paramètres")
def paramètre(tournoi):
    return render_template(
        "paramètres.html", tournoi=tournoi)

@app.route("/listeAdmins")
def listeAdmins():
    return render_template(
    "listeAdmin.html", listeAdmins = get_All_Admins()
    )
