from .config import *

@app.route("/voir_competitions_actives")
def voirCompetitionsActives():
    """
    Redirige vers la page des compétitions actives.
    """
    return render_template(
        "voirCompetitionsActives.html",tournois = get_All_Tournois_by_Etat(1),
        dicoAdmin = get_admin_by_tournoi(1),
        route="voirCompet")

@app.route("/voir_competitions_inactives")
def voirCompetitionsInactives():
    """
    Redirige vers la page des compétitions inactives.
    """
    return render_template(
        "voirCompetitionsInactives.html",tournois = get_All_Tournois_by_Etat(0),
        dicoAdmin = get_admin_by_tournoi(0),
        route="voirCompet")

@app.route("/voir_competitions_terminees")
def voirCompetitionsTerminees():
    """
    Redirige vers la page des compétitions terminées.
    """
    return render_template(
        "voirCompetitionsTerminees.html", tournois = get_All_Tournois_by_Etat(2),
        dicoAdmin = get_admin_by_tournoi(2),
        route="voirCompet")

@app.route("/voir_competition/<int:tournoi>")
def voirCompet(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers la page d'un tournoi dont l'utilisateur n'est pas l'administrateur.
    """
    return render_template(
        "newTournoi.html",
        tournoi=get_Tournoi_by_id(tournoi),
	nbEquipe=count_equipe_by_tournoi(tournoi),
        admin = get_admin_by_id(tournoi),
        nbPartieTerminee=len(get_All_Parties_Terminees(tournoi)),
        route="voirCompet")

@app.route("/voir_competition/<int:tournoi>/matchs")
def voirCompet_Matchs(tournoi):
    """
    param: tournoi (int), identifiant d'un tournoi.

    Redirige vers une page affichant les differents matchs du tounoi ainsi qu'un classement.
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

    Redirige vers une page affichant les photo du tournoi.
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

    Redirige vers une page affichant les differentes équipes du tournoi
    """
    dico = {}
    equipes = get_equipe_by_tournoi(tournoi)
    for equipe in equipes:
        dico[equipe.idE] = get_participant_by_id_equipe(equipe.idE)

    return render_template(
        "equipe.html",
        equipes=get_equipe_by_tournoi(tournoi),
        tournoi=get_Tournoi_by_id(tournoi),
        nbEquipe = count_equipe_by_tournoi(tournoi),
        route="voirCompet",
        participants=dico)

@app.route("/voir_competitions_actives/recherche/", methods=("POST",))
def rechercheTournoisActif():
    """
    Affiche les tournois correspondant à notre recherche dans la page voirCompetitionsActives.html .
    """
    a = request.form['search']
    return render_template(
        "voirCompetitionsActives.html",
        tournois = getRechercheTournoisActif(a),
        dicoAdmin = get_nom_prenom_by_tournoi(1),
        route="voirCompet"
        )

@app.route("/voir_competitions_inactives/recherche/", methods=("POST",))
def rechercheTournoisInactif():
    """
    Affiche les tournois correspondant à notre recherche dans la page voirCompetitionsInactives.html .
    """
    a = request.form['search']
    return render_template(
        "voirCompetitionsInactives.html",
        tournois = getRechercheTournoisInactif(a),
        dicoAdmin = get_nom_prenom_by_tournoi(0),
        route="voirCompet")

@app.route("/voir_competitions_terminees/recherche/", methods=("POST",))
def rechercheTournoisTerminee():
    """
    Affiche les tournois correspondant à notre recherche dans la page voirCompetitionsTerminées.html .
    """
    a = request.form['search']
    return render_template(
        "voirCompetitionsTerminees.html",
        tournois = getRechercheTournoisTerminee(a),
        dicoAdmin = get_nom_prenom_by_tournoi(2),
        route="voirCompet"
        )

@app.route("/voir_competition/<int:tournoi>/bilan")
def voirBilan(tournoi):
    """
    param : tournoi(int), identifiant du tournoi.

    Redirige vers la page de bilan d'un tournoi.
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
        route="voirCompet"
        )
