from App.models import Host
from App.models import db

def create_host(id,name):
    newHost = Host(id,name)
    try:
        db.session.add(newHost)
        db.session.commit()
        return newHost
    except Exception:
        db.session.rollback()
        return newHost
    
    def get_host_by_id(id):
        return Host.query.get(id)
    
    def get_host_by_organizationName(name):
        return Host.query.filter_by(username=username).first()