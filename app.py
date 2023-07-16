from flask import Flask, render_template, Response, request, send_from_directory, redirect, url_for
from camera import VideoCamera
import os

pi_camera = VideoCamera(flip=True) # flip pi camera if upside down.
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Take a photo when pressing camera button
@app.route('/picture')
def take_picture():
    # take picture and redirect to index
    pi_camera.take_picture()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
