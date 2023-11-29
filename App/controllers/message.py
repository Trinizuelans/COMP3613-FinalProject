from App.database import db
from App.models import Message


def create_message(message_inbox_id, content):
    try:
        new_message = Message(message_inbox_id= message_inbox_id, content= content)
        if new_message:
            db.session.add(new_message)
            db.session.commit()
            return new_message
        return None

    except Exception:
        db.rollback()

def get_message(id):
    return Message.query.get(id)

def get_message_json(id):
    m = get_message(id)
    if m:
        return m.get_json()
    return None

def get_all_messages():
    return Message.query.all()

def get_all_messages_json():
    messages = get_all_messages()

    if not messages:
        return []
    
    messages = [message.get_json() for message in messages]
    return messages

def get_all_inbox_messages(message_inbox_id):
    return Message.query.filter_by(message_inbox_id = message_inbox_id).all()

def get_all_inbox_messages_json(message_inbox_id):
    messages =  Message.query.filter_by(message_inbox_id = message_inbox_id).all()

    if not messages:
        return []
    messages = [message.get_json() for message in messages]
    return messages

# changes is_read boolean from false to true
def is_read(message_id):
    
    try:
        message = get_message(message_id)
        if message:
            message.is_read = True
            db.session.add(message)
            db.session.commit()

    except Exception:
        db.session.rollback()