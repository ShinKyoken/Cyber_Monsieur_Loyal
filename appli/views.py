from .app import app
from .models import *
from flask import render_template, redirect, url_for, request
from flask_login import login_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, validators, PasswordField
from flask import request

class LoginForm(FlaskForm):
        username = StringField('Username')
        password = PasswordField('Password')

        def get_authenticated_user(self):
                user = ADMIN.query.get(self.nomAdmin.data)
                if user is None:
                    return None
                m = sha256()
                m.update(self.mdpAdmin.data.encode())
                passwd = m.hexdigest()
                return user if passwd == user.mdpAdmin else None


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
    tournoi['etatT']             = 0
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

@app.route("/voir_competitions_inactives")
def voirCompetitionsInactives():
    return render_template(
        "voirCompetitionsInactives.html",tournois = get_All_Tournois_Inactifs(),
        dicoAdmin = get_nom_prenom_by_tournoi(0),
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
        "voirMatchs.html", tournoi=get_Tournoi_by_id(tournoi), equipes=get_All_Equipes_Classe(tournoi))#, match_A_Venir=get_Match_A_Venir())

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
        "equipe.html", equipes=get_equipe_by_tournoi(tournoi), tournoi=get_Tournoi_by_id(tournoi))

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>")
def membres_equipe(tournoi, equipe):
    t = get_Tournoi_by_id(tournoi)
    return render_template(
        "membres_equipe.html", participants=get_participant_by_id_equipe(equipe), tournoi = t, equipe = equipe)

@app.route("/tableau_de_bord/<int:tournoi>/parametres")
def paramètre(tournoi):
    return render_template(
        "parametres.html", tournoi=tournoi)

@app.route("/listeAdmins")
def listeAdmins():
    return render_template(
    "listeAdmin.html", listeAdmins = get_All_Admins()
    )

@app.route("/tableau_de_bord/<int:tournoi>/equipes/creer_equipe")
def creerEquipe(tournoi):
    return render_template(
    "creerEquipe.html", tailleEquipe = 6, tournoi=get_Tournoi_by_id(tournoi))

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
        "equipe.html", equipes=get_equipe_by_tournoi(tournoi), tournoi=get_Tournoi_by_id(tournoi))

@app.route("/tableau_de_bord/<int:tournoi>/equipes/confirmer_equipe", methods={"POST"})
def confirmerEquipe(tournoi):
    t = get_Tournoi_by_id(tournoi)
    capitaine = {}
    capitaine['nomP'] = request.form['nom_capitaine']
    capitaine['prenomP'] = request.form['prenom_capitaine']
    capitaine['mailP'] = request.form['mail_capitaine']
    idChef = insert_participant(capitaine)

    equipe = {}
    equipe['nom_equipe']   = request.form['nom_equipe']
    equipe['capitaine']    = idChef
    equipe['idTournoi']    = t.idT
    equipe['tailleEquipe'] = int(request.form['nbParticipant'])+1
    idEquipe = insert_equipe(equipe)
    e = get_equipe_by_id(idEquipe)
    print(e)
    return redirect(url_for(
    "ajout_membre", tournoi = tournoi, equipe = idEquipe))

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>/ajout_membre")
def ajout_membre(tournoi, equipe):
    e = get_equipe_by_id(equipe)
    t = get_Tournoi_by_id(tournoi)
    return render_template(
        "ajoutMembre.html", equipe = e, tournoi = t)

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>/ajouter_membre", methods=("GET","POST",))
def ajouterMembre(tournoi, equipe):
    e = get_equipe_by_id(equipe)
    print(e.nbParticipant)
    for i in range(1, e.nbParticipant+1):
        participant = {}
        participant['nomP'] = request.form['nom_membre'+str(i)]
        participant['prenomP'] = request.form['prenom_membre'+str(i)]
        participant['mailP'] = request.form['mail_membre'+str(i)]
        p = insert_participant(participant)
        insert_constituer(equipe, p)

    return redirect(url_for("equipe",tournoi = tournoi))

@app.route("/tableau_de_bord/recherche/", methods=("POST",))
def rechercheTournois():
    a = request.form['search']
    print(a)
    return render_template(
        "tableauDeBord.html", tournois= getRechercheAllTournois(a), route="tableau")

@app.route("/voir_competitions_actives/recherche/", methods=("POST",))
def rechercheTournoisActif():
    a = request.form['search']
    print(a)
    return render_template(
        "voirCompetitionsActives.html",tournois = getRechercheTournoisActif(a),
        dicoAdmin = get_nom_prenom_by_tournoi(1),
        route="voirCompet"
        )

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>/delete")
def delete_equipe(tournoi, equipe):
    t = get_Tournoi_by_id(tournoi)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for("auteur"))
