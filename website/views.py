from flask import render_template, redirect, Blueprint, request, send_from_directory
from flask_login import login_required
from .auth import login_info
from .contest.contest_handling import handle_task_submission
from flask_login import current_user

views = Blueprint("views", __name__)


@views.route("/")
def page_0():
    print("hallo")
    return redirect(request.url + "home")


@views.route("/home")
def home():
    return render_template("/home.html", login_info=login_info())

@views.route("/profile")
def profile():
    return render_template("/profile.html", data=current_user.get_user_data())



@views.route("/test_contest")
@login_required
def test_contest():
    return render_template("/test_contest/test_contest_index.html", login_info=login_info())


@views.route("/test_contest/pizza_distribution_problem", methods=["POST", "GET"])
@login_required
def pizza_distribution_problem():
    result = handle_task_submission("solutions/pizza_distribution_problem/output.txt", "pizza_distribution_problem")
    return render_template("/test_contest/pizza_distribution_problem.html", result=result)


@views.route("/test_contest/pizza_distribution_problem/input.txt")
def pizza_distribution_problem_download_input():
    return send_from_directory("../solutions/pizza_distribution_problem/", "input.txt")
