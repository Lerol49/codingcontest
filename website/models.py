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


    # {"<problem_name>": [<bool: solved>, <int: count>], "probl..."}
    stats = db.Column(db.JSON, default={})


    def _commit_stats(self):
        attributes.flag_modified(self, "stats")
        db.session.commit()

    def increment_tries_counter(self, problem_name):
        self.stats[problem_name][1] += 1
        self._commit_stats()

    def set_submission_result(self, problem_name, result):
        self.stats[problem_name][0] = result
        self._commit_stats()

    def get_tries_count(self, problem_name) -> int:
        return self.stats[problem_name][1]

    def get_problem_status(self, problem_name) -> bool:
        return self.stats[problem_name][0]

    def give_access_to_problem(self, problem_name):
        self.stats[problem_name] = [False, 0]


    def give_access_to_contest(self, contest_name):
        from . import contest_data

        if contest_name in self.contest_data:
            print(f"User {self.username} is already registered in {contest_name}")
            return

        self.contest_data[contest_name] = None
        attributes.flag_modified(self, "contest_data")

        for problem_name in contest_data["contests"][contest_name]["problems"]:
            self.give_access_to_problem(problem_name)

        self._commit_stats()


    def _join_team(self, contest_name, team_name):
        self.contest_data[contest_name] = team_name
        attributes.flag_modified(self, "contest_data")
        db.session.commit()


    def get_team(self, contest_id):
        team = Team.query.filter((Team.name == self.contest_data[contest_id]) & (Team.contest_id == contest_id)).first()
        return team

    def count_solves(self, contest_id):
        from . import contest_data
        count = 0
        for problem_name in contest_data["contests"][contest_id]["problems"]:
            if self.get_problem_status(problem_name):
                count += 1
        return count



class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    contest_id = db.Column(db.String())
    members = db.Column(db.JSON, default={"names": []})
    password = db.Column(db.String())
    stats = db.Column(db.JSON, default={})


    def _commit(self, location):
        attributes.flag_modified(self, location)
        db.session.commit()

    def get_members(self):
        """returns List of all User Objects associated with the team"""
        members_objects = []
        for member in self.members["names"]:
            members_objects.append(User.query.filter_by(username=member).first())
        return members_objects


    def add_member(self, user):
        if user.get_team(self.contest_id) is None:
            self.members["names"].append(user.username)
            self._commit("members")
            user._join_team(self.contest_id, self.name)

    def increment_tries_counter(self, problem_id):
        self.stats[problem_id][1] += 1
        self._commit("stats")

    def set_submission_result(self, problem_name, result):
        self.stats[problem_name][0] = result
        self._commit("stats")

    def get_tries_count(self, problem_name) -> int:
        return self.stats[problem_name][1]

    def get_problem_status(self, problem_name) -> bool:
        return self.stats[problem_name][0]

    def get_score(self):
        return self.stats["_score"]

    def add_to_score(self, additional_score):
        self.stats["_score"] += additional_score
        self._commit("stats")


class Contest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.String())
    stats = db.Column(db.JSON, default={})


    def update_stats(self, stats_dict):
        self.stats = stats_dict
        attributes.flag_modified(self, "stats")
        db.session.commit()



def get_contest(contest_id):
    return Contest.query.filter_by(contest_id=contest_id).first()

def get_teams(contest_id):
    return Team.query.filter_by(contest_id=contest_id).all()

def init_Contests():
    from . import contest_data
    Contest.query.delete()
    contests = contest_data["contests"]
    for contest_name in contests:
        contest = Contest(contest_id=contest_name)
        db.session.add(contest)
        db.session.commit()
        from .leaderboard import eval_score
        eval_score(contest_name)

def create_new_team(creator, team_name, contest_id, hashed_password):
    """creates, returnes and saves new Team Object.
    To add a new member call team.add_member(user).
    """
    from . import contest_data

    stats = {"_score": 0}
    for problem in contest_data["contests"][contest_id]["problems"]:
        stats[problem] = [False, 0]

    team = Team(name=team_name, contest_id=contest_id, stats=stats, password=hashed_password)
    db.session.add(team)
    db.session.commit()
    team.add_member(creator)

    return team


def create_new_user(username, password):
    """creates, returnes and saves new User Object"""
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return new_user





