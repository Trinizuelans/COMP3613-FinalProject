from App.database import db
from App.models.rankListener import RankListener

class RankDownFromTop20(RankListener):


    def __init__(self,listener_id):
        self.id = listener_id

    def get_json(self):
        return{
            'listener_id': self.listener_id,
            'previousTop20competitors': self.previousTop20competitors
        }