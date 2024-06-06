from flask import request
from flask_login import current_user

from website.contest.compare_output_file import compare_output_file
from website.models import User




def handle_task_submission(control_filename, problem_name):
    user = User.query.filter_by(username=current_user.username).first()


    # handles upload of new try
    if request.method == "POST":
        submit_file = request.files["file"]
        if submit_file:

            correct = compare_output_file(submit_file, control_filename)

            user.add_try(problem_name)
            if correct:
                user.mark_solved(problem_name)
                return "richtig!"
            else:
                user.mark_unsolved(problem_name)
                return "falsch!"


    # displays no feedback if no tries have been made
    elif user.get_tries_count(problem_name) == 0:
        return ""



    # displays the result of the last try
    else:
        if user.get_problem_status(problem_name):
            return "richtig"
        else:
            return "falsch"

    return ""





# currently not used
def save_uploaded_file(submit_file):
    from flask import current_app as app
    from werkzeug.utils import secure_filename
    import os
    submit_filename = secure_filename(submit_file.filename)
    submit_filepath = os.path.join(app.config["UPLOAD_DIRECTORY"], submit_filename)
    submit_file.save(submit_filepath)





