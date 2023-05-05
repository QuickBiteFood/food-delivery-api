from os import getenv

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Foods(db.Model):

    __tablename__ = "foods"

    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String, nullable=False)
    description = db.Column("description", db.String, nullable=True)
    price = db.Column("price", db.Float, nullable=False)
    image_url = db.Column("image_url", db.String, nullable=True)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "image_url": f"http://{request.host}/static/{self.image_url}"
        }


@app.route("/foods", methods=["GET"])
def home_root_handler():
    foods = Foods.query.all()

    return jsonify([i.serialize for i in foods])


if __name__ == "__main__":
    app.run(debug=True)