from App.database import db
from App.models.rankListener import RankListener

class RankSwitchInTop20(RankListener):
    __tablename__ = 'rank_switch_in_top20'
    id = db.Column(db.Integer, db.ForeignKey('rank_listener.id'), primary_key=True)
    # Add specific columns for ConcreteRankListenerA

    __mapper_args__ = {
        'polymorphic_identity': 'rank_switch_in_top20',
    }


    def __init__(self,leaderboard_id):
        self.leaderboard_id = leaderboard_id
    


    def get_json(self):
        return{
            'listener_id': self.listener_id,
            'previousTop20competitors': self.previousTop20competitors
        }

    def update(self,prev_top20competitors,top20competitors):
        # print("Rank Switch message!")

        ranked_switch_competitors = {}

        if (prev_top20competitors != top20competitors):
            ranked_switch_competitors = set(top20competitors) and set(prev_top20competitors)

            #figure out some way to show updated ranks

    
        # print(ranked_switch_competitors)