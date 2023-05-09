from datetime import datetime, timedelta

import src.models.employees as employees_model
from flask import jsonify, request
from app import app, db
import jwt
from src.blueprint import token_required

from src.utils import generate_message_response


@token_required
def get_employees(current_employee):
    employees = employees_model.Employees.query.all()
    employees_serialized = []

    if len(employees) == 0:
        return generate_message_response("Данных о сотрудниках не существует", 403)

    for employee in employees:
        employees_serialized.append(employee.safe_serialized)

    return jsonify(employees_serialized)


@token_required
def get_employee_by_id(current_employee, id: int):
    employee = employees_model.Employees.query.get(id)

    if employee is None:
        return generate_message_response("Такого сотрудника не существует", 403)

    return jsonify(employee.safe_serialized)


def register_employee():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    phone = request.form.get("phone")
    email = request.form.get("email")
    login = request.form.get("login")
    password = request.form.get("password")

    if firstname is None or phone is None or login is None or password is None:
        return generate_message_response("Заполните все требуемые данные для добавления сотрудника", 404)

    employee = employees_model.Employees(firstname, phone, login, password, lastname=lastname, email=email)

    try:
        db.session.add(employee)
        db.session.commit()

    except:
        db.session.rollback()
        db.session.flush()

        return generate_message_response("Ошибка при добавлении сотрудника", 404)

    return generate_message_response("Сотрудник был успешно добавлен")


def auth_employee():
    login = request.form.get("login")
    password = request.form.get("password")

    employee = employees_model.Employees.query.filter_by(login=login).first()

    if not employee:
        return generate_message_response("Такого пользователя не существует", 403)

    if employee.check_password(password):
        token = jwt.encode({
            "public_id": employee.public_id,
            "exp": datetime.utcnow() + timedelta(app.config["TOKEN_EXP"])
        }, app.config["SECRET_KEY"])

        return jsonify({"token": token})

    return generate_message_response("Неверный логин или пароль", 404)


routes = [
    {
        "rule": "/get/employee",
        "view_func": get_employees,
        "options": {
            "methods": ["GET"]
        }
    },

    {
        "rule": "/get/employee/<id>",
        "view_func": get_employee_by_id,
        "options": {
            "methods": ["GET"]
        }
    }
]