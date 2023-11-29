from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from App.controllers import (
    get_latest_message,
    get_message_inbox_by_competitor_id_json,
    get_all_message_inbox_json

)


message_inbox_views = Blueprint('message_inbox_views', __name__, template_folder='../templates')


@message_inbox_views.route('/api/inboxes', methods=['GET'])
def get_all_message_inboxes_action():
    m_i = get_all_message_inbox_json()
    if m_i:
        return (m_i,200)
    return (jsonify({'error': f"Error retrieving message inboxes"}), 400)

@message_inbox_views.route('/api/inboxes/<int:competitor_id>', methods=['GET'])
def get_competitor_message_inboxes_action(competitor_id):
    m_i = get_message_inbox_by_competitor_id_json(competitor_id)
    if m_i:
        return (m_i,200)
    return (jsonify({'error': f"Error retrieving message inbox"}), 400)

@message_inbox_views.route('/api/inboxes/latest/<int:inbox_id>', methods=['GET'])
def get_latest_message_action(inbox_id):
    message = get_latest_message(inbox_id)
    if message:
        return (jsonify({'message':message}),200)
    return (jsonify({'error': f"Message inbox not found"}), 400)