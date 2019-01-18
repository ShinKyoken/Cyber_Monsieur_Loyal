from .app import app
from .models import *
from flask import render_template, redirect, url_for, request, send_file, make_response
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, validators, PasswordField
from hashlib import sha256
from io import BytesIO
import io
from PIL import Image
import base64

class LoginForm(FlaskForm):
        username = StringField('Username')
        password = PasswordField('Password')
        next = HiddenField()

        def get_authenticated_user(self):

            """
            param:

            return: (a remplire)
            """
            user = ADMIN.query.filter_by(nomAdmin = self.username.data).first()
            if user is None :
                return None
            m = sha256()
            m.update(self.password.data.encode())
            passwd = m.hexdigest()
            if passwd == user.mdpAdmin or self.password.data == user.mdpAdmin:
                return user
                return None




@app.route("/")
def home():
    """
    Redirige vers l'accueil du site.
    """
    return render_template(
        "home.html")

@app.route("/tableau_de_bord/<int:idTournoi>/download_regles")
def download_regles(idTournoi):
    """
    param: idTournoi (int), l'identifiant d'un tournoi.

    Permet de telecharger les rêgles d'un tournoi.
    """
    regle = get_Regle_by_id(idTournoi)
    return send_file(BytesIO(regle.data), attachment_filename=regle.nomFic, as_attachment=True)

@app.route("/connexion",methods=["GET","POST"])
def connect():
    """
    Connecte un utilisateur, en le redirigant vers l'accueil du site si la connection est effectué.
    """
    form = LoginForm()
    if (not form.is_submitted()) :
        form.next.data = request.args.get("next")
    elif form.validate_on_submit():
        user = form.get_authenticated_user()
        if user :
            login_user(user)
            next = form.next.data or url_for("home")
            return redirect(next)
    return render_template(
        "connexion.html",form = form)

@app.route("/logout/")
@login_required
def logout():
    """
    Déconnecte l'utilisateur et redirige vers l'accueil du site.
    """
    logout_user()
    return redirect(url_for('home'))

@app.route("/inscription",methods=["GET","POST"])
def inscription():
    form = LoginForm()
    return render_template("inscription.html", form = form)

@app.route("/confirmer_inscription",methods=["GET","POST"])
def confirmer_ajout_admin():
    f = LoginForm()
    if f.validate_on_submit():
        m = sha256()
        m.update(f.password.data.encode())
        passwd = m.hexdigest()
        newAdmin = ADMIN(nomAdmin = f.username.data, prenomAdmin = "Michel", dateNaissAdmin = "12/12/1999", mdpAdmin = passwd)
        db.session.add(newAdmin)
        db.session.commit()
        return redirect(url_for("connect"))
    return render_template(
        "inscription.html",form = f)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('connect'))


@app.route("/creer_competition")
@login_required
def creerCompetition():
    """
    Redirige vers la page de création de competition.
    """
    return render_template("creerCompetition.html")

@app.route("/tableau_de_bord/<int:tournoi>/lancer_tournoi/test",methods={"POST"})
@login_required
def test(tournoi):
    """
    (Nom à changer)
    param: tournoi (int), identifiant d'un tournoi.

     Génère les matchs D'un tournoi passé en paramètre
    """
    automatique_match(tournoi,int(request.form['nbMatchs']),int(request.form['nbEquipe']))
    return render_template("letest.html")

@app.route("/confirmer_competition", methods={"POST"})
@login_required
def confirmerTournoi():
    """
    Crée un tournoi et l'ajoute dans la BD.
    """
    tournoi = {}
    tournoi['intituleT']         = request.form['intituleT']
    tournoi['reglement']         = request.files['reglement']
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
    """
    param:id (int), identifiant d'un tournoi

    Modifie un tournoi dans la BD.
    """
    tournoi = {}
    tournoi['intituleT']         = request.form['intituleT']
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

    regle            = {}
    regle['nomFic']  = request.files['reglement'].filename
    regle['data']    = request.files['reglement'].read()

    update_tournoi(tournoi, id)
    update_regle(regle, id)

    return redirect(url_for("tournoi", tournoi = id))



@app.route("/voir_competitions_actives")
def voirCompetitionsActives():
    """
    Redirige vers la page des competitions actives.
    """
    return render_template(
        "voirCompetitionsActives.html",tournois = get_All_Tournois_Actifs(),
        dicoAdmin = get_nom_prenom_by_tournoi(1),
        route="voirCompet")

