from .config import *

@app.route("/tableau_de_bord")
@login_required
def tableauDeBord():
    """
    Redirige vers le tableau de bord de l'utilisateur. Il doit être connecté.
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

    Redirige vers la page d'un tournoi pour un utilisateur connecté.
    """
    return render_template(
        "newTournoi.html",
        tournoi=get_Tournoi_by_id(id),
	    nbEquipe=count_equipe_by_tournoi(id),
        admin=get_admin_by_id(id),
        nbPartieTerminee=len(get_All_Parties_Terminees(id)),
        route="tableau")

@app.route("/tableau_de_bord/<int:tournoi>/matchs")
@login_required
def voirMatchs(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page affichant les different matchs du tournoi ainsi qu'un classement.
    L'utilisateur doit être connecté pour pouvoir y accéder.
    """
    return render_template(
        "voirMatchs.html",
        listeMaps = get_All_Maps(tournoi),
        tournoi = get_Tournoi_by_id(tournoi),
        equipes = get_All_Equipes_Classe(tournoi),
        equipes2 = get_All_Equipe_by_partie(get_All_partie_by_tournoi(tournoi)),
        partiesFinies = get_All_Parties_Terminees(tournoi),
        route="tableau"
        )

@app.route("/tableau_de_bord/<int:tournoi>/stream")
@login_required
def voirStream(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page affichant le stream du tournoi.
    L'utilisateur doit être connecté pour pouvoir y accéder.
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

    Redirige vers une page affichant les photo du tournoi.
    L'utilisateur doit être connecté pour pouvoir y accéder.
    """
    return render_template(
        "photo.html",
        tournoi=get_Tournoi_by_id(tournoi),
        photos=get_All_Photos(tournoi),
        route="tableau")

@app.route("/tableau_de_bord/<int:tournoi>/equipes")
@login_required
def equipe(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page affichant les differentes équipes du tounoi.
    L'utilisateur doit être connecté pour pouvoir y accéder.
    """
    dico = {}
    equipes = get_equipe_by_tournoi(tournoi)
    for equipe in equipes:
        dico[equipe.idE] = get_participant_by_id_equipe(equipe.idE)

    return render_template(
        "equipe.html",
        equipes = equipes,
        tournoi = get_Tournoi_by_id(tournoi),
        nbEquipe=count_equipe_by_tournoi(tournoi),
        route = "tableau",
        participants = dico)

@app.route("/tableau_de_bord/<int:tournoi>/parametres")
@login_required
def parametre(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page qui permet de modifier un tournoi.
    L'utilisateur doit être connecté pour pouvoir y accéder.
    """
    t = get_Tournoi_by_id(tournoi)
    # regles = get_Regle_by_id(tournoi)
    return render_template(
        "parametres.html", tournoi=t)#, regles = regles)


@app.route("/tableau_de_bord/<int:tournoi>/lancer_tournoi")
@login_required
def lancerCompet(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page permettant de remplir un formulaire afin de lancer un tournoi.
    L'utilisateur doit être connecté pour pouvoir y accéder.
    Le tournoi doit être inactif.
    """
    return render_template(
        "creation_matchs.html",
        tournoi = get_Tournoi_by_id(tournoi))

@app.route("/tableau_de_bord/<int:tournoi>/arreter_tournoi")
@login_required
def arreterCompet(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.
    Fonction permettant d'arreter un tournoi.
    L'utilisateur doit être connecté pour pouvoir y accéder.
    Le tournoi doit être actif.
    """
    t=get_Tournoi_by_id(tournoi)
    if t.etatT==1 :
        t.etatT=2
        db.session.commit()
    return redirect(url_for(
    "tournoi", id = tournoi))

    """ return render_template(
        "creation_matchs.html",
        tournoi = get_Tournoi_by_id(tournoi)) """

@app.route("/tableau_de_bord/<int:tournoi>/equipes/creer_equipe")
@login_required
def creerEquipe(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers la page de création d'équipe.
    Il faut être connecté pour pouvoir y acceder.
    """
    return render_template(
    "creerEquipe.html",
    tailleEquipe = 3,
    tournoi=get_Tournoi_by_id(tournoi))



@app.route("/tableau_de_bord/<int:tournoi>/matchs/<int:partie>/lancer_match", methods=("POST",))
def lancerMatch(tournoi, partie):
    """
    Param : tournoi(int), l'identifiant d'un tournoi. partie(int), l'identifiant d'une partie.
    Redirige vers la page permettant de lancer un match.
    """
    cartePartie = request.form["cartePartie"]
    lancer_match(partie, cartePartie)
    return render_template("lancerMatch.html",
                           equipes=get_equipe_by_partie(partie),
                           tournoi = tournoi,
                           partie = partie)

@app.route("/tableau_de_bord/<int:tournoi>/matchs/<int:partie>/resultat")
def resultatMatch(tournoi, partie):
    """
    Param : tournoi(int), l'identifiant d'un tournoi. partie(int), l'identifiant d'une partie.
    Redirige vers la page permettant de voir les resultats d'une partie.
    """
    resultat = arreterMatch_setScore(partie)
    return render_template("resultatMatch.html",
                           dico_resultat = resultat,
                           partie = partie,
                           equipes = get_equipe_by_partie(partie),
                           tournoi = tournoi)

@app.route("/tableau_de_bord/<int:tournoi>/equipes/confirmer_equipe", methods={"POST"})
@login_required
def confirmerEquipe(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Récupère les réponses au formulaire de la page "creerEquipe.html" et jjoute une équipe dans la BD.
    Il faut être connecté pour pouvoir y accéder.
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
    equipe['machineE']        = request.form['machineE']
    idEquipe = insert_equipe(equipe)
    e = get_equipe_by_id(idEquipe)
    insert_constituer(idEquipe, idChef)
    if int(request.form['nbParticipant']) == 0 :
        return redirect(url_for("equipe",tournoi = tournoi))
    else :
        return redirect(url_for(
        "ajout_membre", tournoi = tournoi, equipe = idEquipe))

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>/ajout_membre")
@login_required
def ajout_membre(tournoi, equipe):
    """
    param: tournoi (int), identifiant d'un tournoi.
           equipe (int), identifiant d'une équipe.

    Redirige vers la page d'ajout de membre à une équipe.
    L'utilisateur doit être connecté pour pouvoir y accéder.
    """
    e = get_equipe_by_id(equipe)
    t = get_Tournoi_by_id(tournoi)
    c = get_chef_by_id_equipe(equipe)
    return render_template(
        "ajoutMembre.html", equipe = e, tournoi = t, chef = c)

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>/ajouter_membre", methods=("GET","POST",))
@login_required
def ajouterMembre(tournoi, equipe):
    """
    param: tournoi (int), identifiant d'un tournoi.
           equipe (int), identifiant d'une équipe.

    Récupère les réponses au formulaire de la page "ajoutMembre.html" et ajoutes des membres à l'équipe.
    Il faut être connecté pour pouvoir y acceder.
    """
    e = get_equipe_by_id(equipe)
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

    Redirige vers une page permettant de modifier une équipe.
    Il faut être connecté pour pouvoir y accéder.
    """

    e = get_equipe_by_id(equipe)
    t = get_Tournoi_by_id(tournoi)
    liste = get_membres_constituer(equipe)
    l = []
    for part in liste:
        l.append(get_participant_by_id(part.idP))
    return render_template(
        "modifier_membres.html", tournoi = t, equipe = e, liste_membres = l)

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>/ajouter_un_membre", methods=("GET","POST",))
@login_required
def ajouterMembre2(tournoi, equipe):

    """
    param: tournoi (int), identifiant d'un tournoi.
           equipe (int), identifiant d'une équipe.

    Redirige vers une page permettant d'ajouter un membre unique à une équipe.
    Il faut être connecté pour pouvoir y accéder.
    """


    e = get_equipe_by_id(equipe)
    t = get_Tournoi_by_id(tournoi)
   # liste = get_membres_constituer(equipe)
    #l = []
    #for part in liste:
        #l.append(get_participant_by_id(part.idP))
    #c = get_chef_by_id_equipe(equipe)
    return render_template(
        "ajout1Membre.html", tournoi = t, equipe = e)

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>/valider_ajout_membre", methods={"POST"})
def valider_ajout_membre(tournoi, equipe):
    """
    param: tournoi (int), identifiant d'un tournoi.
           equipe (int), identifiant d'une équipe.

    Récupère les réponses au formulaire de la page ajoutMembre.html et ajoute un membre à l'équipe.
    Il faut être connecté pour pouvoir y accéder.
    """
    e = get_equipe_by_id(equipe)
    l = get_membres_constituer(equipe)
    t = get_Tournoi_by_id(tournoi)

    dico_participant = {}
    dico_participant['nomP'] = request.form['nom_membre']
    dico_participant['prenomP'] = request.form['prenom_membre']
    dico_participant['mailP'] = request.form['mail_membre']
    ajouter_participant(dico_participant,equipe)
    e.nbParticipant += 1
    update_Equipe(e,equipe)

    return redirect(url_for("equipe", tournoi = tournoi))

@app.route("/tableau_de_bord/<int:tournoi>/equipes/<int:equipe>/valider_modification_equipe", methods={"POST"})
def valider_modification_equipe(tournoi, equipe):
    """
    param: tournoi (int), identifiant d'un tournoi.
           equipe (int), identifiant d'une équipe.

    Récupère les réponses au formulaire de la page modifier_membre.html et modifie l'équipe.
    Il faut être connecté pour pouvoir y accéder.
    """
    e = get_equipe_by_id(equipe)
    l = get_membres_constituer(equipe)
    t = get_Tournoi_by_id(tournoi)
    for i in range(len(l)):
        dico_participant = {}
        dico_participant['nomP'] = request.form['nom_membre'+str(i)]
        dico_participant['prenomP'] = request.form['prenom_membre'+str(i)]
        dico_participant['mailP'] = request.form['mail_membre'+str(i)]

        e.nomE = request.form["nomEquipe"]
        e.machineE = request.form["machineE"]
        update_Equipe(e,e.idE)
        update_participant(dico_participant, l[i].idP)

    return redirect(url_for("voirCompet_equipe", tournoi = tournoi))


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
    Affiche les tournois correspondant à notre recherche dans la page tableauDeBord.html.
    Il faut être connecté pour pouvoir y accéder.
    """
    a = request.form['search']
    return render_template(
        "tableauDeBord.html", tournois= getRechercheAllTournois(a), route="tableau")

@app.route("/tableau_de_bord/<int:tournoi>/lancer_tournoi/tournoi_lance",methods={"POST"})
@login_required
def lancer_tournoi(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Génère les matchs du tournoi correspondant à l'id passé en paramètre.
    """
    automatique_match(tournoi,int(request.form['nbMatchs']),int(request.form['nbEquipe']))
    return render_template("versMatchs.html",tournoi = tournoi)

@app.route("/tableau_de_bord/<int:id>/modifier_competition", methods={"POST"})
@login_required
def modifierTournoi(id):
    """
    param:id (int), identifiant d'un tournoi

    Récupère les réponses au formulaire de la page "parametres.html" et modifie le tournoi correspondant
    à l'id passé en paramètre.
    """
    tournoi = {}
    tournoi['intituleT']         = request.form['intituleT']
    tournoi['descT']             = request.form['descT']
    tournoi['dateT']             = request.form['dateT']
    tournoi['dateFinT']          = request.form['dateFinT']
    tournoi['lieuT']             = request.form['lieuT']
    tournoi['disciplineT']       = request.form['disciplineT']
    tournoi['nbEquipe']          = request.form['nbEquipe']
    tournoi['nbParticipantsMax'] = request.form['nbParticipantsMax']
    tournoi['logoT']             = request.form['logoT']
    tournoi['stream']            = request.form['stream']
    tournoi['nbTours']           = request.form['nbTours']
    tournoi['cheminMaps']        = request.form['cheminMaps']
    tournoi['cheminScript']      = request.form['cheminScript']
    tournoi['etatT']             = 0
    tournoi['idAdmin']           = current_user.idAdmin

    update_tournoi(tournoi, id)

    return redirect(url_for("tournoi", id = id))

@app.route("/tableau_de_bord/<int:idT>/confirmer_photo", methods={"POST"})
@login_required
def confirmerPhoto(idT):
    """
    param : idT, l'identifiant du tournoi.
    Crée une photo et l'ajoute dans la BD.
    """
    photo = request.files['photo']

    insert_photo(photo, idT)
    tournoi = get_Tournoi_by_id(idT)
    photo.save(os.path.join(tournoi.dossierTournoi, photo.filename))

    return redirect(url_for("voirPhotos",tournoi=idT))

@app.route("/tableau_de_bord/<int:tournoi>/bilan")
@login_required
def bilan(tournoi):
    """
    param : tournoi(int), identifiant du tournoi.

    Redirige vers la page de bilan d'un tournoi.
    Il faut être connecté pour pouvoir y accéder.
    """

    dico = {}
    equipesT = get_All_Equipes_Classe(tournoi)
    print("bonjour")
    """ for equipe in equipesT:
        dico[equipe.idE] = get_participant_by_id_equipe(equipe.idE) """
    return render_template(
        "bilan.html",
        equipes=equipesT,
        participants=get_participant_by_id_equipe(equipesT[0].idE),
        tournoi = get_Tournoi_by_id(tournoi),
        route="tableau"
        )

@app.route("/tableau_de_bord/<int:tournoi>/supprimer_equipe/<int:equipe>")
@login_required
def supprime_equipe(equipe,tournoi):
    """
    param: equipe (int), identifiant d'une équipe. tournoi(int), l'identifiant du tournoi.

    supprime une equipe dans la BD
    """
    delete_equipe(equipe)
    return redirect(url_for("equipe",tournoi=tournoi))
