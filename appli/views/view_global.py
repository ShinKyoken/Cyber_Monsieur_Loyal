from .config import *

class LoginForm(FlaskForm):
    """
    Le formulaire permettant de se connecter
    """
    username = StringField('Username')
    password = PasswordField('Password')
    next = HiddenField()

    def get_authenticated_user(self):

        """
        param:

        return: (a remplir)
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

@app.route("/connexion",methods=["GET","POST"])
def connect():
    """
    Connecte un utilisateur, en le redirigeant vers l'accueil du site si ses identifiants sont corrects.
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
        "connexion.html",
        form = form,
        route="connexion")

@app.route("/logout/")
@login_required
def logout():
    """
    Déconnecte l'utilisateur et le redirige vers l'accueil du site.
    """
    logout_user()
    return redirect(url_for('home'))

@app.route("/inscription",methods=["GET","POST"])
def inscription():
    """
    Page permettant de pouvoir s'inscrire grâce au formulaire "LoginForm"
    """
    form = LoginForm()
    return render_template("inscription.html", form = form)

@app.route("/confirmer_inscription",methods=["GET","POST"])
def confirmer_ajout_admin():
    """
    Permet de vérifier si le formulaire est validé. Si oui, l'utilisateur est inscrit et est redirigé
    vers la page de connexion. Sinon, il n'est pas inscrit et reste sur la page d'inscription.
    """
    f = LoginForm()
    if f.validate_on_submit():
        if(len(get_admin_by_username(f.username.data))==0):
            m = sha256()
            m.update(f.password.data.encode())
            passwd = m.hexdigest()
            newAdmin = ADMIN(nomAdmin = f.username.data, mdpAdmin = passwd)
            db.session.add(newAdmin)
            db.session.commit()
            return redirect(url_for("connect"))
    return render_template(
        "inscription.html",form = f,adminExiste=1)

@login_manager.unauthorized_handler
def unauthorized_callback():
    """
    Permet de rediriger sur la page de connexion si l'utilisateur n'est pas connecté et essaye
    d'atteindre une page qui n'est pas accessible si on est déconnecté.
    """
    return redirect(url_for('connect'))


@app.route("/creer_competition")
@login_required
def creerCompetition():
    """
    Redirige vers la page de création de competition.
    """
    return render_template("creerCompetition.html",
                           route="creer")

@app.route("/confirmer_competition", methods={"POST"})
@login_required
def confirmerTournoi():
    """
    Récupère les réponses au formulaire présent dans la page creerCompetition.html et créé un tournoi avec.
    """
    tournoi = {}
    tournoi['intituleT']         = request.form['intituleT']
    tournoi['reglement']         = request.files['reglement']
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
    id = insert_tournoi(tournoi)
    os.mkdir("appli/static/tournoi_" + tournoi['intituleT'] + "/photos/")
    os.mkdir("appli/static/tournoi_" + tournoi['intituleT'] + "/reglement/")
    dossierPhotos = "appli/static/tournoi_" + tournoi['intituleT']+"/photos/"
    dossierReglement = "appli/static/tournoi_" + tournoi['intituleT']+"/reglement/"
    insert_cheminPhotos(dossierPhotos,id)
    insert_cheminReglement(dossierReglement,id)
    return redirect(url_for("tournoi", id = int(id)))
