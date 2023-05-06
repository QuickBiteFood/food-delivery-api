from flask import Blueprint

root_blueprint = Blueprint('root_blueprint', __name__)

import src.routes.foods
import src.routes.employees
import src.routes.orders

food_routes = src.routes.foods.routes
employees_routes = src.routes.employees.routes
order_routes = src.routes.orders.routes

routes = food_routes + employees_routes + order_routes

for root in routes:
    root_blueprint.add_url_rule(
        root['rule'],
        endpoint=root.get('endpoint', None),
        view_func=root['view_func'],
        **root.get('options', {}))