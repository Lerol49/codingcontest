from flask import Flask, Blueprint, render_template, request, redirect
from subprocess import check_output
from werkzeug.utils import secure_filename
import os
import socket
from compare_output_file import compare_output_file


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


ip = get_ip_address()

app = Flask(__name__)

# app.register_blueprint(views, url_prefix="/")
app.config["UPLOAD_DIRECTORY"] = "uploads/"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB


@app.route("/")
def page_0():
    return redirect(request.url + "home")


@app.route("/home")
def home():
    return render_template("/home.html")


@app.route("/upload", methods=["POST", "GET"])
def upload_file():
    if request.method == "POST":
        submit_file = request.files["file"]
        if submit_file:
            submit_filename = secure_filename(submit_file.filename)
            submit_filepath = os.path.join(app.config["UPLOAD_DIRECTORY"], submit_filename)
            submit_file.save(submit_filepath)
            result = compare_output_file(submit_filepath, "templates/test_contest/cf_test_contest.txt")
            if result:
                return "yee"

    return render_template("upload.html")


@app.route("/test_contest")
def test_contest():
    return render_template("/test_contest/test_contest_index.html")



if __name__ == "__main__":
    app.run(host=ip, port=8000, debug=True)

