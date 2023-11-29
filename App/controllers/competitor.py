from operator import attrgetter
from App.models.competitor import Competitor
from App.database import db
import App.controllers.leaderboard as leaderboard
import App.controllers.messageInbox as mi

import App.controllers.messageInbox as mi

def create_competitor(username, email, password):
    newCompetitor = Competitor(username=username,email = email, password=password)
    try:
        
        db.session.add(newCompetitor)
        db.session.commit()

        mi.create_message_Inbox(newCompetitor.id)
        update_rank()

        return newCompetitor
    
    except Exception:
        db.session.rollback()
        return newCompetitor

def get_competitor_by_username(username):
    return Competitor.query.filter_by(username=username).first()

def get_competitor(id):
    return Competitor.query.get(id)

def get_competitor_json(id):
    c =  Competitor.query.get(id)
    return c.get_json()

def get_all_competitors():
    return Competitor.query.all()

def get_all_competitors_json():
    competitors = Competitor.query.all()
    if not competitors:
        return []
    competitors = [competitor.get_json() for competitor in competitors]
    return competitors

def update_competitor(id, username, email,password):
    competitor = get_competitor(id)
    if competitor:
        competitor.username = username
        competitor.email = email
        competitor.password = password
        db.session.add(competitor)
        db.session.commit()
        return competitor
    return None

def add_competitor_overall_points(id,points):
    
    try:
        competitor = get_competitor(id)
        if competitor:
            competitor.overall_points = competitor.overall_points + points
            db.session.add(competitor)
            db.session.commit()
            update_rank()
            return competitor
        return None
    except Exception:
        db.session.rollback()

def  remove_competitor_overall_points(id,points):
    try:
        competitor = get_competitor(id)
        if competitor:
            competitor.overall_points = competitor.overall_points - points

            if (competitor.overall_points < 0):
                competitor.overall_points = 0

            db.session.add(competitor)
            db.session.commit()
            update_rank()
            return competitor
        return None
    
    except Exception:
        db.session.rollback()

def delete_competitor(id):
    
    competitor = get_competitor(id)
    try:

        if competitor:

            message_inbox = mi.delete_message_inbox(id)
            if message_inbox:
                db.session.delete(competitor)
                db.session.commit()
                update_rank()
                return True
        return False
    
    except Exception:
        print("lo")
        db.session.rollback()

def update_rank():
    
    try:
        
        competitors = get_all_competitors()
        sorted_competitors = sorted(competitors, key=attrgetter('overall_points'), reverse=True)
        rank = 1
        
        for competitor in sorted_competitors:
            competitor.rank = rank
            rank += 1
            db.session.add(competitor)
            db.session.commit()
        
        leaderboard.populate_top20_leaderboards()
    
    except Exception:
        db.session.rollback()

