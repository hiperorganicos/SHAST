# Adapted by: George Rappel <george.concei[at]hotmail.com>
# From: http://pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
#
#  Functionality: IP updated automatically by Free DNS service.
#  Adress: {freedns domain. ex: shast.ignorelist.com}:7777/video_feed
# =========================================================

# import the necessary packages
import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages')

import argparse
import datetime
from OSC import OSCClient, OSCMessage
import cv2
import imutils
import time
import Queue
import threading
from flask import Flask, render_template, Response
import multiprocessing
import subprocess

manager = multiprocessing.Manager()
q = manager.Queue(3)

showVideo = False

# Update shastcam.ignorelist.com DNS (public static IP)
def updateDNS():
    subprocess.call(["bash", "update_freedns.sh"])

# ========================================================================
# Thread & Flask
# ========================================================================

def FlaskRunner(q):

    queue = q
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    def gen():
        while True:
            if not queue.empty():
                frameaux = queue.get()
                if frameaux is not None:
                    ret, jpeg = cv2.imencode('.jpeg', frameaux)
                    frame = jpeg.tostring()

                if frame is not None:
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            #Slow down the streaming
            time.sleep(0.15)

    @app.route('/video_feed')
    def video_feed():
        return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

    app.run(host='0.0.0.0', port=7777, debug=False)

# ========================================================================
# OSC CLIENT AND FUNCTIONS
# ========================================================================
timeLastConnection = 0
client = OSCClient()

def connectOsc():
    global client, timeLastConnection
    if timeLastConnection < time.time() - 7200:
        print("connecting to OSC server")
        updateDNS()
        client = OSCClient()
        client.connect( ("146.164.80.56", 22244) )
        timeLastConnection = time.time()

connectOsc()

def sendOscMessage(_x, _y, _w, _h):
    if x > 1 and y > 1:
        global client

        connectOsc()

        msg = OSCMessage("/shast/coordinates")
        msg.extend([_x, _y, _w, _h])
        client.send( msg )

# =======================================================================
# Motion detection
# =======================================================================

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type=int, default=300, help="minimum area size")
args = vars(ap.parse_args())

# Reading from webcam
camera = cv2.VideoCapture(0)
time.sleep(0.25)

# initialize the first frame in the video stream
firstFrame = None

# Start Flask
print("Starting flask...")
p = multiprocessing.Process(target=FlaskRunner, args=(q,))
p.start()
print("Started flask!")
# loop over the frames of the video
print("Starting image reading...")
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    grabbed, frame = camera.read()
    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if not grabbed:
        break

    # resize the frame
    frame = imutils.resize(frame, width=500)

    # Coloca o frame redimensionado na Queue
    if not q.full() and frame is not None:
        q.put_nowait(frame)

    # Convert the frame to grayscale, and blur it
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 60, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue


        (x, y, w, h) = cv2.boundingRect(c)
        sendOscMessage(x, y, w, h)

    # show the frame and record if the user presses a key
    # opens three video windows
    if showVideo:
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # draw the text and timestamp on the frame
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow("Security Feed", frame)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

    # give the PC some time to breathe
    time.sleep(0.1)

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
