import src.models.employees as employees_model
from flask import jsonify, request
from app import db

""" DEV FEATURE - Not secure without JWT System """
def get_employees():
    employees = employees_model.Employees.query.all()
    employees_serialized = []

    if len(employees) == 0:
        return "Данных о сотрудниках не существует"

    for employee in employees:
        employees_serialized.append(employee.safe_serialized)

    return jsonify(employees_serialized)


def get_employee_by_id(id):
    employee = employees_model.Employees.query.get(id)

    if employee is None:
        return "Такого сотрудника не существует", 404

    return jsonify(employee.safe_serialized)


def register_employee():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    phone = request.form.get("phone")
    email = request.form.get("email")
    login = request.form.get("login")
    password = request.form.get("password")

    if firstname is None or phone is None or login is None or password is None:
        return "Заполните все требуемые данные для добавления сотрудника", 404

    employee = employees_model.Employees(firstname, phone, login, password, lastname=lastname, email=email)

    try:
        db.session.add(employee)
        db.session.commit()

    except:
        db.session.rollback()
        db.session.flush()

        return "Ошибка при добавлении сотрудника", 404

    return "Сотрудник был успешно добавлен"


def auth_employee():
    login = request.form.get("login")
    password = request.form.get("password")

    employee = employees_model.Employees.query.filter_by(login=login).first()

    if not employee:
        return "Такого пользователя не существует"

    if employee.check_password(password):
        employee_data = {
            "firstname": employee.firstname,
            "lastname": employee.lastname,
            "phone": employee.phone,
            "email": employee.email
        }

        return jsonify(employee_data)

    return "Неверный логин или пароль", 404


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
    },

    {
        "rule": "/register/employee",
        "view_func": register_employee,
        "options": {
            "methods": ["POST"]
        }
    },

    {
        "rule": "/auth/employee",
        "view_func": auth_employee,
        "options": {
            "methods": ["POST"]
        }
    }
]
