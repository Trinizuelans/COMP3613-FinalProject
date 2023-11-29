from App.database import db



def get_rankListener_json(list):
    if not list:
        return []
    
    listeners = [listener.get_json() for listener  in list]
    return listeners