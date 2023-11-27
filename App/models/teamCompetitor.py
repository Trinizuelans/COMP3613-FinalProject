from App.database import db

class CompetitorTeamAssociation(db.Model):
    __tablename__ = 'competitor_team_association'
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), primary_key=True)
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'), primary_key=True)