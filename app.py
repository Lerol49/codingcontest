from flask import Flask, Blueprint, render_template, request, redirect
from subprocess import check_output
from werkzeug.utils import secure_filename
import os
import socket


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
        file = request.files["file"]
        if file:
            file.save(os.path.join(app.config["UPLOAD_DIRECTORY"], secure_filename(file.filename)))
    return render_template("upload.html")


@app.route("/test_contest")
def test_contest():
    return render_template("/test_contest/test_contest_index.html")



if __name__ == "__main__":
    app.run(host=ip, port=8000, debug=True)

