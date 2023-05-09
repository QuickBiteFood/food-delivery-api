from app import db


class Employees(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, unique=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"))

    @property
    def serialize(self):
        return {
            "id": self.id
        }

    @property
    def safe_serialized(self):
        return {
            "id": self.id
        }