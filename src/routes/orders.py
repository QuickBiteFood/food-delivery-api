from functools import wraps
import jwt

import src.models.orders as orders_models
import src.models.foods as foods_models
import src.models.employees as employees_model

from flask import jsonify, request

from app import app, db


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
            return "Во время генерации токена произошла ошибка", 401

        return f(current_user, *args, **kwargs)

    return decorated


@token_required
def get_orders():
    orders = orders_models.Orders.query.all()
    orders_carts = orders_models.OrdersCarts.query.all()

    orders_serialized = []

    for order in orders:
        cart = []

        for order_cart in orders_carts:
            if order_cart.order_id == order.id:
                food = foods_models.Foods.query.filter_by(id=order_cart.food_id).first()

                cart.append(food.serialize)

        orders_serialized.append(
            {
                **order.serialize,
                "cart": cart
            }
        )

    return jsonify(orders_serialized)


@token_required
def get_order_by_id(id):
    order = orders_models.Orders.query.get(id)
    order_cart = orders_models.OrdersCarts.query.filter_by(order_id=order.id).all()
    order_cart_foods = []

    for cart_item in order_cart:
        food = foods_models.Foods.query.filter_by(id=cart_item.food_id).first()
        order_cart_foods.append(food.serialize)

    order_serialized = {
        **order.serialize,
        "cart": order_cart_foods
    }

    return jsonify(order_serialized)


@token_required
def get_not_finished_orders():
    orders = orders_models.Orders.query.filter_by(is_finished=False)
    orders_carts = orders_models.OrdersCarts.query.all()

    orders_serialized = []

    for order in orders:
        cart = []

        for order_cart in orders_carts:
            if order_cart.order_id == order.id:
                food = foods_models.Foods.query.filter_by(id=order_cart.food_id).first()

                cart.append(food.serialize)

        orders_serialized.append(
            {
                **order.serialize,
                "cart": cart
            }
        )

    return jsonify(orders_serialized)


@token_required
def add_order():
    order_data = request.json

    user_name = order_data["user_name"]
    user_phone = order_data["user_phone"]
    delivery_address = order_data["delivery_address"]
    payment_type = order_data["payment_type"]

    cart = order_data["cart"]

    if user_phone is None or delivery_address is None:
        return "Не хватает данных для создания заказа"

    if cart is None:
        return "Невозможно создать заказ с пустой корзиной товаров"

    new_order = orders_models.Orders(user_name=user_name, user_phone=user_phone, delivery_address=delivery_address, payment_type=payment_type)

    try:
        db.session.add(new_order)
        db.session.commit()

        new_order_cart_models = []

        for cart_item in cart:
            cart_food_item = orders_models.OrdersCarts(order_id=new_order.id, food_id=cart_item["food_id"])
            new_order_cart_models.append(cart_food_item)

        db.session.add_all(new_order_cart_models)
        db.session.commit()

    except:
        db.session.rollback()
        db.session.flush()

        return "Во время создания заказа произошла ошибка"

    return "Заказ был успешно принят"


@token_required
def set_order_as_finished(id):
    order = orders_models.Orders.query.get(id)
    order.is_finished = True

    if not order:
        return f"Заказ под номером {order.id} не существует"

    try:
        db.session.commit()

    except:
        db.session.rollback()
        db.session.flush()

        return "Во время завершения заказа произошла ошибка"

    return "Заказ был успешно завершен"


routes = [
    {
        "rule": "/get/order",
        "view_func": get_orders,
        "options": {
            "methods": ["GET"]
        }
    },

    {
        "rule": "/get/not_finished/order",
        "view_func": get_not_finished_orders,
        "options": {
            "methods": ["GET"]
        }
    },

    {
        "rule": "/set/finished/order/<id>",
        "view_func": set_order_as_finished,
        "options": {
            "methods": ["GET"]
        }
    },

    {
        "rule": "/get/order/<id>",
        "view_func": get_order_by_id,
        "options": {
            "methods": ["GET"]
        }
    },

    {
        "rule": "/add/order",
        "view_func": add_order,
        "options": {
            "methods": ["POST"]
        }
    }
]