from functools import wraps
from flask import render_template, redirect, Blueprint, request, send_from_directory, current_app
from flask_login import login_required
from flask_login import current_user
from . import auth
from .models import get_teams
from .leaderboard import sort_teams_score
from . import contest_data
import markdown



from . import contest_data
from .contest.contest_handling import handle_task_submission

views = Blueprint("views", __name__)


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect("/login")

        if not current_user.rights == "admin":
            return "NICHT ADMIN"

        try:
            # current_app.ensure_sync available in Flask >= 2.0
            return current_app.ensure_sync(func)(*args, **kwargs)
        except AttributeError:  # pragma: no cover
            return func(*args, **kwargs)
    return wrapper 


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



# @views.route("/test_contest", methods=["POST", "GET"])
# @login_required
# def test_contest():
#     if request.method == "POST":
#         if "new_teamname" in request.form:
#             auth.create_team()
#         else:
#             auth.join_team()
#
#     return render_template("/test_contest/test_contest_index.html",
#                            user=current_user,
#                            team=current_user.get_team("test_contest"),
#                            problems=contest_data["contests"]["test_contest"]["problems"],
#                            teams=sort_teams_score("test_contest"))


@views.route("/contest/<contest_id>", methods=["POST", "GET"])
@login_required
def contest_index(contest_id):
    if request.method == "POST":
        if "new_teamname" in request.form:
            auth.create_team(contest_id)
        else:
            auth.join_team(contest_id)

    return render_template("/contest_index.html",
                           user=current_user,
                           team=current_user.get_team(contest_id),
                           problems=contest_data["contests"][contest_id]["problems"],
                           teams=sort_teams_score(contest_id),
                           contest_id=contest_id,
                           contest_name=contest_data["contests"][contest_id]["name"])




@views.route("contest/<contest_id>/<problem_id>", methods=["POST", "GET"])
@login_required
def load_contest_problem(contest_id, problem_id):
    if contest_data["contests"].get(contest_id) is None:
        return "no"
    print(problem_id)
    if contest_data["contests"][contest_id]["problems"].get(problem_id.replace(".md", "")) is None:
        return "nein"

    result = handle_task_submission(contest_id, problem_id, "solutions/" + problem_id + "/output.txt")

    with open("website/templates/" + contest_id + "/" + problem_id + ".md", "r") as problem_file:
        markdown_text = problem_file.read()

    # add nl2br for immediante line breaks
    markdown_html = markdown.markdown(markdown_text, extensions=["fenced_code", "tables", "md_in_html"])

    return render_template("/base_problem_md.html", problem_id=problem_id, problem_content=markdown_html,
                           result=result, user=current_user)


@views.route("/contest/input_files/<problem>")
def send_input_file(problem):
    return send_from_directory("../solutions/" + problem + "/", "input.txt")


@views.route("/admin")
@admin_required
def load_admin_main():
    return render_template("/admin_main.html", contests=contest_data["contests"], user=current_user)


@views.route("/admin/<contest>")
@admin_required
def load_admin_contest(contest):
    """loading admin config page for specific contest"""
    return render_template("/admin_contest_config.html", user=current_user)











