from . import contest_data
from .models import Team, get_contest

def eval_score(contest_id):
    problems = contest_data["contests"][contest_id]["problems"]
    teams = Team.query.filter_by(contest_id=contest_id).all()
    team_count = len(teams)
    stats_dict = {}

    for team in teams:
        team.add_to_score(-team.get_score())

    for problem in problems:
        solved_count = 0
        problem_max_points = int(problems[problem]["points"])
        # count how many teams have solved a problem
        for team in teams:

            if team.get_problem_status(problem):
                solved_count += 1

        if solved_count == 0:
            added_score = problem_max_points
        else:
            # subtract a maximum of half the possible points if every team has solved the problem
            added_score = int(problem_max_points - (problem_max_points * (solved_count - 1)) / (team_count * 2))

        # give each team the new points
        for team in teams:
            if team.get_problem_status(problem):
                team.add_to_score(added_score)

        stats_dict[problem] = [solved_count, added_score]

    get_contest(contest_id).update_stats(stats_dict)







def sort_teams_score(contest_id):
    teams = Team.query.filter_by(contest_id=contest_id).all()
    return sorted(teams, key=lambda x: x.get_score(), reverse=True)






