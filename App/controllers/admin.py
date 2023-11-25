from App.models import Admin
from App.database import db


def create_admin(username, email, password):
    newAdmin = Admin(username=username,email = email, password=password)
    try:
        db.session.add(newAdmin)
        db.session.commit()
        return newAdmin
    except Exception:
        db.session.rollback()
        return newAdmin

def get_admin_by_username(username):
    return Admin.query.filter_by(username=username).first()

def get_admin(id):
    return Admin.query.get(id)

def get_all_admins():
    return Admin.query.all()

def get_all_admins_json():
    admins = Admin.query.all()
    if not admins:
        return []
    admins = [admin.get_json() for admin in admins]
    return admins

def update_admin(id, username,email):
    admin = get_admin(id)
    if admin:
        admin.username = username
        admin.email = email
        db.session.add(admin)
        return db.session.commit()
    return None

# def create_host():

# def create_competition_team():

# def add_competitor_to_team(user,team):

