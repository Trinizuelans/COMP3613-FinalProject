from App.database import db

class RankListener(db.Model):
    # __abstract__ = True
    listener_id = db.Column(db.Integer, primary_key=True)
    leaderboard_id = db.Column(db.Integer, db.ForeignKey('leaderboard.leaderboard_id'))



    def __init__(self,listener_id):
        self.id = listener_id

    def get_json(self):
        return{
            'listener_id': self.listener_id,
            'leaderboard': self.leaderboard,
            'previousTop20competitors': self.previousTop20competitors
        }
    
