from App.database import db
from App.models import MessageInbox,Message


def create_message_Inbox(competitor_id):
    try:
        new_Inbox = MessageInbox(competitor_id = competitor_id)
        if new_Inbox:
            db.session.add(new_Inbox)
            db.session.commit()
            return new_Inbox
        return None

    except Exception:
        db.rollback()

def get_message_inbox(id):
    return MessageInbox.query.get(id)

def get_message_inbox_json(id):
    message_inbox = MessageInbox.query.get(id)
    return message_inbox.get_json()

def get_message_inbox_by_competitor_id(competitor_id):
    return MessageInbox.query.filter_by(competitor_id = competitor_id).first()

def get_message_inbox_by_competitor_id_json(competitor_id):
    message_inbox = MessageInbox.query.filter_by(competitor_id = competitor_id).first()
    return message_inbox.get_json()


def get_all_message_inbox():
    return MessageInbox.query.all()

def get_all_message_inbox_json(message_inbox_id):
    messages = get_all_message_inbox_messages(message_inbox_id)
    if not messages:
        return []
    messages = [competitor.get_json() for competitor in messages]
    return messages

# def add_message(message_inbox_id, message):
    
#     try:
#         message_inbox = get_message_inbox(message_inbox_id)

#         if message_inbox:
#             message_inbox.messages.append(message)
#             db.session.add(message_inbox)
#             db.session.commit()
#             return message_inbox
#         return None
#     except Exception:
#         db.session.rollback()

def get_all_message_inbox_messages(message_inbox_id):
        message_inbox = get_message_inbox(message_inbox_id)
        return message_inbox.messages

def get_latest_message(message_inbox_id):
    
    try:
        message_inbox = get_message_inbox(message_inbox_id)
        if message_inbox:
            latest_message = message_inbox.messages.order_by(Message.timestamp.desc()).first()
            
            if(latest_message.is_read == False):
                latest_message.is_read = True
                db.session.add(latest_message)
                db.session.commit()
                return latest_message

            return None
        
        return None
    except Exception:
        db.session.rollback()


