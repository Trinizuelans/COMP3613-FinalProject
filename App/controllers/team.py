from App.models import Team
from App.database import db

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
    
def update_team_score(team_name, score):
    team = Team.query.filter_by(team_name=team_name).first()
    
    if not team:
        print("Team not found")
        return False
    
    if len(team.competitors) == 0:
       print("No members in team. Can't add score")
       return False
    
    add = False
    
    if team:
        try:
            team.team_score += score
            add = True
            for comp in team.competitors:
                added = update_team_memeber_overall_score(comp, score)
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
    

def update_team_memeber_overall_score(member, score):
    member.overall_points += score
    try:
        db.session.add(member)
        db.session.commit()
        return True
    except Exception as e:
            db.session.rollback()
    return False 
        