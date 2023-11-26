from App.models import Competition
from App.database import db

def create_competition(name, host_id, location, date, competitionScore):
    
    newcomp = Competition(name = name, host_id=host_id, location = location, date=date, competitionScore=competitionScore)

    try:
        db.session.add(newcomp)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False
    return True

def get_all_competitions():
    return Competition.query.all()

def get_all_competitions_json():
    competition = Competition.query.all()

    if not competition:
        return []
    else:
        return [comp.toDict() for comp in competition]


def get_competition_by_id(id):
    competition = Competition.query.get(id)
    return competition

def remove_competition(competition_id):
    competition = Competition.query.get(competition_id)
    
    if competition:
        try:
            db.session.delete(competition)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
    return False

def modify_competition(competition_id, new_name, new_host_id, new_location, new_date, new_competition_score):
    competition = Competition.query.get(competition_id)
    
    if competition:
        try:
            # Update competition attributes
            competition.name = new_name
            competition.host_id = new_host_id
            competition.location = new_location
            competition.date = new_date
            competition.competition_score = new_competition_score

            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
    return Fals


# def add_results(user_id, comp_id, rank):
#     Comp = Competition.query.get(comp_id)
#     user = User.query.get(user_id)
        
        
            
#     if user and Comp:
#         compParticipant = UserCompetition(user_id = user.id, comp_id = Comp.id, rank=rank)


#         try:
#             db.session.add(compParticipant)
#             db.session.commit 
#             print("successfully added user to comp")
#             return True
#         except Exception as e:
#             db.session.rollback()
#             print("error adding to comp")
#             return False
#         return False



# def get_competition_users(comp_id):
#     Comp = get_competition_by_id(comp_id)
    

#     if Comp:
#         compUsers = Comp.participants
#         Participants = [User.query.get(part.user_id) for part in compUsers]
#         print(Participants)
