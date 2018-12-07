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

@app.route("/voir_competition")
def voirCompetition():
    return render_template(
        "voirCompetition.html")

@app.route("/tableau_de_bord")
def tableauDeBord():
    return render_template(
        "tableauDeBord.html", tournoi=["Pétanque","Concours informatique","Football"])

@app.route("/voir_competition/<string:tournoi>")
def tournoi(tournoi):
    return render_template(
        "tournoi.html", tournoi=tournoi)

@app.route("/voir_competition/<string:tournoi>/voir_les_matchs")
def voirMatchs(tournoi):
    return render_template(
        "voirMatchs.html", tournoi=tournoi)

@app.route("/voir_competition/<string:tournoi>/stream")
def voirStream(tournoi):
    return render_template(
        "stream.html", tournoi=tournoi)

@app.route("/voir_competition/<string:tournoi>/photos")
def voirPhotos(tournoi):
    return render_template(
        "photo.html", tournoi=tournoi)

@app.route("/voir_competition/<string:tournoi>/Equipes")
def equipe(tournoi):
    return render_template(
        "equipe.html", tournoi=tournoi)

@app.route("/voir_competition/<string:tournoi>/paramètres")
def paramètre(tournoi):
    return render_template(
        "paramètres.html", tournoi=tournoi)

@app.route("/voir_competition/<string:tournoi>/creer_equipe")
def creerEquipe(tournoi):
    return render_template(
        "creerEquipe.html", tournoi=tournoi, tailleEquipe=6)
