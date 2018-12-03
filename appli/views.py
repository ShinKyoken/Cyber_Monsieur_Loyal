from .app import app
from .models import *
from flask import render_template, redirect, url_for

@app.route("/")
def home():
    return render_template(
        "home.html")

@app.route("/connexion")
def connect():
    return render_template(
        "connexion.html")
