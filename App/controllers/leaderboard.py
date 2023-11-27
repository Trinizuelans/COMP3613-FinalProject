from sqlalchemy import desc
from App.database import db
from App.models.competitor import Competitor
from App.models.leaderboard import Leaderboard


def create_leaderboard(leaderboard_id):
    newLeaderboard = Leaderboard(leaderboard_id= leaderboard_id)
    try:
        db.session.add(newLeaderboard)

        db.session.commit()
        return newLeaderboard

    except Exception:
        db.session.rollback()
        return newLeaderboard
    
def get_leaderboard(id):
    return Leaderboard.query.filter_by(leaderboard_id = id).first()

def populate_top20_leaderboards():
    leaderboard  = get_leaderboard(1)
    try:
        if leaderboard:
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
            
            db.session.add(leaderboard)
            db.session.commit()
            print("Prev------------------------------")
            print(leaderboard.prev_top20competitors)
            print("Curr------------------------------")
            print(leaderboard.top20competitors)
    except Exception:
        db.rollback()



    

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


def show_competitor_leaderboard_rankings():
    leaderboard = get_leaderboard(1);
    if leaderboard:
        sorted_competitors = Competitor.query.filter_by(leaderboard_id=leaderboard.leaderboard_id).order_by(desc(Competitor.overall_points)).all()
        return sorted_competitors
    return None