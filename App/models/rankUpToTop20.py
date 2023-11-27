from App.database import db
from App.models.rankListener import RankListener

class RankUpToTop20(RankListener):
    __tablename__ = 'rank_up_to_top20'
    id = db.Column(db.Integer, db.ForeignKey('rank_listener.id'), primary_key=True)
    # Add specific columns for ConcreteRankListenerA

    __mapper_args__ = {
        'polymorphic_identity': 'rank_up_to_top20',
    }
    def __init__(self,leaderboard_id):
        self.leaderboard_id = leaderboard_id

    def get_json(self):
        return{
            'listener_id': self.listener_id,
            'previousTop20competitors': self.previousTop20competitors
        }