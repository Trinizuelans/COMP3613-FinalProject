import traceback
from sqlalchemy import desc
from App.controllers.rankDownFromTop20 import create_rankDownListener
from App.controllers.rankSwitchInTop20 import create_switchListener
from App.controllers.rankUpToTop20 import create_rankUpListener
from App.database import db
from App.models.competitor import Competitor
from App.models.leaderboard import Leaderboard
from App.models import *

def create_leaderboard(leaderboard_id):
    newLeaderboard = Leaderboard(leaderboard_id= leaderboard_id)
    try:
        db.session.add(newLeaderboard)
        db.session.commit()

        init_listeners(leaderboard_id)
        return newLeaderboard

    except Exception:
        db.session.rollback()
        return newLeaderboard

def init_listeners(leaderboard_id):
    
    try:
        leaderboard = get_leaderboard(leaderboard_id)
        if leaderboard:
            leaderboard.subscribe(create_rankDownListener(leaderboard_id))
            leaderboard.subscribe(create_rankUpListener(leaderboard_id))
            leaderboard.subscribe(create_switchListener(leaderboard_id))
            db.session.add(leaderboard)
            db.session.commit()

    except Exception:
        db.session.rollback()


        
def get_leaderboard(id):
    return Leaderboard.query.filter_by(leaderboard_id = id).first()

def get_leaderboard_json(id):
    leaderboard = Leaderboard.query.filter_by(leaderboard_id = id).first()
    return leaderboard.get_json()


def populate_top20_leaderboards():
    leaderboard  = get_leaderboard(1)
    try:
        if leaderboard:
            leaderboard.prev_top20competitors = leaderboard.top20competitors
            db.session.add(leaderboard)
            db.session.commit()
            leaderboard.top20competitors = []
            competitors = (
                Competitor.query.filter_by(leaderboard_id=leaderboard.leaderboard_id)  # Assuming 'leaderboard_id' is a field in the Competitor model
                .order_by(desc(Competitor.overall_points))  # Order by overall_score in descending order
                .limit(20)  # Limit the query to retrieve only the top 20 competitors
                .all()
            )
            

            for competitor in competitors:
                leaderboard.top20competitors.append(competitor)

                curr_competitor = Competitor.query.get(competitor.id)

                

                if competitor.id in leaderboard.rank_switch:
                    # Update the current rank for the competitor
                    leaderboard.rank_switch[competitor.id]['previous_rank'] = leaderboard.rank_switch[competitor.id]['current_rank']
                    leaderboard.rank_switch[competitor.id]['current_rank'] = curr_competitor.rank
                else:
                    # Add a new entry for the competitor in the dictionary
                    leaderboard.rank_switch[competitor.id] = {
                        'competitor_id': competitor.id,
                        'previous_rank': None,  # Assuming 'rank' is a field in the Competitor model
                        'current_rank': curr_competitor.rank  # Assuming the rank is the position in the list
                    }
        
            for r in leaderboard.rank_switch:
                curr_competitor = Competitor.query.get(r)
                leaderboard.rank_switch[r]['current_rank'] = curr_competitor.rank

            
            db.session.add(leaderboard)
            db.session.commit()
            notify_subscribers(leaderboard)
            
    except Exception as e:
        traceback.print_exc()
        db.rollback()



def notify_subscribers(leaderboard):
    for rankListener in leaderboard.rankListeners:
        rankListener.update(leaderboard.prev_top20competitors,leaderboard.top20competitors, leaderboard.rank_switch)

def show_competitor_leaderboard_rankings():
    leaderboard = get_leaderboard(1);
    if leaderboard:
        sorted_competitors = Competitor.query.filter_by(leaderboard_id=leaderboard.leaderboard_id).order_by(desc(Competitor.overall_points)).all()
        return sorted_competitors
    return None

