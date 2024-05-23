import os
from flask import request, current_app as app
from flask_login import current_user
from sqlalchemy.orm import attributes
from werkzeug.utils import secure_filename

from website.contest.compare_output_file import compare_output_file
from website.models import Problems
from website import db


def handle_task_submission(control_filename, problem_name):
    # checks if user has already submitted something
    user = Problems.query.filter_by(username=current_user.username).first()
    if user is None:
        new_try = Problems(username=current_user.username)
        db.session.add(new_try)
        db.session.commit()
        return ""

    elif request.method == "POST":
        submit_file = request.files["file"]
        if submit_file:
            # submit_filename = secure_filename(submit_file.filename)
            # submit_filepath = os.path.join(app.config["UPLOAD_DIRECTORY"], submit_filename)
            # submit_file.save(submit_filepath)
            correct = compare_output_file(submit_file, control_filename)
            user = Problems.query.filter_by(username=current_user.username).first()
            current_data = getattr(user, problem_name)
            if correct:
                current_data["passed"] = 1
                current_data["tries"] += 1
                setattr(user, problem_name, current_data)
                attributes.flag_modified(user, problem_name)
                db.session.commit()
                return "richtig!"
            else:
                current_data = getattr(user, problem_name)
                current_data["passed"] = 0
                current_data["tries"] += 1
                setattr(user, problem_name, current_data)
                attributes.flag_modified(user, problem_name)
                db.session.commit()
                return "falsch!"

    elif getattr(user, problem_name).get("tries") == 0:
        return ""

    else:
        problem = Problems.query.filter_by(username=current_user.username).first()
        if getattr(problem, problem_name).get("passed"):
            return "richtig"
        else:
            return "falsch"

    return ""
