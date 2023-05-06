import app
from flask import request


class Foods(app.db.Model):
    id = app.db.Column("id", app.db.Integer, primary_key=True)
    title = app.db.Column("title", app.db.String, nullable=False)
    description = app.db.Column("description", app.db.String, nullable=True)
    price = app.db.Column("price", app.db.Float, nullable=False)
    image_url = app.db.Column("image_url", app.db.String, nullable=True)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "image_url": f"http://{request.host}/static/images/foods/{self.image_url}"
        }
