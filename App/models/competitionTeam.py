from App.database import db

class CompetitionTeamAssociation(db.Model):
    __tablename__ = 'competition_team_association'
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), primary_key=True)

    def get_json(self):
        return{
            'competition_id': self.competition_id,
            'team_id': self.team_id
        }