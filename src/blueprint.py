from functools import wraps

import jwt
from flask import Blueprint, request, jsonify

from app import app

import src.models.employees as employees_model

root_blueprint = Blueprint('root_blueprint', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({"message": "Токен не указан"}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = employees_model.Employees.query.filter_by(public_id=data['public_id']).first()

        except:
            return jsonify({
                "message": "Срок действия токена истек или токен невалиден"
            }), 401

        return f(current_user, *args, **kwargs)

    return decorated

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