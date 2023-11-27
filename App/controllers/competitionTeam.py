from App.database import db
from App.models import CompetitionTeamAssociation

def get_all_competitionTeams():
     compteam = CompetitionTeamAssociation.query.all()
     if not compteam:
        return []
     compteaminfo = [c.get_json() for c in compteam]
     return compteaminfo
  
def get_competition_team(competition_id, team_id):
   return CompetitionTeamAssociation.query.filter_by(competition_id=competition_id, team_id=team_id).first()

