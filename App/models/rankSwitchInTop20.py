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

    def update(self,prev_top20competitors,top20competitors,rank_switch):
        from App.models import MessageInbox
        import App.controllers.message as message

        ranked_switch_competitors = {}

        if (prev_top20competitors != top20competitors):
            ranked_switch_competitors = set(top20competitors) & set(prev_top20competitors)
 
            for r in ranked_switch_competitors:
                if(rank_switch[r.id]["previous_rank"] != rank_switch[r.id]["current_rank"]):

                    if(rank_switch[r.id]["previous_rank"] > rank_switch[r.id]["current_rank"]):
                        content = "Great Job! You increased your rank in the Top 20 from Rank #" + str(rank_switch[r.id]["previous_rank"]) + " to Rank # " + str(rank_switch[r.id]["current_rank"])

                    if(rank_switch[r.id]["previous_rank"] < rank_switch[r.id]["current_rank"]):
                        content = "Oh No! Your rank has decreased in the Top 20 from Rank #" + str(rank_switch[r.id]["previous_rank"]) + " to Rank # " + str(rank_switch[r.id]["current_rank"])

                    competitor_message_inbox = MessageInbox.query.filter_by(competitor_id = r.id).first()
                
                    if competitor_message_inbox:
                        message.create_message(competitor_message_inbox.id,content)
                    
 
 
 
 
 
 
 
            # print(rank_switch[20]["previous_rank"])
            # print("\n")
            # print("top20competitors")
            # print(top20competitors)
            # print("\n")
            # print("prev_top20competitors")
            # print(prev_top20competitors)

            # print("\n")
            # print("length:" + str(len(ranked_switch_competitors)))
            # for x in ranked_switch_competitors:
            #     print(x)
            #figure out some way to show updated ranks

    
        # print(ranked_switch_competitors)