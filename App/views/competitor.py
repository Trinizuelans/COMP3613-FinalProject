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
    get_competitor_by_username
    



)


competitor_views = Blueprint('competitor_views', __name__, template_folder='../templates')

@competitor_views.route('/api/competitors', methods=['GET'])
def get_competitors_action():
    competitors = get_all_competitors_json()
    if not competitors:
        return (jsonify({'error': f"Error retrieving competitors"}),400)
    return (competitors,200)

@competitor_views.route('/api/competitors', methods=['POST'])
def create_competitor_endpoint():

    data = request.form

    response = get_competitor_by_username(data['username'])

    if data['username'] == "" or data['email'] == "":
        return (jsonify({'error': f"Error creating competitor"}),400)

    if response:
        return (jsonify({'error': f"Competitor already exist"}),400)

    response = create_competitor(data['username'],data['email'],data['password'])
    if response:
        return (jsonify({'message': f"Competitor created"}),201)
    return (jsonify({'error': f"Error creating competitor"}),400)


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
    if data['username'] == "" or data['email'] == "":
       return (jsonify({'error': f"Error updating competitor"}),400)

    if updated:
        return jsonify({'message': f"Competitor updated"}), 200
    return jsonify({'error': f"Error updating competitor"}), 400


@competitor_views.route('/api/competitors/<int:competitor_id>', methods=['GET'])
def get_competitor_action(competitor_id):
    competitor = get_competitor_json(competitor_id)
    if competitor:
        return jsonify(competitor)
    return jsonify({'error': 'Competitor not found'}), 404

@competitor_views.route('/api/competitors/points/addition', methods=['PUT'])
def add_points_competitor_action():
    data = request.form

    id = int(data['competitor_id'])
    points = int(data['points'])

    if points < 0:
        return (jsonify({'error': f"Error adding competitor points"}),400)

    response = add_competitor_overall_points(id, points)



    if response:
        return (jsonify({'message': f"Competitor points added"}),200)
    return (jsonify({'error': f"Error adding competitor points"}),400)

@competitor_views.route('/api/competitors/points/deduction', methods=['PUT'])
def remove_points_competitor_action():
    data = request.form

    id = int(data['competitor_id'])
    points = int(data['points'])
    
    if points < 0:
        return (jsonify({'error': f"Error adding competitor points"}),400)

    response = remove_competitor_overall_points(id, points)
    if response:
        return (jsonify({'message': f"Competitor points removed"}),200)
    return (jsonify({'error': f"Error removing competitor points"}),400)

@competitor_views.route('/api/competitors/delete/<int:competitor_id>', methods=['DELETE'])
def delete_competitor_action(competitor_id):
    response = delete_competitor(competitor_id)

    if response:
           return (jsonify({'message': f"Competitor deleted"}),200)
    return (jsonify({'error': f"Error deleting competitor"}),400)
