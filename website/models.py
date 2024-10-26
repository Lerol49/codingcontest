from . import db
from flask_login import UserMixin
from sqlalchemy.orm import attributes
from werkzeug.security import generate_password_hash, check_password_hash


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

    def has_access_to(self, problem_or_contest_id):
        return problem_or_contest_id in self.stats.keys() or problem_or_contest_id in self.contest_data.keys()


    def give_access_to_contest(self, contest_name):
        from . import contest_data

        if contest_name in self.contest_data:
            print(f"User {self.username} is already registered in {contest_name}")
            return

        self.contest_data[contest_name] = None
        attributes.flag_modified(self, "contest_data")

        if contest_data["contests"][contest_name]["progression"] is False:
            for problem_name in contest_data["contests"][contest_name]["problems"]:
                self.give_access_to_problem(problem_name)
        else:
            for problem_name in contest_data["contests"][contest_name]["unlock_tree"]["base"]:
                self.give_access_to_problem(problem_name)

        self._commit_stats()

    def give_access_to_next_problems(self, contest_name, solved_problem):
        from . import contest_data

        if contest_data["contests"][contest_name]["progression"] is False:
            return

        new_problems = contest_data["contests"][contest_name]["unlock_tree"][solved_problem]
        for problem in new_problems:
            if not self.has_access_to(problem):
                self.give_access_to_problem(problem)
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
            if self.has_access_to(problem_name) and self.get_problem_status(problem_name):
                count += 1
        return count

    def change_username(self, new_username):
        if User.query.filter_by(username=new_username).first() is None:
            self.username = new_username
            db.session.commit()
            return True
        else:
            return False

    def change_password(self, new_password, alleged_current_password):
        if check_password_hash(self.password, alleged_current_password):
            new_password = generate_password_hash(new_password)
            self.password = new_password
            db.session.commit()
            return True
        else:
            return False




class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    contest_id = db.Column(db.String())
    members = db.Column(db.JSON, default={"member_id": []})
    password = db.Column(db.String())
    stats = db.Column(db.JSON, default={})


    def _commit(self, location):
        attributes.flag_modified(self, location)
        db.session.commit()

    def get_members(self):
        """returns List of all User Objects associated with the team"""
        members_objects = []
        for member_id in self.members["member_id"]:
            members_objects.append(User.query.filter_by(id=member_id).first())
        return members_objects


    def add_member(self, user):
        if user.get_team(self.contest_id) is None:
            self.members["member_id"].append(user.id)
            self._commit("members")
            user._join_team(self.contest_id, self.name)

    def increment_tries_counter(self, problem_id):
        self.stats[problem_id][1] += 1
        self._commit("stats")

    def set_submission_result(self, problem_name, result):
        self.stats[problem_name][0] = result
        self._commit("stats")

    def give_access_to_problem(self, problem_name):
        self.stats[problem_name] = [False, 0]

    def get_tries_count(self, problem_name) -> int:
        return self.stats[problem_name][1]

    def get_problem_status(self, problem_name) -> bool:
        return self.stats[problem_name][0]

    def get_score(self):
        return self.stats["_score"]

    def add_to_score(self, additional_score):
        self.stats["_score"] += additional_score
        self._commit("stats")

    def give_others_access_to_next_problems(self, user, contest_name, solved_problem):
        members = self.get_members()
        for member in members:
            if member == user:
                continue
            member.give_access_to_next_problems(contest_name, solved_problem)


class Contest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.String())
    stats = db.Column(db.JSON, default={})
    running = db.Column(db.Boolean, default=False)
    end_time = db.Column(db.Integer, default=0)


    def update_stats(self, stats_dict):
        self.stats = stats_dict
        attributes.flag_modified(self, "stats")
        db.session.commit()

    def set_end_time(self, new_time):
        self.end_time = new_time
        db.session.commit()

    def set_running(self, value):
        self.running = value
        db.session.commit()

    def get_running(self):
        return self.running

    def get_end_time(self):
        return self.end_time



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


def update_stats_on_new_problem():
    from . import contest_data
    for contest in contest_data["contests"]:
        for problem_id in contest_data["contests"][contest]["problems"]:
            # users_in_need = User.query.filter(User.stats[problem_id] is None).all()
            # teams_in_need = Team.query.filter(Team.stats[problem_id] is None).all()
            for user in User.query.all():
                if user.stats.get(problem_id) is None and user.has_access_to(contest):
                    user.give_access_to_problem(problem_id)
                    user._commit_stats()
            for team in Team.query.all():
                if team.stats.get(problem_id) is None:
                    team.give_access_to_problem(problem_id)
                    team._commit("stats")




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





