from flask import Blueprint

root_blueprint = Blueprint('root_blueprint', __name__)

from src.routes import routes as main_roots

for root in main_roots:
    root_blueprint.add_url_rule(
        root['rule'],
        endpoint=root.get('endpoint', None),
        view_func=root['view_func'],
        **root.get('options', {}))