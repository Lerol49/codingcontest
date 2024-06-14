from . import contest_data
from .models import Team

def eval_score(contest_id):
    problems = contest_data["contests"][contest_id]["problems"]
    teams = Team.query.filter_by(contest_id=contest_id).all()
    team_count = len(teams)

    for team in teams:
        team.add_to_score(-team.get_score())

    for problem in problems:
        solved_count = 0
        problem_max_points = problems[problem]["points"]
        # count how many teams have solved a problem
        for team in teams:

            if team.get_problem_status(problem):
                solved_count += 1

        # subtract a maximum of half the possible points if every team has solved the problem
        added_score = int(problem_max_points - (problem_max_points * (solved_count - 1)) / (team_count * 2))

        # give each team the new points
        for team in teams:
            if team.get_problem_status(problem):
                team.add_to_score(added_score)




def sort_teams_score(contest_id):
    teams = Team.query.filter_by(contest_id=contest_id).all()
    return sorted(teams, key=lambda x: x.get_score(), reverse=True)





