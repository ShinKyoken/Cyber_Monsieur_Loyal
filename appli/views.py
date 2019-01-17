from .app import app
from .models import *
from flask import render_template, redirect, url_for, request, send_file
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, validators, PasswordField
from flask import request
from hashlib import sha256
from io import BytesIO

class LoginForm(FlaskForm):
        username = StringField('Username')
        password = PasswordField('Password')
        next = HiddenField()

        def get_authenticated_user(self):
                print('\n '+ str(self.username.data) + ' ' + str(self.password.data)+'\n\n')
                user = ADMIN.query.filter_by(nomAdmin = self.username.data).first()
                print(user.mdpAdmin)
                if user is None :
                    return None
                # Décomenter en-dessous dès que le mdp est cripté dans la bd

                # m = sha256()
                # m.update(self.password.data.encode())
                # passwd = m.hexdigest()
                if self.password.data == user.mdpAdmin :
                    print("azazeazeazeazeazea")
                    return user
                return None


@app.route("/")
def home():
    return render_template(
        "home.html")

@app.route("/tableau_de_bord/<int:idTournoi>/download_regles")
def download_regles(idTournoi):
    tournoi = TOURNOI.query.filter_by(idT = idTournoi).first()
    return send_file(BytesIO(tournoi.regleT), attachment_filename='regles.pdf', as_attachment=True)

@app.route("/connexion",methods=["GET","POST"])
def connect():
    form = LoginForm()
    if (not form.is_submitted()) :
        form.next.data = request.args.get("next")
    elif form.validate_on_submit():
        user = form.get_authenticated_user()
        if user :
            login_user(user)
            print(current_user.is_authenticated)
            print(current_user.nomAdmin)
            next = form.next.data or url_for("home")
            return redirect(next)
    return render_template(
        "connexion.html",form = form)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/creer_competition")
@login_required
def creerCompetition():
    return render_template("creerCompetition.html")

@app.route("/tableau_de_bord/<int:tournoi>/lancer_tournoi/test",methods={"POST"})
@login_required
def test(tournoi):
    automatique_match(tournoi,int(request.form['nbMatchs']),int(request.form['nbEquipe']))
    return render_template("letest.html")

@app.route("/confirmer_competition", methods={"POST"})
@login_required
def confirmerTournoi():
    tournoi = {}
    tournoi['intituleT']         = request.form['intituleT']
    tournoi['regleT']            = request.files['regleT']
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
    tournoi['idAdmin']           = current_user.idAdmin
    insert_tournoi(tournoi)
    return render_template("confirmerTournoi.html")

@app.route("/tableau_de_bord/<int:id>/modifier_competition", methods={"POST"})
@login_required
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
    tournoi['etatT']             = 0
    tournoi['idAdmin']           = current_user.idAdmin
    update_tournoi(tournoi,id)
    return render_template("modifierTournoi.html")


@app.route("/voir_competitions_actives")
def voirCompetitionsActives():
    return render_template(
        "voirCompetitionsActives.html",tournois = get_All_Tournois_Actifs(),
        dicoAdmin = get_nom_prenom_by_tournoi(1),
        route="voirCompet")

@app.route("/voir_competitions_inactives")
def voirCompetitionsInactives():
    return render_template(
        "voirCompetitionsInactives.html",tournois = get_All_Tournois_Inactifs(),
        dicoAdmin = get_nom_prenom_by_tournoi(0),
        route="voirCompet")

@app.route("/voir_competitions_terminees")
def voirCompetitionsTerminees():
    return render_template(
        "voirCompetitionsTerminees.html", tournois = get_All_Tournois_Terminees(),
        dicoAdmin = get_nom_prenom_by_tournoi(2),
        route="voirCompet")

@app.route("/voir_competition/<int:tournoi>")
def voirCompet(tournoi):
    return render_template(
        "tournoi.html",
        tournoi=get_Tournoi_by_id(tournoi),
        route="voirCompet")

@app.route("/tableau_de_bord")
@login_required
def tableauDeBord():
    return render_template(
        "tableauDeBord.html",
        tournois= get_All_Tournois_Admin(),
        route="tableau")

@app.route("/tableau_de_bord/<int:tournoi>")
@login_required
def tournoi(tournoi):
    return render_template(
        "tournoi.html",
        tournoi=get_Tournoi_by_id(tournoi),
        route="tableau")

@app.route("/tableau_de_bord/<int:tournoi>/matchs")
@login_required
def voirMatchs(tournoi):
    return render_template(
        "voirMatchs.html",
        equipes = get_All_Equipes_Classe(tournoi),
        equipes2 = get_All_Equipe_by_partie(get_All_partie_by_tournoi(tournoi)))

@app.route("/tableau_de_bord/<int:tournoi>/stream")
@login_required
def voirStream(tournoi):
    return render_template(
        "stream.html",
        tournoi=get_Tournoi_by_id(tournoi),
        route="tableau")

@app.route("/tableau_de_bord/<int:tournoi>/photos")
@login_required
def voirPhotos(tournoi):
    return render_template(
        "photo.html",
        tournoi=get_Tournoi_by_id(tournoi),
        photos=get_All_Photos(tournoi),
        route="tableau")

@app.route("/tableau_de_bord/<int:tournoi>/equipes")
@login_required
def equipe(tournoi):
    return render_template(
        "equipe.html",
        equipes=get_equipe_by_tournoi(tournoi),
        tournoi=get_Tournoi_by_id(tournoi))

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>")
@login_required
def membres_equipe(tournoi, equipe):
    t = get_Tournoi_by_id(tournoi)
    return render_template(
        "membres_equipe.html",
        participants=get_participant_by_id_equipe(equipe),
        tournoi = t,
        equipe = equipe)

