from . import db
from flask_login import UserMixin



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))

    groups = db.Column(db.JSON)

    rights = db.Column(db.String(), default="normalo")  # or "admin"
    problem_access = db.Column(db.JSON)
    solved_problems = db.Column(db.JSON)


    def get_user_data(self):
        """returns dict with keys 'username', 'rights', 'problem_access' and
        'solved_problems'."""
        return {"username": self.username, "rights": self.rights,
                "problem_access": self.problem_access, "solved_problems": self.solved_problems}


class Problems(db.Model):
    username = db.Column(db.String(15), unique=True, primary_key=True)
    pizza_distribution_problem = db.Column(db.JSON, default={"passed": False, "tries": 0})

