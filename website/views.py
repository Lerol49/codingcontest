from flask import render_template, redirect, Blueprint, request, send_from_directory
from flask_login import login_user, login_required, current_user
from werkzeug.security import check_password_hash

from . import contest_data
from .auth import login_info
from .contest.contest_handling import handle_task_submission
from .form import LoginForm
from .models import User

views = Blueprint("views", __name__)


@views.route("/")
def page_0():
    print("hallo")
    return redirect(request.url + "home")


@views.route("/home")
def home():
    return render_template("/home.html", user=current_user)





@views.route("/upload", methods=["POST", "GET"])
def test_upload_file():
    return render_template("upload.html")


@views.route("/test_contest")
@login_required
def test_contest():
    return render_template("/test_contest/test_contest_index.html", user=current_user)


@views.route("/<contest>/<problem>", methods=["POST", "GET"])
@login_required
def load_contest_problem(contest, problem):
    if contest_data["contests"].get(contest) is None:
        return "no"
    if contest_data["contests"][contest]["problems"].get(problem) is None:
        return "nein"

    result = handle_task_submission("solutions/" + problem + "/output.txt", problem)
    return render_template("/" + contest + "/" + problem  + ".html", result=result)


@views.route("/test_contest/pizza_distribution_problem/input.txt")
def pizza_distribution_problem_download_input():
    return send_from_directory("../solutions/pizza_distribution_problem/", "input.txt")
