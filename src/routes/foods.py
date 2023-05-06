from functools import wraps

import jwt

import src.models.foods as food_model
import src.models.employees as employees_model

from app import db, app
from flask import jsonify, request, render_template
from uuid import uuid1


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

def get_foods():
    foods = food_model.Foods.query.all()

    foods_serialized = []

    for food in foods:
        foods_serialized.append(food.serialize)

    return jsonify(foods_serialized)


def get_food_by_id(id: int):
    food = food_model.Foods.query.get(id)

    if food is None:
        return "Такого товара не существует", 404

    return jsonify(food.serialize)

@token_required
def delete_food(current_employee, id: int):
    try:
        food = food_model.Foods.query.get(id)

        if food is None:
            return "Такого товара не существует", 404

        food_model.Foods.query.filter_by(id=id).delete()
        db.session.commit()

    except Exception as db_error:
        db.session.rollback()
        db.session.flush()

        return "Ошибка во время выполнения операции", 404

    return "Товар был успешно удален", 200


def add_food():
    title = request.form.get("title")
    description = request.form.get("description")
    price = request.form.get("price")
    food_image = request.files.get("food_image")

    if title is None or description is None or price is None or food_image is None:
        return render_template("error.html", error_message="Ошибка добавления еды", error_body="Для подробностей просмотрите документацию", documentation_link="https://clck.ru/34Lf2T"), 404

    try:
        image_name = f"{str(uuid1())}.{food_image.filename.split('.')[1]}"
        food_image.save(f"static/images/foods/{image_name}")

        food = food_model.Foods(title=title, description=description, price=price, image_url=image_name)

        db.session.add(food)
        db.session.commit()

    except Exception as db_error:
        db.session.rollback()
        db.session.flush()

        return "Во время добавления товара произошла ошибка", 404

    return "Товар был успешно добавлен!"


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
