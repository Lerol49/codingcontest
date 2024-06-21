from flask import Blueprint, send_from_directory
from .models import Contest
import json
from .form import SetEndTime
import time
from flask import request, flash


other_requests = Blueprint("other_requests", __name__)



@other_requests.route("/contest/input_files/<problem>")
def send_input_file(problem):
    print("hallo")
    return send_from_directory("../solutions/" + problem + "/", "input.txt")


@other_requests.route("/contest/<contest_id>/get_end_time")
def get_end_time(contest_id):
    contest = Contest.query.filter_by(contest_id=contest_id).first()
    end_time = contest.get_end_time()

    return json.dumps(end_time)


def set_end_time(contest_id):
    form = SetEndTime()
    if request.method == "POST":
        try:
            submitted_time = int(form.end_time.data)
        except ValueError:
            return
        if form.validate_on_submit():
            contest = Contest.query.filter_by(contest_id=contest_id).first()
            contest.set_running(True)
            contest.set_end_time(time.time() + submitted_time * 3600)


