# blue prints are imported 
# explicitly instead of using *
# from .user import user_views
from .index import index_views
from .auth import auth_views
from .competition import comp_views
from .team import team_views
from .competitor import competitor_views
from .leaderboard import leaderboard_views


views = [index_views,auth_views, comp_views, team_views, competitor_views,leaderboard_views]
# blueprints must be added to this list