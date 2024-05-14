from flask import Blueprint, render_template, request, redirect
from werkzeug.utils import secure_filename
import os

views = Blueprint("views", __name__)


@views.route("/")
def page_0():
    return redirect(request.url + "home")


@views.route("/home")
def home():
    return render_template("/home.html")