@app.route("/tableau_de_bord/<int:tournoi>/parametres")
@login_required
def paramètre(tournoi):
    t = get_Tournoi_by_id(tournoi)
    return render_template(
        "parametres.html", tournoi=t)

@app.route("/tableau_de_bord/<int:tournoi>/lancer_tournoi")
@login_required
def lancerCompet(tournoi):
    return render_template(
        "creation_matchs.html",
        tournoi = get_Tournoi_by_id(tournoi))

@app.route("/listeAdmins")
@login_required
def listeAdmins():
    return render_template(
    "listeAdmin.html",
    listeAdmins = get_All_Admins())

@app.route("/tableau_de_bord/<int:tournoi>/equipes/creer_equipe")
@login_required
def creerEquipe(tournoi):
    return render_template(
    "creerEquipe.html",
    tailleEquipe = 3,
    tournoi=get_Tournoi_by_id(tournoi))

@app.route("/voir_competition/<int:tournoi>/matchs")
def voirCompet_Matchs(tournoi):
    return render_template(
        "voirMatchs.html",
        tournoi=get_Tournoi_by_id(tournoi),
        route="voirCompet")

@app.route("/voir_competition/<int:tournoi>/stream")
def voirCompet_Stream(tournoi):
    return render_template(
        "stream.html",
        tournoi=get_Tournoi_by_id(tournoi),
        route="voirCompet")

@app.route("/voir_competition/<int:tournoi>/photos")
def voirCompet_Photos(tournoi):
    return render_template(
        "photo.html",
        tournoi=get_Tournoi_by_id(tournoi),
        photos=get_All_Photos(tournoi),
        route="voirCompet")

@app.route("/voir_competition/<int:tournoi>/equipes")
def voirCompet_equipe(tournoi):
    return render_template(
        "equipe.html",
        equipes=get_equipe_by_tournoi(tournoi),
        tournoi=get_Tournoi_by_id(tournoi))

@app.route("/tableau_de_bord/<int:tournoi>/equipes/confirmer_equipe", methods={"POST"})
@login_required
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
    insert_constituer(idEquipe, idChef)
    return redirect(url_for(
    "ajout_membre", tournoi = tournoi, equipe = idEquipe))

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>/ajout_membre")
@login_required
def ajout_membre(tournoi, equipe):
    e = get_equipe_by_id(equipe)
    t = get_Tournoi_by_id(tournoi)
    c = get_chef_by_id_equipe(equipe)
    print(c.nomP)
    return render_template(
        "ajoutMembre.html", equipe = e, tournoi = t, chef = c)

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>/ajouter_membre", methods=("GET","POST",))
@login_required
def ajouterMembre(tournoi, equipe):
    e = get_equipe_by_id(equipe)
    print(e.nbParticipant)
    for i in range(1, e.nbParticipant):
        participant = {}
        participant['nomP'] = request.form['nom_membre'+str(i)]
        participant['prenomP'] = request.form['prenom_membre'+str(i)]
        participant['mailP'] = request.form['mail_membre'+str(i)]
        p = insert_participant(participant)
        insert_constituer(equipe, p)
    return redirect(url_for("equipe",tournoi = tournoi))

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>/modifier_equipe", methods=("GET","POST",))
@login_required
def modifierEquipe(tournoi, equipe):
    e = get_equipe_by_id(equipe)
    t = get_Tournoi_by_id(tournoi)
    liste = get_membres_constituer(equipe)
    l = []
    for part in liste:
        l.append(get_participant_by_id(part.idP))
    c = get_chef_by_id_equipe(equipe)
    return render_template(
        "modifier_membres.html", tournoi = t, equipe = e, liste_membres = l)

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>/valider_modification_equipe", methods={"POST"})
def valider_modification_equipe(tournoi, equipe):
    e = get_equipe_by_id(equipe)
    l = get_membres_constituer(equipe)
    t = get_Tournoi_by_id(tournoi)
    for i in range(len(l)):
        dico_participant = {}
        dico_participant['nomP'] = request.form['nom_membre'+str(i)]
        dico_participant['prenomP'] = request.form['prenom_membre'+str(i)]
        dico_participant['mailP'] = request.form['mail_membre'+str(i)]
        update_participant(dico_participant, l[i].idP)
    return redirect(url_for("membres_equipe", tournoi = tournoi, equipe = equipe))

@app.route("/tableau_de_bord/<int:tournoi>/ajouter_photo", methods={"GET","POST",})
@login_required
def ajouterPhoto(tournoi):
    return render_template(
        "ajouterPhoto.html", tournoi= get_Tournoi_by_id(tournoi))

@app.route("/tableau_de_bord/recherche/", methods=("POST",))
@login_required
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
        "voirCompetitionsActives.html",
        tournois = getRechercheTournoisActif(a),
        dicoAdmin = get_nom_prenom_by_tournoi(1),
        route="voirCompet"
        )

@app.route("/voir_competitions_inactives/recherche/", methods=("POST",))
def rechercheTournoisInactif():
    a = request.form['search']
    print(a)
    return render_template(
        "voirCompetitionsInactives.html",
        tournois = getRechercheTournoisInactif(a),
        dicoAdmin = get_nom_prenom_by_tournoi(0),
        route="voirCompet")

@app.route("/voir_competitions_terminees/recherche/", methods=("POST",))
def rechercheTournoisTerminee():
    a = request.form['search']
    print(a)
    return render_template(
        "voirCompetitionsTerminees.html",
        tournois = getRechercheTournoisTerminee(a),
        dicoAdmin = get_nom_prenom_by_tournoi(2),
        route="voirCompet"
        )

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>/delete")
@login_required
def delete_equipe(tournoi, equipe):
    t = get_Tournoi_by_id(tournoi)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for("auteur"))
