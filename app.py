from flask import Flask
from flask import render_template, request, redirect, jsonify
import os

app = Flask(__name__)

app.config['VIDEO_UPLOADS'] = "C:\\Users\\Rachana\\Desktop\\ProjectFrontend\\FlaskApp\\uploads"

@app.route("/upload-video", methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        if request.files:
            video = request.files['myvideo']

            #video.save(os.path.join(app.config['VIDEO_UPLOADS']), video.filename)
            #video.save("C:\\Users\\Rachana\\Desktop\\ProjectFrontend\\FlaskApp\\uploads\\" + video.filename)
            print("Video saved")
            path = os.getcwd()
            print(path)
            print(os.listdir(path))

            return redirect(request.url)
    return render_template("upload_video.html")

@app.route("/")
def hello():
    return render_template("upload_video.html")
