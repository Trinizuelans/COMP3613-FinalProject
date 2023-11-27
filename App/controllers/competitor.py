from operator import attrgetter
from App.models.competitor import Competitor
from App.database import db


def create_competitor(username, email, password):
    newCompetitor = Competitor(username=username,email = email, password=password)
    try:

        db.session.add(newCompetitor)
        db.session.commit()
        update_rank()
        return newCompetitor
    except Exception:
        db.session.rollback()
        return newCompetitor

def get_competitor_by_username(username):
    return Competitor.query.filter_by(username=username).first()

def get_competitor(id):
    return Competitor.query.get(id)

def get_all_competitors():
    return Competitor.query.all()

def get_all_competitors_json():
    competitors = Competitor.query.all()
    if not competitors:
        return []
    competitors = [competitor.get_json() for competitor in competitors]
    return competitors

def update_competitor(id, username, email):
    competitor = get_competitor(id)
    if competitor:
        competitor.username = username
        competitor.email = email
        db.session.add(competitor)
        db.session.commit()
        return competitor
    return None

def add_competitor_overall_points(id,points):
    
    try:
        competitor = get_competitor(id)
        if competitor:
            competitor.points = competitor.points + points
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
            competitor.points = competitor.points - points
            db.session.add(competitor)
            db.session.commit()
            update_rank()
            return competitor
        return None
    
    except Exception:
        db.session.rollback()

def delete_competitor(id):
    try:
        competitor = get_competitor(id)

        if competitor:
            db.session.delete(competitor)
            db.session.commit()
            return True
        return False
    
    except Exception:
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
    
    except Exception:
        db.session.rollback()

