# routes/food/detail_route.py
from flask import jsonify
from routes.food import food_bp

from core.database import RESTAURANTS, MENUS_BY_RESTAURANT_ID

@food_bp.route('/restaurants/<string:place_id>', methods=['GET'])
def get_restaurant_detail(place_id):
	"""Lấy chi tiết nhà hàng và menu của nhà hàng đó theo Google Places ID."""
	# 1. Tìm nhà hàng có ID tương ứng
	restaurant = RESTAURANTS.get(place_id)
	
	if not restaurant:
		return jsonify({"error": "Restaurant not found"}), 404

	# 2. Lấy menu tương ứng (nếu có)
	menu_items = MENUS_BY_RESTAURANT_ID.get(place_id, [])

	# 3. Gộp dữ liệu lại
	detail = {
		**restaurant,
		"menu": menu_items
	}

	return jsonify(detail)