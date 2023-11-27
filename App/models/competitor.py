from flask_login import UserMixin
from App.database import db
from App.models.user import User


class Competitor (User):
    overall_points = db.Column(db.Integer,nullable = False, default = 0)
    rank = db.Column(db.Integer, default = None)
    leaderboard_id = db.Column(db.Integer, db.ForeignKey('leaderboard.leaderboard_id'), nullable=False)



    def __init__(self,username,email,password):
        # super().__init__(username,email,password)
        self.username = username
        self.email = email
        self.set_password(password)
        self.overall_points = 0
        self.rank = None
        self.leaderboard_id = 1

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'overall_points': self.overall_points,
            'rank': self.rank,
            'leaderboard_id': self.leaderboard_id
        }
        
    def toDict(self):
        return{
            "id": self.id,
            "username": self.username,
            "overall_points": self.overall_points,
            "rank": self.rank
        }