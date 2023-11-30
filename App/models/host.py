from App.database import db

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organizationName =  db.Col
    #competitions = db.relationship("CompetitionHost", lazy=True, backref=db.backref("competitions"), cascade="all, delete-orphan")

    def __init__(self,id ,name):
        self.id = id
        self.name = name

    def toDict(self):
        res = {
            "id": self.id,umn(db.String, nullable=False, unique=True)
    #website = db.Column(db.String, nullable=True)
    
            "name": self.organizationName,
            #"website": self.website
        }
        return res
    