from os import getenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SECRET_KEY"] = "123"
app.config["TOKEN_EXP"] = 120  # minutes

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src.blueprint import root_blueprint

app.register_blueprint(root_blueprint)


@app.route("/", methods=["GET"])
def handle_home_root():
    return jsonify({"message": "Простая Restfull API для системы доставки еды"})