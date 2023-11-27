from App.database import db

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(120), nullable=False, unique=True)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120), nullable=False)
    competitionScore = db.Column(db.Integer, nullable=False)
    teams = db.relationship("Team", secondary="competition_team_association", backref="competition")


    def __init__(self, name, host_id, location, date, competitionScore):
        self.name = name
        self.host_id = host_id
        self.location = location
        self.date = date
        self.competitionScore = competitionScore

    
    def get_json(self):
        return{
            'id': self.id,
            'name': self.name,
            'host_id': self.host_id,
            'location': self.location,
            'date': self.date,
            'competitionScore': self.competitionScore, 
            'teams': self.teams   
        }



    def toDict(self):
        comp = {
            "id": self.id,
            "name": self.name,
            "host_id": self.host_id,
            "location": self.location,
            "date": self.date,
            "competitionScore": self.competitionScore,
            "teams": [team.toDict() for team in self.teams]
            
           
            #"participants": [participant.toDict() for participant in self.participants]
        } 
        return comp
