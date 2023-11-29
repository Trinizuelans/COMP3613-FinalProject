from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from App.controllers.message import (
    create_message,
    get_message_json,
    get_all_messages_json

)

message_views = Blueprint('message_views', __name__, template_folder='../templates')


@message_views.route('/api/messages', methods=['POST'])
def create_message_action():
    data = request.form
    message_inbox_id = int(data['message_inbox_id'])
    content = data['content']

    message = create_message(message_inbox_id,content)
    
    if message:
        return (jsonify({'message': f"Message created"}),201)
    return (jsonify({'error': f"Error creating message"}), 400)

@message_views.route('/api/messages/<int:message_id>', methods=['GET'])
def get_message_action(message_id):
    message = get_message_json(message_id)
    if message:
        return (message,200)
    return (jsonify({'error': f"Error retrieving message"}), 400)

@message_views.route('/api/messages', methods=['GET'])
def get_all_messages_action():
    messages = get_all_messages_json()

    if messages:
        return(messages,200)
    
    return jsonify({'error': f"Error retrieving messages"}), 400
