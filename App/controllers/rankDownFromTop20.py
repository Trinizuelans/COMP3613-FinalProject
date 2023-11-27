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


# def update(prev_top20competitors,top20competitors):

#     if (prev_top20competitors != top20competitors):
#         deranked_competitors = set(prev_top20competitors) - set(top20competitors)
    
#     print(deranked_competitors)