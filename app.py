from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src.blueprint import root_blueprint

app.register_blueprint(root_blueprint)


@app.route("/", methods=["GET"])
def get_home():
    return "Simple food API"
