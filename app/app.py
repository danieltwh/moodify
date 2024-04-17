import os
import shutil
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_from_directory,
    jsonify,
    Response,
)
from flask_cors import CORS
import json
import datetime

# from src import speech_emotion
# from src.face_detection import face_detection_model
# from src.speech_to_text import speech_to_text_model

# from .CV.eye_tracker import *

from extensions import (
    open_rabbitmq_connection,
    init_postgres,
    sql_from_dict,
    sql_to_dict,
)

import models

import uuid

app = Flask(__name__)
CORS(app)
app.secret_key = "your_secret_key_here"
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"mp4", "avi", "mov", "mkv", "wmv"}
app.config["TEMPLATES_AUTO_RELOAD"] = True


UPLOAD_DIR = "uploads"

# Create the file system
if not os.path.isdir(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Cache-Control"] = "public, max-age=0"
    return response


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


# @app.route("/signin", methods=["GET", "POST"])
# def signin():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")

#         valid_username = "test"
#         valid_password = "AIPentaHack"

#         if username == valid_username:
#             session['user'] = username

#             user_dir = os.path.join(UPLOAD_DIR, username)
#             # Create directory for user
#             if not os.path.exists(user_dir):
#                 os.mkdir(user_dir)

#             return redirect(url_for("dashboard"))
#         else:
#             flash("Invalid username or password.", category="error")

#     return render_template("signin.html")


@app.route("/upload", methods=["POST"])
def upload():
    # if 'username' not in session:
    #     flash("Please log in to access this page.", category="error")
    #     return redirect(url_for("signin"))

    # if "user" not in session:
    #     return redirect(url_for("signin"))

    if request.method == "POST":
        if "file" not in request.files:
            resp = jsonify(status="failed", error_message="No file attached.")
            return resp

        file = request.files["file"]

        if file.filename == "":
            resp = jsonify(status="failed", error_message="No file attached.")
            return resp

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit(".", 1)[1].lower()
            filename = f"video.{file_ext}"

            video_id = str(uuid.uuid4())
            # print(video_id)

            dir_path = os.path.join(app.config["UPLOAD_FOLDER"], video_id)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)

            file.save(os.path.join(dir_path, filename))
            # session['video_file'] = filename
            # flash("Video uploaded successfully!", category="success")

            postgres = init_postgres()

            new_video = models.Videos(video_id, filename)

            video_details = (
                postgres.query(models.Videos)
                .filter(models.Videos.video_id == new_video.video_id)
                .first()
            )
            if video_details:
                return Response("Video id already taken.", status=409)

            postgres.add(new_video)
            postgres.commit()

            video_msg_dict = {
                "video_id": video_id,
            }
            video_msg = json.dumps(video_msg_dict)

            try:
                with open_rabbitmq_connection() as channel:
                    channel.basic_publish(
                        exchange="amq.direct",
                        routing_key="analyse-video",
                        body=video_msg,
                    )
            except Exception as err:
                print(err)

                body = {
                    "status": "failed",
                    "error_message": "Failed to send message to rabbitmq",
                }
                return jsonify(body)

            resp = jsonify(status="success")
            return resp
    
    
    # speech_data = {}

    # if "preds"
    # speech_data = {
    #     "preds_str": session["preds_str"],
    #     "interps": session["interps"],
    #     "curr_pred": session['curr_pred'],
    #     "curr_interps": session['curr_interps']
    # }

    # return render_template("dashboard.html")
    # return redirect(url_for("dashboard"))


@app.route("/video-metadata", methods=["GET"])
def video_metadata():
    # if 'username' not in session:
    #     flash("Please log in to access this page.", category="error")
    #     return redirect(url_for("signin"))

    # if "user" not in session:
    #     return redirect(url_for("signin"))
    postgress = init_postgres()

    all_videos = postgress.query(models.Videos).all()

    videos_dict = [video.__dict__ for video in all_videos]

    resp = []

    for d in videos_dict:
        intermediate = {}
        intermediate["id"] = d["video_id"]
        intermediate["title"] = d["video_name"]
        intermediate["uploadDate"] = d["date_created"].strftime("%Y-%m-%d")
        intermediate["status"] = d["video_status"]

        if d["predictions"] != "":
            predictions = json.loads(d["predictions"])
            intermediate["speechSentiment"] = predictions["aggregates"]["speech_data"]
            intermediate["expressionSentiment"] = predictions["aggregates"]["face_emotion"]
        else:
            intermediate["speechSentiment"] = "-"
            intermediate["expressionSentiment"] = "-"
        resp.append(intermediate)

    # resp = [
    #     {
    #         "expressionSentiment": "fearful",
    #         "speechSentiment": "fearful",
    #         "status": "completed",
    #         "title": "video.mp4",
    #         "uploadDate": "Mon, 13 Mar 2023 20:46:43 GMT",
    #     },
    # ]

    return jsonify(resp)


@app.route("/video/<id>/predictions", methods=["GET"])
def video_predictions(id):
    postgress = init_postgres()

    video = postgress.query(models.Videos).get(id).__dict__
    return jsonify(json.loads(video["predictions"]))


# @app.route("/reset", methods=["GET", "POST"])
# def reset():
#     if "user" not in session:
#         return redirect(url_for("signin"))

#     if request.method == "POST":
#         # If directory exist, then delete
#         user_dir_img = os.path.join(UPLOAD_DIR, session['user'], 'img')
#         if os.path.exists(user_dir_img):
#             # os.rmdir(user_dir_img)
#             shutil.rmtree(user_dir_img)

#         if "video_file" in session:
#             del session['video_file']
#         if 'speech_data' in session:
#             del session['speech_data']

#     # speech_data = {}

#     # if "preds"
#     # speech_data = {
#     #     "preds_str": session["preds_str"],
#     #     "interps": session["interps"],
#     #     "curr_pred": session['curr_pred'],
#     #     "curr_interps": session['curr_interps']
#     # }


#     # return render_template("dashboard.html")
#     return redirect(url_for("dashboard"))


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("signin"))

    # print(session)

    if "speech_data" in session:
        return render_template(
            "dashboard.html", speech_data=json.dumps(session["speech_data"])
        )
    else:
        return render_template("dashboard.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        os.path.join(app.config["UPLOAD_FOLDER"], session["user"]), filename
    )


@app.route("/stream/<video_id>")
def stream(video_id):
    postgres = init_postgres()
    video_details = (
        postgres.query(models.Videos).filter(models.Videos.video_id == video_id).first()
    )

    if not video_details:
        return Response("Video id not found.", status=404)

    return send_from_directory(
        os.path.join(app.config["UPLOAD_FOLDER"], video_details.video_id),
        video_details.video_name,
    )


@app.route("/slider_update", methods=["POST", "GET"])
def slider():
    if request.method == "POST":
        received_data = request.get_json()
        idx = int(received_data["idx"])
        # print(idx, session["preds_str"])
        curr_pred = session["preds_str"][idx]
        curr_interps = session["interps"][idx]

        # print(curr_pred, curr_interps)
        body = {"pred": curr_pred, "data": curr_interps}
        return jsonify(body)
        # return body


# @app.route("/logout")
# def logout():
#     session.pop('username', None)
#     flash("Logged out successfully.", category="success")
#     return redirect(url_for("signin"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
