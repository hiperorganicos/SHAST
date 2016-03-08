# Adapted by: George Rappel <george.concei[at]hotmail.com>
# From: http://pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
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

# ========================================================================
# OSC CLIENT AND FUNCTIONS
# ========================================================================

oscCalls = 0
oscCallsLimit = 200

# OSC Client
client = OSCClient()
client.connect( ("146.164.80.56", 22244) )

def sendOscMessage(_x, _y, _w, _h):
    global oscCalls, oscCallsLimit, client
    oscCalls = oscCalls + 1

    if oscCalls > oscCallsLimit:
        client = OSCClient()
        client.connect( ("146.164.80.56", 22244) )
        oscCalls = 0
    msg = OSCMessage("/shast/coordenadas")
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

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    (grabbed, frame) = camera.read()

    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if not grabbed:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
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

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        sendOscMessage(x, y, w, h)

    # draw the text and timestamp on the frame
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    # show the frame and record if the user presses a key
    # opens three video windows
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
