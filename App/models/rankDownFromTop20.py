from App.database import db
from App.models.rankListener import RankListener

class RankDownFromTop20(RankListener):

    __tablename__ = 'rank_down_from_top20'
    id = db.Column(db.Integer, db.ForeignKey('rank_listener.id'), primary_key=True)
    # Add specific columns for ConcreteRankListenerA

    __mapper_args__ = {
        'polymorphic_identity': 'rank_down_from_top20',
    }

    def __init__(self,leaderboard_id):
        self.leaderboard_id = leaderboard_id

    def get_json(self):
        return{
            'listener_id': self.listener_id,
            'previousTop20competitors': self.previousTop20competitors
        }
    
    def update(self,prev_top20competitors,top20competitors):

        deranked_competitors = {}

        if (prev_top20competitors != top20competitors):
            from App.models import MessageInbox
            import App.controllers.message as message

            deranked_competitors =  set(prev_top20competitors) - set(top20competitors)
          
            # for every deranked competitor, print rank down message along with their new rank
            for competitor in deranked_competitors:
                content = "Oh no! You are no longer in the top 20!. You fell from your previous Rank to Rank #" + str(competitor.rank)
                
                competitor_message_inbox = MessageInbox.query.filter_by(competitor_id = competitor.id).first()
                if competitor_message_inbox:
                    message.create_message(competitor_message_inbox.id,content)


