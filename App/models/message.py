from App.database import db
from sqlalchemy.orm import relationship

class Message(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    message_inbox_id = db.Column(db.Integer(), db.ForeignKey('message_inbox.id'), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    is_read = db.Column(db.Boolean(), default=False)
    timestamp = db.Column(db.DateTime(), default=db.func.current_timestamp())

    def __init__(self, message_inbox_id, content):
        self.message_inbox_id = message_inbox_id
        self.content = content

    def get_json(self):
        return {
            'id': self.id,
            'message_inbox_id': self.message_inbox_id,
            'content': self.content,
            'is_read': self.is_read,
            'timestamp': self.timestamp
        }
    
    def __repr__(self):
        return f"Message(id={self.id}, message_inbox_id={self.message_inbox_id}, content='{self.content}', is_read={self.is_read}, timestamp={self.timestamp})"