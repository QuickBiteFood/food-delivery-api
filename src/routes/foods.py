from functools import wraps
import jwt

import src.models.foods as food_model
from src.blueprint import token_required

from app import db
from flask import jsonify, request
from uuid import uuid1

from src.utils import generate_message_response


def get_foods():
    foods = food_model.Foods.query.all()

    foods_serialized = []

    for food in foods:
        foods_serialized.append(food.serialize)

    return jsonify(foods_serialized)


def get_food_by_id(id: int):
    food = food_model.Foods.query.get(id)

    if food is None:
        return generate_message_response("Такого товара не существует", 403)

    return jsonify(food.serialize)


@token_required
def delete_food(current_employee, id: int):
    employees = employees_model.Employees.query.all()
    user_is_employee = False

    for employee in employees:
        if current_user.id == employee.user_id:
            user_is_employee = True

    if not user_is_employee:
        return generate_message_response(f"Пользователь не является сотрудником", 200)

    try:
        food = food_model.Foods.query.get(id)

        if food is None:
            return generate_message_response("Такого товара не существует", 403)

        food_model.Foods.query.filter_by(id=id).delete()
        db.session.commit()

    except:
        db.session.rollback()
        db.session.flush()

        return generate_message_response("Ошибка во время выполнения операции", 500)

    return generate_message_response("Товар был успешно удален")


@token_required
def add_food(current_employee):
    employees = employees_model.Employees.query.all()
    user_is_employee = False

    for employee in employees:
        if current_user.id == employee.user_id:
            user_is_employee = True

    if not user_is_employee:
        return generate_message_response(f"Пользователь не является сотрудником", 200)

    title = request.form.get("title")
    description = request.form.get("description")
    price = request.form.get("price")
    food_image = request.files.get("food_image")

    if not title or not description or not price or not food_image:
        return generate_message_response("Недостаточно данных для добавление еды", 404)

    try:
        image_name = f"{str(uuid1())}.{food_image.filename.split('.')[1]}"
        food_image.save(f"static/images/foods/{image_name}")

        food = food_model.Foods(title=title, description=description, price=price, image_url=image_name)

        db.session.add(food)
        db.session.commit()

    except Exception:
        db.session.rollback()
        db.session.flush()

        return generate_message_response("Во время добавления товара произошла ошибка", 500)

    return generate_message_response("Товар был успешно добавлен")


routes = [
    {
        "rule": "/get/food",
        "view_func": get_foods,
        "options": {
            "methods": ["GET"]
        }
    },

    {
        "rule": "/get/food/<id>",
        "view_func": get_food_by_id,
        "options": {
            "methods": ["GET"]
            }
    },

    {
        "rule": "/delete/food/<id>",
        "view_func": delete_food,
        "options": {
            "methods": ["DELETE"]
        }
    },

    {
        "rule": "/add/food",
        "view_func": add_food,
        "options": {
            "methods": ["POST"]
        }
    }
]
