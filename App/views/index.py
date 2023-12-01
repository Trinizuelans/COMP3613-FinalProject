from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user, create_competition, create_team, add_competitor_to_team, create_competitor, add_team, create_leaderboard
from App.controllers.admin import create_admin

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()

    a = create_admin("ricky","ricky@mail.com","rickypass")

    leaderboard = create_leaderboard(1)
    for x in range (25):
        lastperson = create_competitor("rick" + str(x) ,"rick"+ str(x) + "@mail.com","rickpass")



    b = create_competition("Comp1", 1, "Arima","28-11-2023", 10)
    c = create_competition("Comp2", 1, "Arima","28-11-2023", 10)
    d = create_team("Team1")
    rick = create_competitor("Rick", "rick@mail.com", "rickpass")
    sally = create_competitor("Sally", "sally@mail.com", "sallypass")
    e = add_competitor_to_team(rick,"Team1")
    f = add_team("Comp1","Team1")
    return jsonify(message='The Database has been successfully initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/healthcheck', methods=['GET'])
def health():
    return jsonify({'status':'healthy'})

@index_views.route('/reset', methods=['GET'])
def delete():
    db.drop_all()
    return jsonify(message='db reset!')