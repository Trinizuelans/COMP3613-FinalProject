from App.database import db
from App.models.rankSwitchInTop20 import RankSwitchInTop20

def create_switchListener(leaderboard_id):
    
    try:
        listener = RankSwitchInTop20(leaderboard_id);
        if listener:
            db.session.add(listener)
            db.session.commit()
            return listener
        return None

    except Exception:
        db.session.rollback()


# def update(prev_top20competitors,top20competitors):
#     print("Rank Switch message")