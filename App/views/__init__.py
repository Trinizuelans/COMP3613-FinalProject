# blue prints are imported 
# explicitly instead of using *
# from .user import user_views
from .index import index_views
# from .auth import auth_views
# from .competition import comp_views


views = [index_views] 
# blueprints must be added to this list