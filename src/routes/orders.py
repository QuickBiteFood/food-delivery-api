import src.models.orders as orders_models
import src.models.foods as foods_models
import src.models.employees as employees_model
import src.models.users as users_model

from flask import jsonify, request
from src.blueprint import token_required

from app import db
from src.utils import generate_message_response


@token_required
def get_orders(current_user):
    employees = employees_model.Employees.query.all()
    user_is_employee = False

    for employee in employees:
        if current_user.id == employee.user_id:
            user_is_employee = True

    if not user_is_employee:
        return generate_message_response(f"Пользователь не является сотрудником", 200)

    orders = orders_models.Orders.query.all()
    orders_carts = orders_models.OrdersCarts.query.all()

    orders_serialized = []

    for order in orders:
        cart = []
        user = users_model.Users.query.filter_by(id=order.user_id).first()

        for order_cart in orders_carts:
            if order_cart.order_id == order.id:
                food = foods_models.Foods.query.filter_by(id=order_cart.food_id).first()
                cart.append({
                    **food.serialize,
                    "count": order_cart.food_count
                })

        orders_serialized.append(
            {
                **user.safe_serialized,
                **order.serialize,
                "cart": cart
            }
        )

    return jsonify(orders_serialized)


@token_required
def get_current_user_orders(current_user):
    orders = orders_models.Orders.query.filter_by(user_id=current_user.id).all()

    orders_serialized = []

    for order in orders:
        orders_serialized.append(order.serialize)

    return jsonify(orders_serialized)


@token_required
def add_order(current_user):
    order_data = request.get_json()

    user_id = current_user.id
    delivery_address = order_data.get("delivery_address")
    payment_type = order_data.get("payment_type")

    cart = order_data.get("cart")

    if not user_id or not delivery_address:
        return generate_message_response("Не хватает данных для создания заказа", 404)

    if not cart:
        return generate_message_response("Невозможно создать заказ с пустой корзиной товаров", 404)

    new_order = orders_models.Orders(user_id=user_id, delivery_address=delivery_address, payment_type=payment_type)

    try:
        db.session.add(new_order)
        db.session.commit()

        new_order_cart_models = []

        for cart_item in cart:
            cart_food_item = orders_models.OrdersCarts(order_id=new_order.id, food_id=cart_item["id"], food_count=cart_item["count"])
            new_order_cart_models.append(cart_food_item)

        db.session.add_all(new_order_cart_models)
        db.session.commit()

    except:
        db.session.rollback()
        db.session.flush()

        return generate_message_response("Во время создания заказа произошла ошибка", 404)

    return generate_message_response("Заказ был успешно принят")


@token_required
def set_order_as_finished(current_user, id):
    employees = employees_model.Employees.query.all()
    user_is_employee = False

    for employee in employees:
        if current_user.id == employee.user_id:
            user_is_employee = True

    if not user_is_employee:
        return generate_message_response(f"Пользователь не является сотрудником", 200)

    order = orders_models.Orders.query.get(id)
    order.is_finished = True

    if not order:
        return generate_message_response(f"Заказ под номером {order.id} не существует", 200)

    try:
        db.session.commit()

    except:
        db.session.rollback()
        db.session.flush()

        return generate_message_response("Во время завершения заказа произошла ошибка", 404)

    return generate_message_response("Заказ был успешно завершен", 200)


routes = [
    {
        "rule": "/get/order",
        "view_func": get_orders,
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
        "rule": "/get/current/user/orders",
        "view_func": get_current_user_orders,
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