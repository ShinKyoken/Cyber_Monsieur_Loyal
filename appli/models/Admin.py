from flask_login import UserMixin, current_user
from appli.app import db, login_manager

class ADMIN(UserMixin,db.Model):
    idAdmin        = db.Column(db.Integer, primary_key = True)
    nomAdmin       = db.Column(db.String(100))
    mdpAdmin       = db.Column(db.String(100))
    def get_id(self) :
        return self.idAdmin

@login_manager.user_loader
def load_user(username):
    """
    param: username (str), le nom d'un admin

    recherche un admin qui a le nom recherché
    """
    return ADMIN.query.get(username)

def get_All_Admins():
    """
    retourne la liste des Admins
    """
    return ADMIN.query.all()

def get_admin_by_username(username):
    """
    param : username(string), le nom d'un admin

    Retourne un admin
    """

    a = ADMIN.query.filter_by(nomAdmin = username).all()
    return a
