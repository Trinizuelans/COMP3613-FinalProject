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
    
    def update(self,prev_top20competitors,top20competitors,rank_switch):
        from App.models import MessageInbox
        import App.controllers.message as message
        
        upranked_competitors = {}

        if (prev_top20competitors != top20competitors):
            upranked_competitors = set(top20competitors) - set(prev_top20competitors)
            for competitor in upranked_competitors:
                content = "Great Job! You are in the Top 20 currently at rank at #" + str(competitor.rank)

                competitor_message_inbox = MessageInbox.query.filter_by(competitor_id = competitor.id).first()
                
                if competitor_message_inbox:
                    message.create_message(competitor_message_inbox.id,content)
                
