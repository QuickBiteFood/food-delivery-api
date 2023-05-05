from app import db
from flask import request


class Foods(db.Model):
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
            "image_url": f"http://{request.host}/static/images/foods/{self.image_url}"
        }
