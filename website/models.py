from . import db
from flask_login import UserMixin
from sqlalchemy.orm import attributes



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())

    rights = db.Column(db.String(), default="normalo")  # or "admin"

    # {"<allowed_contest_name>": "<group>", "<allow..."}
    # "group" is set to None per default
    contest_data = db.Column(db.JSON, default={})


    # {"<problem_name>": {"solved": False, "tries": 0}, "probl..."}
    problems_data = db.Column(db.JSON, default={})


    def _commit_problems_data(self):
        attributes.flag_modified(self, "problems_data")
        db.session.commit()

    def increment_tries_counter(self, problem_name):
        self.problems_data[problem_name][1] += 1
        self._commit_problems_data()

    def mark_solved(self, problem_name):
        self.problems_data[problem_name][0] = True
        self._commit_problems_data()

    def mark_unsolved(self, problem_name):
        self.problems_data[problem_name][0] = False
        self._commit_problems_data()

    def get_tries_count(self, problem_name) -> int:
        return self.problems_data[problem_name][1]

    def get_problem_status(self, problem_name) -> bool:
        return self.problems_data[problem_name][0]

    def get_team(self, contest_name):
        return self.contest_data[contest_name]


    def give_access_to_problem(self, problem_name):
        self.problems_data[problem_name] = [False, 0]
        self._commit_problems_data()


    def give_access_to_contest(self, contest_name):
        from . import contest_data

        if contest_name in self.contest_data:
            print(f"User {self.username} is already registered in {contest_name}")
            return

        self.contest_data[contest_name] = None
        attributes.flag_modified(self, "contest_data")
        db.session.commit()

        for problem_name in contest_data["contests"][contest_name]["problems"]:
            self.give_access_to_problem(problem_name)


    def join_team(self, contest_name, group_name):
        if contest_name in self.contest_data:
            self.contest_data[contest_name] = group_name

        attributes.flag_modified(self, "contest_data")
        db.session.commit()


def get_users_of_team(team, contest_name):
    users = db.session.query(User).filter(User.contest_data[contest_name] is not None).all()
    return users






