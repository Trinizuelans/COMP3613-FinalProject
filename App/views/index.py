from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user, create_competition, create_team, add_competitor_to_team, create_competitor

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_competition("Comp1", 1, "Arima","28-11-2023", 10)
    create_user('bob',"bob@mail.com", 'bobpass')
    create_team("Team1")
    rick = create_competitor("Rick", "rick@mail.com", "rickpass")
    add_competitor_to_team(rick,"Team1")
    return jsonify(message='The Database has been successfully initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/healthcheck', methods=['GET'])
def health():
    return jsonify({'status':'healthy'})