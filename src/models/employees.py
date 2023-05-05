from app import db


class Employees(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    firstname = db.Column("firstname", db.String, nullable=False)
    lastname = db.Column("lastname", db.String, nullable=True)

    phone = db.Column("phone", db.String, nullable=False)
    email = db.Column("email", db.String, nullable=True)

    login = db.Column("login", db.String, nullable=False)
    password = db.Column("password", db.String, nullable=False)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "phone": self.phone,
            "email": self.email,
            "login": self.login,
            "password": self.password
        }