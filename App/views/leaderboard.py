from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from App.controllers import (
    get_leaderboard_json,
    show_competitor_leaderboard_rankings,
    competitor_list_to_json



)


leaderboard_views = Blueprint('leaderboard_views', __name__, template_folder='../templates')


@leaderboard_views.route('/api/leaderboard', methods=['GET'])
def get_leaderboard_action():
    leaderboard= get_leaderboard_json(1)
    if leaderboard:
        return (leaderboard,200)

    return (jsonify({'error': f"Leaderboard not found"}),400)

@leaderboard_views.route('/api/leaderboard/rankings', methods=['GET'])
def get_leaderboard_rankings_action():
    ranking = competitor_list_to_json(show_competitor_leaderboard_rankings())
    if ranking:
        return(ranking,200)
    
    return (jsonify({'error': f"Error retrieving leaderboard rankings"}),400)