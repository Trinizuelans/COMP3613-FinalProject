from App.database import db
from App.models import CompetitionTeamAssociation

def get_all_competitionTeams():
     compteam = CompetitionTeamAssociation.query.all()
     if not compteam:
        return []
     compteaminfo = [c.get_json() for c in compteam]
     return compteaminfo

