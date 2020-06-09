from flask import Flask
from flask import render_template, request, redirect, jsonify, send_from_directory, redirect, url_for, session
import os
import cv2
from fastai import *
from fastai.vision import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

current_path = os.getcwd()

export_file_url = 'https://drive.google.com/file/d/1-0jqkVSvVtyhhBgszZIxAaF8bh2tevtV/view?usp=sharing'
export_file_name = 'export_onlysuspicious_resnet34.pkl'

def getFrame(sec, vidcap, count, video_name):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        write_path = "static/" + str(video_name) + "_" + str(count) + ".jpg"
        written_file_name = str(video_name) + "_" + str(count) + ".jpg"
        cv2.imwrite(write_path, image)     # save frame as JPG file
    return hasFrames, written_file_name


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
            
            vidcap = cv2.VideoCapture(full_filename)

            #defaults.device = torch.device('cpu')
            path = Path(current_path)
            download_file(export_file_url, path / export_file_name)
            learn = load_learner(path)
            results = {}

            sec = 0
            frameRate = 1 #it will capture image in each 0.5 second
            count = 1
            success, write_path = getFrame(sec, vidcap, count, video.filename)
            
            while success:
                count = count + 1
                sec = sec + frameRate
                sec = round(sec, 2)
                success, written_file_name = getFrame(sec, vidcap, count, video.filename)
                img = open_image(path/'static'/written_file_name)
                pred_class, pred_idx, outputs = learn.predict(img)
                results[count] = pred_class


            substring = video.filename + '_'
            sources = []
            for fname in os.listdir(os.getcwd() + '/static'):
                if fname.find(substring) != -1:
                    sources.append('static/' + fname)

            session['sources'] = sources
            session['results'] = results
            session['full_filename'] = full_filename

            return redirect(url_for('display_video'))
    return render_template('upload_video.html')


@app.route("/display-video")
def display_video():
    full_filename = session['full_filename']
    sources = session['sources']
    results = session['results']
    print(session['full_filename'])
    return render_template('display.html', full_filename=full_filename, sources=sources, results=results)
