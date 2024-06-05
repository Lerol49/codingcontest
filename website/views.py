from flask import render_template, redirect, Blueprint, request, send_from_directory
from flask_login import login_required
from flask_login import current_user

from . import contest_data
from .contest.contest_handling import handle_task_submission

views = Blueprint("views", __name__)


@views.route("/")
def page_0():
    return redirect(request.url + "home")


@views.route("/home")
def home():
    return render_template("/home.html", user=current_user)

@login_required
@views.route("/profile")
def profile():
    return render_template("/profile.html", user=current_user)



@views.route("/test_contest")
@login_required
def test_contest():
    return render_template("/test_contest/test_contest_index.html", user=current_user, problems=contest_data["contests"]["test_contest"]["problems"])


@views.route("/<contest_name>/<problem>", methods=["POST", "GET"])
@login_required
def load_contest_problem(contest_name, problem):
    if contest_data["contests"].get(contest_name) is None:
        return "no"
    if contest_data["contests"][contest_name]["problems"].get(problem) is None:
        return "nein"

    result = handle_task_submission(contest_name, problem, "solutions/" + problem + "/output.txt")
    return render_template("/" + contest_name + "/" + problem + ".html", result=result)


@views.route("/test_contest/pizza_distribution_problem/input.txt")
def pizza_distribution_problem_download_input():
    return send_from_directory("../solutions/pizza_distribution_problem/", "input.txt")

@views.route("input_files/<problem>")
def send_input_file(problem):
    return send_from_directory("../solutions/" + problem + "/", "input.txt")


