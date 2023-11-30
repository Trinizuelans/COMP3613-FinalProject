from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

from App.models import User,Competitor,Admin

def jwt_authenticate(username, password, is_admin=False):
    user = None
    
    if is_admin:
        user = Admin.query.filter_by(username=username).first()
    else:
        user = Competitor.query.filter_by(username=username).first()

    if user and user.check_password(password):
        return create_access_token(identity=username)
    
    return None

def login(username, password, admin = False):
    if (admin == True):
        user = Admin.query.filter_by(username=username).first()

    else:
        user = Competitor.query.filter_by(username=username).first()

    if user and user.check_password(password):
        return user
    return None

# def setup_flask_login(app):
#     login_manager = LoginManager()
#     login_manager.init_app(app)
    
#     @login_manager.user_loader
#     def load_user(user_id):
#         return Competitor.query.get(user_id)
    
#     return login_manager

# def setup_jwt(app):
#     jwt = JWTManager(app)

#     @jwt.user_identity_loader
#     def user_identity_lookup(identity):
#         user = Competitor.query.filter_by(username=identity).one_or_none()
#         if user:
#             return user.id
#         return None

#     @jwt.user_lookup_loader
#     def user_lookup_callback(_jwt_header, jwt_data):
#         identity = jwt_data["sub"]
#         return User.query.get(identity)

#     return jwt

# def isAdmin(user):
    
#     user = Admin.query.filter_by(username=username).first()

#     if (user == None):
#         user = Competitor.query.filter_by(username=username).first()

def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        # Load either Admin or Competitor based on the provided user_id
        admin = Admin.query.get(user_id)
        if admin:
            return admin
        else:
            return Competitor.query.get(user_id)
    
    return login_manager

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        # Check if the identity exists as an Admin or Competitor
        admin = Admin.query.filter_by(username=identity).one_or_none()
        if admin:
            return admin.username
        else:
            competitor = Competitor.query.filter_by(username=identity).one_or_none()
            if competitor:
                return competitor.username
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        # Lookup the user (Admin or Competitor) based on the identity (username)
        admin = Admin.query.filter_by(username=identity).one_or_none()
        if admin:
            return admin
        else:
            return Competitor.query.filter_by(username=identity).one_or_none()
    
    return jwt