from app import db
from uuid import uuid4


class Orders(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    public_id = db.Column("public_id", db.String, nullable=False, default=str(uuid4()))

    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
    delivery_address = db.Column("delivery_address", db.String, nullable=False)
    payment_type = db.Column("payment_type", db.String, nullable=True)

    is_finished = db.Column("is_finished", db.Boolean, nullable=False, default=False)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "public_id": self.public_id,
            "user_id": self.user_id,
            "delivery_address": self.delivery_address,
            "is_finished": self.is_finished
        }


class OrdersCarts(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    order_id = db.Column("order_id", db.Integer, db.ForeignKey("orders.id"))
    food_id = db.Column("food_id", db.Integer, db.ForeignKey("foods.id"))
