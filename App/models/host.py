from App.database import db

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organizationName =  db.Column(db.String, nullable=False, unique=True)

    def __init__(self,name):
        self.organizationName = name

    def toDict(self):
        res = {
            "id": self.id,
            "name": self.organizationName
        }
        return res
    
