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

@app.route("/voir_competition/test")
def tournoi():
    return render_template(
        "tournoi.html", tournoi="Pétanque")