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
        dicoAdmin = get_nom_prenom_by_tournoi(1),
        route="voirCompet"
        )

@app.route("/voir_competitions_terminees")
def voirCompetitionsTerminees():
    return render_template(
        "voirCompetitionsTerminees.html", tournois = get_All_Tournois_Terminees(),
        dicoAdmin = get_nom_prenom_by_tournoi(2),
        route="voirCompet"
        )

@app.route("/voir_competition/<int:tournoi>")
def voirCompet(tournoi):
    return render_template(
        "tournoi.html", tournoi=get_Tournoi_by_id(tournoi)
        , route="voirCompet")

@app.route("/tableau_de_bord")
def tableauDeBord():
    return render_template(
        "tableauDeBord.html", tournois= get_All_Tournois_Admin(), route="tableau")

@app.route("/tableau_de_bord/<int:tournoi>"    )
def tournoi(tournoi):
    return render_template(
        "tournoi.html", tournoi=get_Tournoi_by_id(tournoi)
        , route="tableau")

@app.route("/tableau_de_bord/<int:tournoi>/matchs")
def voirMatchs(tournoi):
    return render_template(
        "voirMatchs.html", tournoi=get_Tournoi_by_id(tournoi))#, equipes=get_All_Equipes_Classe(), match_A_Venir=get_Match_A_Venir())

@app.route("/tableau_de_bord/<int:tournoi>/stream")
def voirStream(tournoi):
    return render_template(
        "stream.html", tournoi=get_Tournoi_by_id(tournoi)
        , route="tableau")

@app.route("/tableau_de_bord/<int:tournoi>/photos")
def voirPhotos(tournoi):
    return render_template(
        "photo.html", tournoi=get_Tournoi_by_id(tournoi), photos=get_All_Photos(tournoi)
        , route="tableau"
    )

@app.route("/tableau_de_bord/<int:tournoi>/equipes")
def equipe(tournoi):
    return render_template(
        "equipe.html", equipes=get_All_Equipes(tournoi)
        , route="tableau")

@app.route("/tableau_de_bord/<int:tournoi>/parametres")
def paramètre(tournoi):
    return render_template(
        "parametres.html", tournoi=tournoi)

@app.route("/listeAdmins")
def listeAdmins():
    return render_template(
    "listeAdmin.html", listeAdmins = get_All_Admins()
    )

@app.route("/tableau_de_bord/<string:tournoi>/equipes/creer_equipe")
def creerEquipe(tournoi):
    return render_template(
    "creerEquipe.html", tailleEquipe = 3, tournoi=get_Tournoi_by_id(tournoi))

@app.route("/voir_competition/<int:tournoi>/matchs")
def voirCompet_Matchs(tournoi):
    return render_template(
        "voirMatchs.html", tournoi=get_Tournoi_by_id(tournoi)
        , route="voirCompet")

@app.route("/voir_competition/<int:tournoi>/stream")
def voirCompet_Stream(tournoi):
    return render_template(
        "stream.html", tournoi=get_Tournoi_by_id(tournoi)
        , route="voirCompet")

@app.route("/voir_competition/<int:tournoi>/photos")
def voirCompet_Photos(tournoi):
    return render_template(
        "photo.html", tournoi=get_Tournoi_by_id(tournoi), photos=get_All_Photos(tournoi)
        , route="voirCompet"
    )

@app.route("/voir_competition/<int:tournoi>/equipes")
def voirCompet_equipe(tournoi):
    return render_template(
        "equipe.html", equipes=get_All_Equipes(tournoi)
        , route="voirCompet")

@app.route("/tableau_de_bord/<string:tournoi>/equipes/confirmer_equipe", methods={"POST"})
def confirmerEquipe(tournoi):
  capitaine = {}
  capitaine['nomP'] = request.form['nom_capitaine']
  capitaine['prenomP'] = request.form['prenom_capitaine']
  capitaine['mailP'] = request.form['mail_capitaine']
  insert_participant(capitaine)
  for i in range(1, 3):
      participant = {}
      participant['nomP'] = request.form['nom_membre'+str(i)]
      participant['prenomP'] = request.form['prenom_membre'+str(i)]
      participant['mailP'] = request.form['mail_membre'+str(i)]
      insert_participant(participant)
  return render_template(
  "equipe.html")
