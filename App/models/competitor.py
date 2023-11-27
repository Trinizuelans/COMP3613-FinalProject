from flask_login import UserMixin
from App.database import db
from App.models.user import User


class Competitor (User):
    overall_points = db.Column(db.Integer,nullable = False, default = 0)
    rank = db.Column(db.Integer, default = None)



    def __init__(self,username,email,password):
        # super().__init__(username,email,password)
        self.username = username
        self.email = email
        self.set_password(password)
        self.overall_points = 0
        self.rank = None

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'overall_points': self.overall_points,
            'rank': self.rank
        }
        
    def toDict(self):
        return{
            "id": self.id,
            "username": self.username,
            "overall_points": self.overall_points,
            "rank": self.rank
        }