from werkzeug.security import check_password_hash, generate_password_hash
from App.models.user import User

class Admin(User):

    # competitions relationship
    # teams relationship


    def __init__(self, username, email, password):
        # super().__init__(username,email,password)
        self.username = username
        self.email = email
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }


