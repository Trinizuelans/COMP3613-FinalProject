from App.database import db

class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(120), nullable=False)
    team_score = db.Column(db.Integer, nullable=True)
    competitors = db.relationship("Competitor", secondary="competitor_team_association", backref="team")
   
    def __init__(self, team_name):
        self.team_name = team_name
        self.team_score = 0
        
    def get_json(self):
        return{
            'team_id': self.team_id,
            'team_name': self.team_name,
            'team_score': self.team_score,
            'competitors': self.competitors
        }
        
    def toDict(self):
        team = {
            "team_id": self.team_id,
            "team_name": self.team_name,
            "team_score": self.team_score,
            "competitors": [comp.toDict() for comp in self.competitors]
        }
        return team
            
            
            
            
            

    
    