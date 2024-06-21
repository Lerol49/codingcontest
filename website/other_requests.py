from flask import Blueprint, send_from_directory
from .models import Contest
import json


other_requests = Blueprint("other_requests", __name__)



@other_requests.route("/contest/input_files/<problem>")
def send_input_file(problem):
    print("hallo")
    return send_from_directory("../solutions/" + problem + "/", "input.txt")


@other_requests.route("/contest/<contest_id>/get_end_time")
def idk(contest_id):
    contest = Contest.query.filter_by(contest_id=contest_id).first()
    end_time = contest.get_end_time()

    return json.dumps(end_time)


