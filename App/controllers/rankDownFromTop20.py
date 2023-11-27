from App.database import db
from App.models.rankDownFromTop20 import RankDownFromTop20


def create_rankDownListener(leaderboard_id):
    
    try:
        listener = RankDownFromTop20(leaderboard_id);
        if listener:
            db.session.add(listener)
            db.session.commit()
            return listener
        return None

    except Exception:
        db.session.rollback()


