import os
import shutil
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, jsonify
import json

from src import speech_emotion
from src.face_detection import face_detection_model
from src.speech_to_text import speech_to_text_model

# from .CV.eye_tracker import *

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv', 'wmv'}
app.config['TEMPLATES_AUTO_RELOAD'] = True


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
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        valid_username = "test"
        valid_password = "AIPentaHack"

        if username == valid_username:
            session['user'] = username
            # Create directory for user
            os.mkdir(os.path.join(UPLOAD_DIR, username))

            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", category="error")

    return render_template("signin.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    # if 'username' not in session:
    #     flash("Please log in to access this page.", category="error")
    #     return redirect(url_for("signin"))

    if "user" not in session:
        return redirect(url_for("signin"))

    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part.", category="error")
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash("No selected file.", category="error")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[1].lower()
            filename = f"video.{file_ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], session['user'], filename))
            session['video_file'] = filename
            flash("Video uploaded successfully!", category="success")
            
    # speech_data = {}

    # if "preds"
    # speech_data = {
    #     "preds_str": session["preds_str"],
    #     "interps": session["interps"],
    #     "curr_pred": session['curr_pred'],
    #     "curr_interps": session['curr_interps']
    # }


    # return render_template("dashboard.html")
    return redirect(url_for("dashboard"))


@app.route("/reset", methods=["GET", "POST"])
def reset():
    if "user" not in session:
        return redirect(url_for("signin"))

    if request.method == "POST":
        # If directory exist, then delete
        user_dir_img = os.path.join(UPLOAD_DIR, session['user'], 'img')
        if os.path.exists(user_dir_img):
            # os.rmdir(user_dir_img)
            shutil.rmtree(user_dir_img)
        
        if "video_file" in session:
            del session['video_file']
        if 'speech_data' in session:
            del session['speech_data']
            
    # speech_data = {}

    # if "preds"
    # speech_data = {
    #     "preds_str": session["preds_str"],
    #     "interps": session["interps"],
    #     "curr_pred": session['curr_pred'],
    #     "curr_interps": session['curr_interps']
    # }


    # return render_template("dashboard.html")
    return redirect(url_for("dashboard"))


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("signin"))

    # print(session)
    
    if 'speech_data' in session:
        return render_template("dashboard.html",
                               speech_data=json.dumps(session['speech_data']))
    else:
        return render_template("dashboard.html")
                           

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], session['user']),filename)

@app.route("/analyse", methods=["GET", "POST"])
def analyse():
    if 'user' not in session:
        flash("Please log in to access this page.", category="error")
        return redirect(url_for("signin"))


    file = ""
    if request.method == "GET":
        file = session['video_file']

        if file == '':
            flash("No selected file.", category="error")
            return redirect(request.url)
        # print(file)
        path = os.path.join(UPLOAD_DIR, session['user'], file)
        # preds, interps = speech_emotion.analyse_audio(file)
        
        # If directory exist, then delete
        user_dir_img = os.path.join(UPLOAD_DIR, session['user'], 'img')
        if os.path.exists(user_dir_img):
            # os.rmdir(user_dir_img)
            shutil.rmtree(user_dir_img)
        

        # Face Detection
        face_detection_model.save_cropped_faces(session['user'], path)
        # face_detection_model.video_with_box(session['user'], path)

        # new_video_path = os.path.join(UPLOAD_DIR, session['user'], "video", file)

        # shutil.move(os.path.join(new_video_path), os.path.join(UPLOAD_DIR, file))

        # Speech Emotion
        preds, interps = speech_emotion.analyse_audio_path(path)

        preds_str = list(map(lambda x: speech_emotion.id2label[x], preds))
        
        session['speech_data'] = {
            "preds_str": preds_str,
            "interps": interps,
            # "curr_pred": preds_str[0],
            # "curr_interps": session['curr_interps']
        }

        # session["preds_str"] = preds_str
        # session["interps"] = interps
        # session['curr_pred'] = preds_str[0]
        # session['curr_interps'] = interps[0]

        # Speech to Text
        text = speech_to_text_model.analyse(session['user'], path)
        session['text'] = text

    # speech_data = {
    #     "preds_str": session["preds_str"],
    #     "interps": session["interps"],
    #     "curr_pred": session['curr_pred'],
    #     "curr_interps": session['curr_interps']
    # }
    # return render_template("upload.html", 
    #                        speech_data = speech_data)
        
    return redirect(url_for("dashboard"))

@app.route('/slider_update', methods=['POST', 'GET'])
def slider():
    if request.method == "POST":
        received_data = request.get_json()
        idx = int(received_data['idx'])
        # print(idx, session["preds_str"])
        curr_pred = session["preds_str"][idx]
        curr_interps = session["interps"][idx]
        
        # print(curr_pred, curr_interps)
        body = {
            "pred": curr_pred,
            "data": curr_interps
        }
        return jsonify(body)
        # return body


# @app.route("/logout")
# def logout():
#     session.pop('username', None)
#     flash("Logged out successfully.", category="success")
#     return redirect(url_for("signin"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)

