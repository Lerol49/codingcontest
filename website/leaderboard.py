from . import contest_data
from .models import Team

def eval_score(contest_id):
    problems = contest_data["contests"][contest_id]["problems"]
    teams = Team.query.filter_by(contest_id=contest_id).all()

    

