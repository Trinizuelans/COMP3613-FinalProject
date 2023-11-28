from App.models import Team
from App.database import db
from App.controllers.competitionTeam import get_competition_team
from App.controllers.competitor import add_competitor_overall_points
from App.models.competition import Competition



def create_team (team_name):
    new_team = Team(team_name)
    
    try:
        db.session.add(new_team)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False
    return True

def get_team_Byid(id):
    return Team.query.get(id)

def get_team_Byname(name):
    return Team.query.filter_by(team_name=name).first()

def get_all_teams():
    return Team.query.all()

def get_all_teams_json():
    teams = Team.query.all()

    if not teams:
        return []
    else:
        return [team.toDict() for team in teams]
    
def delete_team(team_id):
    team = Team.query.get(team_id)
    
    if not team:
        print("Team not found")
        return False
    
    if team:
        try:
            db.session.delete(team)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
    return False

def add_competitor_to_team(competitor, team_name):
    team = Team.query.filter_by(team_name=team_name).first()
    
    if not team:
        print("Team not found")
        return False
    
    add = False
    
    if team:
      try: 
        team.competitors.append(competitor)
        add = True
      except Exception as e:
          print("Unable to add team memeber")
          return False

    if add == True:
        try:
           db.session.add(team)
           db.session.commit()
           return True
        except Exception as e:
            db.session.rollback()
        return False 
    
def remove_competitor_to_team(competitor, team_name):
    team = Team.query.filter_by(team_name=team_name).first()
    
    if not team:
        print("Team not found")
        return False
     
    remove = False
    
    if team:
      try: 
        team.competitors.remove(competitor)
        remove = True
      except Exception as e:
          print("Unable to remove team memeber")
          return False

    if remove == True:
        try:
           db.session.add(team)
           db.session.commit()
           return True
        except Exception as e:
            db.session.rollback()
        return False 
    
def update_team_score(competition_name, team_name, score):
    team = Team.query.filter_by(team_name=team_name).first()
    
    if not team:
        print("Team not found")
        return False
    
    if len(team.competitors) == 0:
       print("No members in team. Can't add score")
       return False
   
    competition = Competition.query.filter_by(name=competition_name).first()
    
    if not competition:
        print("Competition not found")
        return False
    
    competitionTeam = get_competition_team(competition.id, team.team_id)
    
    if not competitionTeam:
        print(team.team_name + " is not competing in " + competition.name )
        return False
    
    add = False
    
    if competitionTeam:
       try:
            if team.team_score == competition.competitionScore:
                print("Team has already received the max number of points for competition")
                return False 
            if team.team_score < competition.competitionScore:
               team.team_score += score
               add = True
               diff = 0
               if team.team_score > competition.competitionScore:
                   diff = team.team_score - competition.competitionScore
                   team.team_score = competition.competitionScore
            for comp in team.competitors:
                added = add_competitor_overall_points(comp.id, score - diff)
       except Exception as e:
          print("Unable to add score to team and team memebers ")
          return False 
          
    if add == True:
       try:
           db.session.add(team)
           db.session.commit()
           return True
       except Exception as e:
            db.session.rollback()
       return False  

        