from flask import Blueprint

root_blueprint = Blueprint('root_blueprint', __name__)

from src.routes.foods import routes as food_routes
from src.routes.employees import routes as employees_routes

routes = food_routes + employees_routes

for root in routes:
    root_blueprint.add_url_rule(
        root['rule'],
        endpoint=root.get('endpoint', None),
        view_func=root['view_func'],
        **root.get('options', {}))