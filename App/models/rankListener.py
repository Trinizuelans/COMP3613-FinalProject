from App.database import db

class RankListener(db.Model):
    __tablename__ = 'rank_listener'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    leaderboard_id = db.Column(db.Integer, db.ForeignKey('leaderboard.leaderboard_id'))

    __mapper_args__ = {
        'polymorphic_on': type,
    }

    def __init__(self,leaderboard_id):
        self.leaderboard_id = leaderboard_id



    def get_json(self):
        return{
            'id': self.id,
            'leaderboard_id': self.leaderboard_id,
            'type': self.type
        }
    
    def update(self,prev_top20competitors,top20competitors,rank_switch):
        print("Rank Listener message")