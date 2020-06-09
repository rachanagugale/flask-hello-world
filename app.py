from flask import Flask
from flask import render_template, request, redirect, jsonify, send_from_directory, redirect, url_for, session
import os
import cv2

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

current_path = os.getcwd()

def getFrame(sec, vidcap, count, video_name):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite("static/" + str(video_name) + "_" + str(count)+".jpg", image)     # save frame as JPG file
    return hasFrames


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

            vidcap = cv2.VideoCapture(full_filename)

            sec = 0
            frameRate = 1 #it will capture image in each 0.5 second
            count = 1
            success = getFrame(sec, vidcap, count, video.filename)
            while success:
                count = count + 1
                sec = sec + frameRate
                sec = round(sec, 2)
                success = getFrame(sec, vidcap, count, video.filename)

            substring = video.filename + '_'
            sources = []
            for fname in os.listdir(os.getcwd() + '/static'):
                if fname.find(substring) != -1:
                    sources.append('static/' + fname)

            session['sources'] = sources

            return redirect(url_for('display_video'))
    return render_template('upload_video.html')


@app.route("/display-video")
def display_video():
    full_filename = session['full_filename']
    sources = session['sources']
    print(session['full_filename'])
    return render_template('display.html', full_filename=full_filename, sources=sources)
