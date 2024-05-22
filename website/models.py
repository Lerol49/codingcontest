from . import db
from flask_login import UserMixin



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))



class Problems(db.Model):
    username = db.Column(db.String(15), unique=True, primary_key=True)
    pizza_distribution_problem = db.Column(db.JSON, default={"passed": False, "tries": 0})

