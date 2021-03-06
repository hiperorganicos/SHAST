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

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import StringIO

manager = multiprocessing.Manager()
q = manager.Queue(3)

showVideo = True
max_area = 5000
min_area = 800

# Update shastcam.ignorelist.com DNS (public static IP)
def updateDNS():
    subprocess.call(["bash", "update_freedns.sh"])
    print ("DNS Updated.")

# ========================================================================
# Thread & Flask
# ========================================================================
def camrunner(q):

    queu = q

    class CamHandler(BaseHTTPRequestHandler):
        queue = None
        def do_GET(self):
            if self.path.endswith('.mjpg'):
                self.send_response(200)
                self.send_header('Content-type','multipart/x-mixed-replace; boundary=frame')
                self.end_headers()
                while True:
                    try:
                        if not self.queue.empty():
                            frame = None
                            frameaux = self.queue.get()
                            if frameaux is not None:
                                ret, jpeg = cv2.imencode('.jpeg', frameaux)
                                frame = jpeg.tostring()

                            self.wfile.write("--frame")
                            self.send_header('Content-type','image/jpeg')
                            self.wfile.write('\r\n' + frame)
                            self.end_headers()
                            time.sleep(0.01) #slow the stream a bit
                    except KeyboardInterrupt:
                        break
                return
            if self.path.endswith('.html'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write('<html><head></head><body>')
                self.wfile.write('<img src="/cam.mjpg"/>')
                self.wfile.write('</body></html>')
                return

    class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        """Handle requests in a separate thread."""

    def main(queuee):
        try:
            camhand = CamHandler
            camhand.queue = queuee
            server = ThreadedHTTPServer(('0.0.0.0', 8080), camhand)
            print "server started"
            server.serve_forever()
        except KeyboardInterrupt:
            capture.release()
            server.socket.close()

    if __name__ == '__main__':
        main(queu)
# ========================================================================
# OSC CLIENT AND FUNCTIONS
# ========================================================================
timeLastConnection = 0
client = OSCClient()

def connectOsc():
    global client, timeLastConnection
    if timeLastConnection < time.time() - 20:
        #updateDNS()
        client = OSCClient()
        client.connect( ("localhost", 22243) )
        timeLastConnection = time.time()

connectOsc()

def sendOscMessage(_x, _y, _w, _h):
    if x > 1 and y > 1:
        global client

        connectOsc()

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

# initialize the first frame in the video stream
firstFrame = None

# Start Flask
print("Starting stream server...")
p = multiprocessing.Process(target=camrunner, args=(q,))
p.daemon = True
p.start()
print("Started stream!")
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
    frame = imutils.resize(frame, width=480)

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
        if cv2.contourArea(c) > max_area or cv2.contourArea(c) < min_area:
            continue

        (x, y, w, h) = cv2.boundingRect(c)
        sendOscMessage(x, y, w, h)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # show the frame and record if the user presses a key
    # opens three video windows
    if showVideo:
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        # draw the text and timestamp on the frame
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow("Security Feed", frame)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

    # give the PC (and OSC server) some time to breathe
    time.sleep(0.05)

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
