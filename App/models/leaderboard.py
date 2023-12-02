from flask import jsonify
from App.database import db

# This is the Publisher for the Observer Design Pattern
class Leaderboard(db.Model):
    leaderboard_id = db.Column(db.Integer, primary_key=True)
    competitors = db.relationship('Competitor', backref='leaderboard', lazy=True)
    prev_top20competitors = None
    top20competitors = None
    rank_switch = None
    rankListeners = db.relationship('RankListener', backref='leaderboard', lazy=True)

    def __init__(self,leaderboard_id):
        self.leaderboard_id = leaderboard_id
        if self.prev_top20competitors is None:  # Check if prev_top20competitors is None
            self.prev_top20competitors = []
        
        self.top20competitors = []
        self.rankListeners = []
        if self.rank_switch is None:
            self.rank_switch = {}

    def get_json(self):
        from App.controllers import competitor_list_to_json,get_rankListener_json
        return{
            'leaderboard_id': self.leaderboard_id,
            'rankListeners': get_rankListener_json(self.rankListeners)
        }

    def subscribe(self,rankListener):
        try:
            self.rankListeners.append(rankListener)
            db.session.add()
            db.session.commit()
        except Exception:
            db.session.rollback()

    #notify_subscribers moved to leaderboard_controllers

    def __repr__(self):
        return f"Leaderboard(leaderboard_id={self.leaderboard_id})"