@app.route("/voir_competitions_inactives")
def voirCompetitionsInactives():
    """
    Redirige vers la page des competitions inactives.
    """
    return render_template(
        "voirCompetitionsInactives.html",tournois = get_All_Tournois_Inactifs(),
        dicoAdmin = get_nom_prenom_by_tournoi(0),
        route="voirCompet")

@app.route("/voir_competitions_terminees")
def voirCompetitionsTerminees():
    """
    Redirige vers la page des competitions terminé.
    """
    return render_template(
        "voirCompetitionsTerminees.html", tournois = get_All_Tournois_Terminees(),
        dicoAdmin = get_nom_prenom_by_tournoi(2),
        route="voirCompet")

@app.route("/voir_competition/<int:tournoi>")
def voirCompet(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers la page d'un tournoi dont l'utilisateur est l'administrateur
    """
    return render_template(
        "tournoi.html",
        tournoi=get_Tournoi_by_id(tournoi),
        admin = get_admin_by_id(tournoi),
        route="voirCompet")

@app.route("/tableau_de_bord")
@login_required
def tableauDeBord():
    """
    Redirige vers le tableau de bord d'un administrateur connecté
    """
    return render_template(
        "tableauDeBord.html",
        tournois= get_All_Tournois_Admin(),
        route="tableau")

@app.route("/tableau_de_bord/<int:id>")
@login_required
def tournoi(id):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers la page d'un tournoi pour un utilisateur non connecté
    """
    return render_template(
        "tournoi.html",
        tournoi=get_Tournoi_by_id(id),
        admin=get_admin_by_id(id),
        route="tableau")

@app.route("/tableau_de_bord/<int:tournoi>/matchs")
@login_required
def voirMatchs(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page affichant les differant matchs du tounoi ainsi qu'un classement.
    """
    return render_template(
        "voirMatchs.html",
        equipes = get_All_Equipes_Classe(tournoi),
        equipes2 = get_All_Equipe_by_partie(get_All_partie_by_tournoi(tournoi)))

@app.route("/tableau_de_bord/<int:tournoi>/stream")
@login_required
def voirStream(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page affichant le stream du tournoi.
    """
    return render_template(
        "stream.html",
        tournoi=get_Tournoi_by_id(tournoi),
        route="tableau")

@app.route("/tableau_de_bord/<int:tournoi>/photos")
@login_required
def voirPhotos(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page affichant les photo du tournoi
    """
    photos = get_All_Photos(tournoi)
    listeImages = []
    for photo in photos:
        image = base64.b64decode(photo.Photo)
        listeImages.append(image)
    return render_template(
        "photo.html",
        tournoi=get_Tournoi_by_id(tournoi),
        photos=get_All_Photos(tournoi),
        images = listeImages,
        route="tableau")

@app.route("/tableau_de_bord/<int:tournoi>/equipes")
@login_required
def equipe(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page affichant les differantes équipes du tounoi
    """
    dico = {}
    equipes = get_equipe_by_tournoi(tournoi)
    for equipe in equipes:
        dico[equipe.idE] = get_participant_by_id_equipe(equipe.idE)

    return render_template(
        "equipe.html",
        equipes = equipes,
        tournoi = get_Tournoi_by_id(tournoi),
        participants = dico)


@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>")
@login_required
def membres_equipe(tournoi, equipe):
    """
    param: tournoi (int), identifiant d'un tournoi.
           equipe (int), identifiant d'une équipe.

    Redirige vers une page affichant les differants membres d'une équipe d'un tournoi
    """
    t = get_Tournoi_by_id(tournoi)
    return render_template(
        "membres_equipe.html",
        participants=get_participant_by_id_equipe(equipe),
        tournoi = t,
        equipe = equipe)

@app.route("/tableau_de_bord/<int:tournoi>/parametres")
@login_required
def paramètre(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page pour modifier un tournoi
    """
    t = get_Tournoi_by_id(tournoi)
    regles = get_Regle_by_id(tournoi)
    return render_template(
        "parametres.html", tournoi=t, regles = regles)

@app.route("/tableau_de_bord/<int:tournoi>/lancer_tournoi")
@login_required
def lancerCompet(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page pour modifier un tournoi
    """
    return render_template(
        "creation_matchs.html",
        tournoi = get_Tournoi_by_id(tournoi))

@app.route("/listeAdmins")
@login_required
def listeAdmins():
    """
    Redirige vers une page qui montre les administrateurs du site
    """
    return render_template(
    "listeAdmin.html",
    listeAdmins = get_All_Admins())

@app.route("/tableau_de_bord/<int:tournoi>/equipes/creer_equipe")
@login_required
def creerEquipe(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers la page de création d'équipe
    """
    return render_template(
    "creerEquipe.html",
    tailleEquipe = 3,
    tournoi=get_Tournoi_by_id(tournoi))

@app.route("/voir_competition/<int:tournoi>/matchs")
def voirCompet_Matchs(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page affichant les differant matchs du tounoi ainsi qu'un classement.
    """
    return render_template(
        "voirMatchs.html",
        tournoi=get_Tournoi_by_id(tournoi),
        route="voirCompet")

@app.route("/voir_competition/<int:tournoi>/stream")
def voirCompet_Stream(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page affichant le stream du tournoi.
    """
    return render_template(
        "stream.html",
        tournoi=get_Tournoi_by_id(tournoi),
        route="voirCompet")

@app.route("/voir_competition/<int:tournoi>/photos")
def voirCompet_Photos(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page affichant les photo du tournoi
    """
    return render_template(
        "photo.html",
        tournoi=get_Tournoi_by_id(tournoi),
        photos=get_All_Photos(tournoi),
        route="voirCompet")

@app.route("/voir_competition/<int:tournoi>/equipes")
def voirCompet_equipe(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page affichant les differantes équipes du tounoi
    """
    return render_template(
        "equipe.html",
        equipes=get_equipe_by_tournoi(tournoi),
        tournoi=get_Tournoi_by_id(tournoi))

@app.route("/tableau_de_bord/<int:tournoi>/equipes/confirmer_equipe", methods={"POST"})
@login_required
def confirmerEquipe(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Ajoute une équipe dans la BD.
    """
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
    """
    param: tournoi (int), identifiant d'un tournoi.
           equipe (int), identifiant d'une équipe.

    redirige vers la page d'ajout de membre
    """
    e = get_equipe_by_id(equipe)
    t = get_Tournoi_by_id(tournoi)
    c = get_chef_by_id_equipe(equipe)
    print(c.nomP)
    return render_template(
        "ajoutMembre.html", equipe = e, tournoi = t, chef = c)

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>/ajouter_membre", methods=("GET","POST",))
@login_required
def ajouterMembre(tournoi, equipe):
    """
    param: tournoi (int), identifiant d'un tournoi.
           equipe (int), identifiant d'une équipe.

    Ajoute des membre a une équipe dans la BD
    """
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

    """
    param: tournoi (int), identifiant d'un tournoi.
           equipe (int), identifiant d'une équipe.

    Modifie une équipe dans la BD
    """

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
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers la page d'ajout de photo
    """
    return render_template(
        "ajouterPhoto.html", tournoi= get_Tournoi_by_id(tournoi))

@app.route("/tableau_de_bord/recherche/", methods=("POST",))
@login_required
def rechercheTournois():
    """
    Redirige vers la page d'ajout de photo
    """
    a = request.form['search']
    print(a)
    return render_template(
        "tableauDeBord.html", tournois= getRechercheAllTournois(a), route="tableau")

@app.route("/voir_competitions_actives/recherche/", methods=("POST",))
def rechercheTournoisActif():
    """
    Redirige vers la page de recherche de competition active
    """
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
    """
    Redirige vers la page de recherche de competition inactive
    """
    a = request.form['search']
    print(a)
    return render_template(
        "voirCompetitionsInactives.html",
        tournois = getRechercheTournoisInactif(a),
        dicoAdmin = get_nom_prenom_by_tournoi(0),
        route="voirCompet")

@app.route("/voir_competitions_terminees/recherche/", methods=("POST",))
def rechercheTournoisTerminee():
    """
    Redirige vers la page de recherche de competition terminé
    """
    a = request.form['search']
    print(a)
    return render_template(
        "voirCompetitionsTerminees.html",
        tournois = getRechercheTournoisTerminee(a),
        dicoAdmin = get_nom_prenom_by_tournoi(2),
        route="voirCompet"
        )

@app.route("/supprimer_equipe/<int:tournoi>/<int:equipe>")
@login_required
def supprime_equipe(equipe,tournoi):
    """
    param: equipe (int), identifiant d'une équipe.

    supprime une equipe dans la BD
    """
    delete_equipe(equipe)
    return redirect(url_for("equipe",tournoi=tournoi))

@app.route("/tableau_de_bord/<int:tournoi>/confirmer_photo", methods={"POST"})
@login_required
def confirmerPhoto(tournoi):
    """
    Crée une photo et l'ajoute dans la BD.
    """
    photo = {}
    photo['idT']               = tournoi
    photo['Photo']             = request.files['mon_fichier'].read()
    photo['descPhoto']         = request.form['description']
    photo['titrePhoto']        = request.form['titre']

    insert_photo(photo)
    return redirect(url_for("voirPhotos",tournoi=tournoi))
