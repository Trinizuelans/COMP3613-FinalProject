from App.database import db
 
class MessageInbox(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    competitor_id = db.Column(db.Integer(), db.ForeignKey('competitor.id'), nullable=False)
    messages = db.relationship('Message', backref='message_inbox', lazy='dynamic')

    def __init__(self, competitor_id):
        self.competitor_id = competitor_id
        self.messages = []

    def get_json(self):
        from App.controllers.message import get_all_inbox_messages_json

        return{
            'id': self.id,
            'competitor_id': self.competitor_id,
            'messages': get_all_inbox_messages_json(self.id)
        }
    
    def __repr__(self):
        from App.controllers.message import get_all_inbox_messages_json
        return f"MessageInbox(id={self.id}, competitor_id={self.competitor_id}, messages={get_all_inbox_messages_json(self.id)})"