from App.database import db

# This is the Publisher for the Observer Design Pattern
class Leaderboard(db.Model):
    leaderboard_id = db.Column(db.Integer, primary_key=True)
    competitors = db.relationship('Competitor', backref='leaderboard', lazy=True)
    prev_top20competitors = None
    top20competitors = None
    rankListeners = db.relationship('RankListener', backref='leaderboard', lazy=True)

    def __init__(self,leaderboard_id):
        self.leaderboard_id = leaderboard_id
        self.prev_top20competitors = []
        self.top20competitors = []
        self.rankListeners = []

    def get_json(self):
        return{
            'leaderboard_id': self.leaderboard_id,
            'competitors': self.competitors,
            'top20competitors': self.prev_top20competitors,
            'rankListener': self.rankListener
        }

    def subscribe(self,rankListener):
        self.rankListeners.append(rankListener)

    def notify_subscribers(self,prev_top20competitors, top20competitors):
        for rankListener in self.rankListeners:
            rankListener.update(self.prev_top20competitors,self.top20competitors)

