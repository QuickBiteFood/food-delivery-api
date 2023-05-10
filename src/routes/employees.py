from datetime import datetime, timedelta

import src.models.employees as employees_model
import src.models.users as users_model
from flask import jsonify, request
from app import app, db
import jwt

from src.utils import generate_message_response


def auth_employee():
    login = request.form.get("login")
    password = request.form.get("password")

    user = users_model.Users.query.filter_by(login=login).first()
    employees = employees_model.Employees.query.all()

    if not user:
        return generate_message_response("Такого пользователя не существует", 200)

    if user.check_password(password):
        user_is_employee = False

        for employee in employees:
            if employee.user_id == user.id:
                user_is_employee = True

        if user_is_employee:
            token = jwt.encode({
                "public_id": user.public_id,
                "exp": datetime.utcnow() + timedelta(app.config["TOKEN_EXP"])
            }, app.config["SECRET_KEY"])

            return jsonify({"token": token})

        else:
            return generate_message_response("Пользователь не является сотрудником", 200)

    return generate_message_response("Неверный логин или пароль", 200)


routes = [
    {
        "rule": "/auth/employee",
        "view_func": auth_employee,
        "options": {
            "methods": ["POST"]
        }
    }
]