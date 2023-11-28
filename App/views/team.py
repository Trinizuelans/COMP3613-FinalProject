from flask import Blueprint, jsonify, request

from App.controllers import (
   get_all_teams_json,
   get_team_Byname,
   create_team,
   delete_team,
   get_competitor_by_username,
   add_competitor_to_team,
   remove_competitor_to_team,
   update_team_score
)

team_views = Blueprint('team_views', __name__, template_folder='../templates')


#return the json list of teams fetched from the db
@team_views.route('/teams', methods=['GET'])
def get_teams():
    teams = get_all_teams_json()
    return (jsonify(teams),200) 

#get team by name
@team_views.route('/teams/<string:name>', methods=['GET'])
def get_team_name(name):
    print(name)
    team = get_team_Byname(name)
    if not team:
        return jsonify({'error': 'team not found'}), 404 
    return (jsonify([team.toDict()]),200)


#create a team in the db
@team_views.route('/teams', methods=['POST'])
def make_team():
    data = request.json
    response = create_team(data['team_name'])
    if response:
        return (jsonify({'message': f"team created"}), 201)
    return (jsonify({'error': f"error creating team"}),500)

#remove a team from the db
@team_views.route('/teams', methods=['DELETE'])
def erase_team():
    data = request.json
    response = delete_team(data['team_name'])
    if response:
        return (jsonify({'message': f"team removed"}), 200)
    return (jsonify({'error': f"error removing team"}),500)

#add competitor to a team 
@team_views.route('/teams/competitor', methods=['PUT'])
def add_team_competitor():
    data = request.json
    competitor = get_competitor_by_username(data['competitor_name'])
    response = add_competitor_to_team(competitor, data['team_name'])
    if response:
        return (jsonify({'message': f"team member added"}), 200)
    return (jsonify({'error': f"error adding team member"}),500)

#remove competitor from a team 
@team_views.route('/teams/competitor', methods=['DELETE'])
def remove_team_competitor():
    data = request.json
    competitor = get_competitor_by_username(data['competitor_name'])
    response = remove_competitor_to_team(competitor, data['team_name'])
    if response:
        return (jsonify({'message': f"team member removed"}), 200)
    return (jsonify({'error': f"error removing team member"}),500)

#add score to a team in db
@team_views.route('/teams/score', methods=['PUT'])
def add_team_score():
    data = request.json
    response = update_team_score(data['competition_name'],data['team_name'], data['score'])
    if response:
        return (jsonify({'message': f"team score added"}), 200)
    return (jsonify({'error': f"error adding team score"}),500)

      
    