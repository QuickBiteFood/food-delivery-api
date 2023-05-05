import src.models.employees as employees_model
from flask import jsonify


""" DEV FEATURE - Not secure without JWT System """
def get_employees():
    employees = employees_model.Employees.query.all()
    employees_serialized = []

    if len(employees) == 0:
        return "Данных о сотрудниках не существует"

    for employee in employees:
        employees_serialized.append(employee.serialize)

    return jsonify(employees_serialized)


def get_employee_by_id(id):
    employee = employees_model.Employees.query.get(id)

    if employee is None:
        return "Такого сотрудника не существует", 404

    return jsonify(employee)

def add_employee():
    ...


routes = [
    {
        "rule": "/get/user",
        "view_func": get_employees,
        "options": {
            "methods": ["GET"]
        }
    },

    {
        "rule": "/get/user/<id>",
        "view_func": get_employee_by_id,
        "options": {
            "methods": ["GET"]
        }
    }
]
