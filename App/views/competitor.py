from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from App.controllers import (
    create_competitor,
    get_competitor_json,
    get_all_competitors_json,
    update_competitor,
    add_competitor_overall_points,
    remove_competitor_overall_points,
    delete_competitor,
    



)


competitor_views = Blueprint('competitor_views', __name__, template_folder='../templates')

@competitor_views.route('/api/competitors', methods=['GET'])
def get_competitors_action():
    users = get_all_competitors_json()
    return users

@competitor_views.route('/api/competitors', methods=['POST'])
def create_competitor_endpoint():
    data = request.form
    response = create_competitor(data['username'],data['email'],data['password'])
    if response:
        return (jsonify({'message': f"Competitor created"}),201)
    return (jsonify({'error': f"Error creating user"}),400)


@competitor_views.route('/api/competitors', methods=['PUT'])

def update_competitor_endpoint():
    data = request.form
    competitor_id = request.args.get('id')
    updated = update_competitor(
        competitor_id,
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    print(current_user)
    if updated:
        return jsonify({'message': f"Competitor {competitor_id} updated"}), 200
    return jsonify({'error': f"Error updating competitor {competitor_id}"}), 400


@competitor_views.route('/api/competitors/<int:competitor_id>', methods=['GET'])
def get_competitor_action(competitor_id):
    competitor = get_competitor_json(competitor_id)
    if competitor:
        return jsonify(competitor)
    return jsonify({'error': 'Competitor not found'}), 404

@competitor_views.route('/api/competitors/addPoints', methods=['PUT'])
def add_points_competitor_action():
    data = request.form

    id = int(data['competitor_id'])
    points = int(data['points'])

    print(id)
    print(points)
    response = add_competitor_overall_points(id, points)
    print("yo")
    print(response)
    if response:
        return (jsonify({'message': f"Competitor points added"}),201)
    return (jsonify({'error': f"Error adding competitor points"}),400)

@competitor_views.route('/api/competitors/removePoints', methods=['PUT'])
def remove_points_competitor_action():
    data = request.form

    id = int(data['competitor_id'])
    points = int(data['points'])

    response = remove_competitor_overall_points(id, points)
    if response:
        return (jsonify({'message': f"Competitor points removed"}),201)
    return (jsonify({'error': f"Error removing competitor points"}),400)

@competitor_views.route('/api/competitors/delete/<int:competitor_id>', methods=['DELETE'])
def delete_competitor_action(competitor_id):
    response = delete_competitor(competitor_id)

    if response:
           return (jsonify({'message': f"Competitor id: {competitor_id} deleted"}),201)
    return (jsonify({'error': f"Error deleting competitor id: {competitor_id}"}),400)
