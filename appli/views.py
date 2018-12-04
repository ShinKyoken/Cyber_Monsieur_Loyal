from .app import app
from .models import *
from flask import render_template, redirect, url_for

@app.route("/")
def home():
    return render_template(
        "home.html")



@app.route("/creerCompetition")
def creerCompetition():
    return render_template("creerCompetition.html")

@app.route("/connexion")
def connect():
    return render_template(
        "connexion.html")

@app.route("/voirCompetition")
def voirCompetition():
    return render_template(
        "voirCompetition.html")
