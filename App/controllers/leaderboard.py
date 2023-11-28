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

def populate_top20_leaderboards():
    leaderboard  = get_leaderboard(1)
    try:
        if leaderboard:
            # rank_switch = {}
            leaderboard.prev_top20competitors = leaderboard.top20competitors
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
                # print(curr_competitor)
                leaderboard.rank_switch[r]['current_rank'] = curr_competitor.rank

            
            db.session.add(leaderboard)
            db.session.commit()
            notify_subscribers(leaderboard)
            # print("notify")
            # print("Prev------------------------------")
            # print(leaderboard.prev_top20competitors)
            # print("Curr------------------------------")
            # print(leaderboard.top20competitors)
            # print("\n")
            # print(leaderboard.rank_switch)
            
    except Exception:
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

# def populate_top20_competitors(leaderboard_id):
#         leaderboard = get_leaderboard(leaderboard_id)
        
#         if leaderboard.competitors:
#             # Clear the existing top 20 competitors
#             leaderboard.prevtop20competitors = leaderboard.top20competitors
#             leaderboard.top20competitors = []

#             # Fetch the top 20 competitors based on overall_points
#             top_20_competitors = (
#                 Competitor.query.filter_by(leaderboard_id=leaderboard.leaderboard_id)
#                 .order_by(desc(Competitor.overall_points))
#                 .limit(20)
#                 .all()
#             )

#             # Add the top 20 competitors to the leaderboard's top20competitors attribute
#             leaderboard.top20competitors.extend(top_20_competitors)
#             print(leaderboard.top20competitors)
#             print("Top 20 competitors added to the leaderboard successfully.")



# def populate_top20_competitors(leaderboard_id):
#     leaderboard = get_leaderboard(leaderboard_id)

#     if leaderboard:
#         # Fetch the top 20 competitors based on overall_points
#         top_20_competitors = (
#             Competitor.query.filter_by(leaderboard_id=leaderboard.leaderboard_id)
#             .order_by(Competitor.overall_points.desc())
#             .limit(20)
#             .all()
#         )
#         # Update the top 20 competitors list in the leaderboard
#         # leaderboard.top20competitors = top_20_competitors
#         # db.session.commit()  # Make sure to commit the changes to the database
#         print("********************")
#         print(top_20_competitors)
#         print("Top 20 competitors added to the leaderboard successfully.")


