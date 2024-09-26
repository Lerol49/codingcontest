from flask import request, flash
from flask_login import current_user
from website.models import User

from website.contest.compare_output_file import compare_output_file, compare_output_number
from website.leaderboard import eval_score
from website.form import NumberSubmission


def handle_task_submission(contest_name, problem_name, control_filename):
    user = User.query.filter_by(id=current_user.id).first()
    team = user.get_team(contest_name)



    # handles upload try
    if request.method == "POST":
        submission_result = False
        if request.files.get("file") is not None:
            submit_file = request.files["file"]
            if submit_file:
                submission_result = compare_output_file(submit_file, control_filename)
                _add_try(user, team, problem_name, submission_result)

        elif "submission_number" in request.form:
            form = NumberSubmission()
            if form.validate_on_submit():
                submission_result = compare_output_number(form.submission_number.data, control_filename)
                _add_try(user, team, problem_name, submission_result)

        eval_score(contest_name)

        if submission_result:
            flash("Richtig!")
        else:
            flash("Falsch!", "error")



    # display previous result
    else:
        if not has_previous_submission(user, team, problem_name):
            pass
        elif get_previous_result(user, team, problem_name):
            flash("Das Problem wurde bereits gelöst")
        else:
            pass




def _add_try(user, team, problem_name, submission_result):
    if team is not None:
        _add_try_individual(user, problem_name, submission_result)
        _add_try_team(team, problem_name, submission_result)


def _add_try_individual(user, problem_name, submission_result):
    user.increment_tries_counter(problem_name)
    user.set_submission_result(problem_name, submission_result)


def _add_try_team(team, problem_name, submission_result):
    team.increment_tries_counter(problem_name)
    team.set_submission_result(problem_name, submission_result)


def get_previous_result(user, team, problem_name):
    if team is None:
        return user.get_problem_status(problem_name)
    else:
        return team.get_problem_status(problem_name)

def has_previous_submission(user, team, problem_name):
    if team is not None:
        return team.get_tries_count(problem_name) != 0
    return user.get_tries_count(problem_name) != 0



# currently not used
def save_uploaded_file(submit_file):
    from flask import current_app as app
    from werkzeug.utils import secure_filename
    import os
    submit_filename = secure_filename(submit_file.filename)
    submit_filepath = os.path.join(app.config["UPLOAD_DIRECTORY"], submit_filename)
    submit_file.save(submit_filepath)





