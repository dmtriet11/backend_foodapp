from flask import Blueprint
food_bp = Blueprint('food', __name__)

# Import các route để đăng ký vào blueprint
# ⚠️ CRITICAL: Import routes with specific paths BEFORE generic <variable> routes
# This ensures /restaurants/nearby matches before /restaurants/<place_id>
from . import search_route
from . import list_all_foods_route
from . import restaurants_route  # /restaurants (exact match)
from . import restaurants_extra_route  # /restaurants/nearby, /restaurants/category/<id>
from . import get_restaurants_by_ids_route  # /restaurants/details-by-ids
from . import detail_route  # /restaurants/<place_id> - MUST BE LAST to avoid catching specific routes
from . import direction_route
from . import reviews_route
from . import food_search_route
from . import category_route