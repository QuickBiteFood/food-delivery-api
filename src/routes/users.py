from flask import request, jsonify

import src.models.users as users_model
from src.utils import generate_message_response

import jwt
from src.blueprint import token_required
from app import app, db
from datetime import datetime, timedelta


def auth_user():
    login = request.form.get("login")
    password = request.form.get("password")

    user = users_model.Users.query.filter_by(login=login).first()

    if not user:
        return generate_message_response("Такого пользователя не существует", 403)

    if user.check_password(password):
        token = jwt.encode({
            "public_id": user.public_id,
            "exp": datetime.utcnow() + timedelta(app.config["TOKEN_EXP"])
        }, app.config["SECRET_KEY"])

        return jsonify({"token": token})

    return generate_message_response("Неверный логин или пароль", 404)


def register_user():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    phone = request.form.get("phone")
    email = request.form.get("email")
    login = request.form.get("login")
    password = request.form.get("password")

    if firstname is None or phone is None or login is None or password is None:
        return generate_message_response("Заполните все требуемые данные для добавления пользователя", 404)

    employee = users_model.Users(firstname, phone, login, password, lastname=lastname, email=email)

    try:
        db.session.add(employee)
        db.session.commit()

    except:
        db.session.rollback()
        db.session.flush()

        return generate_message_response("Ошибка при регистрации пользователя", 404)

    return generate_message_response("Пользователь был успешно добавлен")


@token_required
def get_current_user(current_user):
    return jsonify(current_user.safe_serialized)


routes = [
    {
        "rule": "/register/user",
        "view_func": register_user,
        "options": {
            "methods": ["POST"]
        }
    },

    {
        "rule": "/auth/user",
        "view_func": auth_user,
        "options": {
            "methods": ["POST"]
        }
    },

    {
        "rule": "/get/user/current",
        "view_func": get_current_user,
        "options": {
            "methods": ["GET"]
        }
    }
]