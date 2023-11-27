from App.database import db
from App.models.rankUpToTop20 import RankUpToTop20

def create_rankUpListener(leaderboard_id):
    
    try:
        listener = RankUpToTop20(leaderboard_id);
        if listener:
            db.session.add(listener)
            db.session.commit()
            return listener
        return None

    except Exception:
        db.session.rollback()


# def update(prev_top20competitors,top20competitors):
#     print("Rank Up message")