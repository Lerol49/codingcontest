from . import db
from flask_login import UserMixin
from sqlalchemy.orm import attributes



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())

    groups = db.Column(db.JSON)

    rights = db.Column(db.String(), default="normalo")  # or "admin"

    contest_access = db.Column(db.JSON, default={"contests": []})

    problems_data = db.Column(db.JSON, default={})


    def _commit(self):
        attributes.flag_modified(self, "problems_data")
        db.session.commit()

    def set_current_problem(self, problem_name):
        self.current_problem_name = problem_name

    def add_try(self):
        self.problems_data[self.current_problem_name]["tries"] += 1
        self._commit()

    def mark_solved(self):
        self.problems_data[self.current_problem_name]["solved"] = True
        self._commit()

    def mark_unsolved(self):
        self.problems_data[self.current_problem_name]["solved"] = False
        self._commit()

    def get_tries_count(self) -> int:
        return self.problems_data[self.current_problem_name]["tries"]

    def get_problem_status(self) -> bool:
        return self.problems_data[self.current_problem_name]["solved"]


    def give_access_to_problem(self, problem_name):
        self.problems_data[problem_name] = {"solved": False, "tries": 0}
        self._commit()

    def give_access_to_contest(self, contest_name):
        from . import contest_data

        self.contest_access["contests"].append(contest_name)
        attributes.flag_modified(self, "contest_access")
        db.session.commit()

        for problem_name in contest_data["contests"][contest_name]["problems"]:
            self.give_access_to_problem(problem_name)








