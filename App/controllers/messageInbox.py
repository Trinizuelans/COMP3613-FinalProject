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
    if message_inbox:
        return message_inbox.get_json()
    return None


def get_all_message_inbox():
    return MessageInbox.query.all()

def get_all_message_inbox_json():
    messages = get_all_message_inbox()
    if not messages:
        return []
    messages = [competitor.get_json() for competitor in messages]
    return messages

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
                return latest_message.content
            
            if(latest_message.is_read == True):
                return "No new unread messages"

            return "Empty message inbox"
        
        return None
    except Exception:
        db.session.rollback()

def delete_message_inbox(id):
    try:
        inbox = get_message_inbox_by_competitor_id(id)
        inbox_id = inbox.id
        if inbox:
            deleted =  delete_messages_by_message_inbox_id(inbox_id)
            if deleted:
                db.session.delete(inbox)
                db.session.commit()
                return True
        else:
            print(f"Message Inbox with ID {inbox_id} does not exist.")
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        db.session.rollback()
        return False
    

def delete_messages_by_message_inbox_id(message_inbox_id):
    try:
        messages_to_delete = Message.query.filter_by(message_inbox_id=message_inbox_id).all()
        if messages_to_delete:
            for message in messages_to_delete:
                db.session.delete(message)
            db.session.commit()
            return True
        else:
            print(f"No messages found for Message Inbox ID: {message_inbox_id}")
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        db.session.rollback()
        return False
