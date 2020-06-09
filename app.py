from flask import Flask
from flask import render_template, request, redirect, jsonify, send_from_directory, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

current_path = os.getcwd()

@app.route("/upload-video", methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        if request.files:
            video = request.files['myvideo']

            if 'static' not in os.listdir(current_path):
                os.mkdir('static')

            video.save(os.path.join('static', video.filename))
            print("Video saved")

            full_filename = os.path.join('static', video.filename)
            session['full_filename'] = full_filename
            return redirect(url_for('display_video'))
    return render_template("upload_video.html")


@app.route("/display-video")
def display_video():
    full_filename = session['full_filename']
    print(session['full_filename'])
    return render_template("display.html", full_filename=full_filename)
