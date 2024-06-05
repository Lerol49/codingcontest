from flask import request
from flask_login import current_user

from website.contest.compare_output_file import compare_output_file
from website.models import User, get_users_of_team




def handle_task_submission(contest_name, problem_name, control_filename):
    user = User.query.filter_by(username=current_user.username).first()


    # handles upload try
    if request.method == "POST":
        return _add_try(user, contest_name, problem_name, control_filename)


    # displays no feedback if no tries have been made
    # elif user.get_tries_count(problem_name) == 0:
    #     return ""

    # display previous result
    else:
        if user.get_problem_status(problem_name):
            return "richtig"
        else:
            return "falsch"



def _add_try(user, contest_name, problem_name, control_filename):
    submit_file = request.files["file"]
    if submit_file:

        submission_result = compare_output_file(submit_file, control_filename)
        team = user.get_team(contest_name)

        if team is None:
            _add_try_individual(user, problem_name, submission_result)

        else:
            _add_try_team(team, contest_name, problem_name, submission_result)

        if submission_result:
            return "richtig!"
        else:
            return "falsch!"



def _get_previous_result(user, problem_name):
    user.get_problem_status(problem_name)

def _add_try_individual(user, problem_name, submission_result):
    user.increment_tries_counter(problem_name)
    _save_submission_result(user, problem_name, submission_result)


def _add_try_team(team, contest_name, problem_name, submission_result):
    team_members = get_users_of_team(team, contest_name)
    for user in team_members:
        _add_try_individual(user, problem_name, submission_result)


def _save_submission_result(user, problem_name, submission_result):
    if submission_result:
        user.mark_solved(problem_name)
    else:
        user.mark_unsolved(problem_name)




# currently not used
def save_uploaded_file(submit_file):
    from flask import current_app as app
    from werkzeug.utils import secure_filename
    import os
    submit_filename = secure_filename(submit_file.filename)
    submit_filepath = os.path.join(app.config["UPLOAD_DIRECTORY"], submit_filename)
    submit_file.save(submit_filepath)





