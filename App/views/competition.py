from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from.index import index_views

from App.controllers import (
    # create_user,
    # jwt_authenticate, 
    # get_all_users,
    # get_all_users_json,
    jwt_required,
    create_competition,
    get_all_competitions_json,
    get_competition_by_id,
    get_competition_by_name,
    remove_competition,
    modify_competition,
    add_team,
    remove_team
    # add_results,
    # get_user_rankings,
    # add_user_to_comp
)


comp_views = Blueprint('comp_views', __name__, template_folder='../templates')


#return the json list of competitions fetched from the db
@comp_views.route('/competitions', methods=['GET'])
def get_competitons():
    competitions = get_all_competitions_json()
    return (jsonify(competitions),200) 

#get competition by id
@comp_views.route('/competitions/<int:id>', methods=['GET'])
def get_competition(id):
    print(id)
    competition = get_competition_by_id(id)
    if not competition:
        return jsonify({'error': 'competition not found'}), 404 
    return (jsonify([competition.toDict()]),200)

#get competition by name
@comp_views.route('/competitions/<string:name>', methods=['GET'])
def get_competition_name(name):
    print(name)
    competition = get_competition_by_name(name)
    if not competition:
        return jsonify({'error': 'competition not found'}), 404 
    return (jsonify([competition.toDict()]),200)

#add new competition to the db
@comp_views.route('/competitions', methods=['POST'])
def add_new_comp():
    data = request.json
    response = create_competition(data['name'], data['host_id'], data['location'], data['date'], data['competitionScore'])
    if response:
        return (jsonify({'message': f"competition created"}), 201)
    return (jsonify({'error': f"error creating competition"}),500)

#remove a competition from the db
@comp_views.route('/competitions', methods=['DELETE'])
def remove_comp():
    data = request.json
    response = remove_competition(data['name'])
    if response:
        return (jsonify({'message': f"competition removed"}), 200)
    return (jsonify({'error': f"error removing competition"}),500)

#update a competiton in the db
@comp_views.route('/competition', methods=['PUT'])
def update_comp():
    data = request.json
    response = modify_competition(data['id'], data['name'], data['host_id'], data['location'], data['date'], data['competitionScore'])
    if response:
        return (jsonify({'message': f"competition updated"}), 200)
    return (jsonify({'error': f"error updating competition"}),500)

#add a team to competition in db
@comp_views.route('/competition/team', methods=['PUT'])
def add_team_comp():
    data = request.json
    response = add_team(data['competition_name'], data['team_name'])
    if response:
        return (jsonify({'message': f"competition added team"}), 200)
    return (jsonify({'error': f"error adding team to competition"}),500)

#remove a team from competition in db
@comp_views.route('/competition/team', methods=['DELETE'])
def remove_team_comp():
    data = request.json
    response = remove_team(data['competition_name'], data['team_name'])
    if response:
        return (jsonify({'message': f"competition removed team"}), 200)
    return (jsonify({'error': f"error removing team to competition"}),500)

# @comp_views.route('/competitions/user', methods=['POST'])
# def add_comp_user():
#     data = request.json
#     response = add_new_user()
#     if response: 
#         return (jsonify({'message': f"user added to competition"}),201)
#     return (jsonify({'error': f"error adding user to competition"}),500)



# @comp_views.route('/competitions/results', methods=['POST'])
# def add_comp_results():
#     data = request.json
#     response = add_user_to_comp(data['user_id'],data['comp_id'], data['rank'])
#     if response:
#         return (jsonify({'message': f"results added successfully"}),201)
#     return (jsonify({'error': f"error adding results"}),500)

# @comp_views.route('/rankings/<int:id>', methods =['GET'])
# def get_rankings(id):
#     ranks = get_user_rankings(id)
#     return (jsonify(ranks),200)




