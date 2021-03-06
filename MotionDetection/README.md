# Motion Detection
Cuida da detecção de movimento dentro da colméia. Composto por uma Raspberry Pi e uma WebCam, realiza o envio via OSC das coordenadas das abelhas para o servidor do NANO.

`python socket-motion.py`

<strong>Caminho OSC:</strong>

/shast/coordenadas (4 argumentos: X, Y, Altura, Largura)

##Files
### socket-motion.py
Uses Python's BaseHTTPServer and SocketServer to host the server provider for the MJPEG Streaming, and OpenCV 2 for motion detection.

### old-motion.py
Previous version of our motion tracker, used Flask as the MJPEG streaming server, not recommended for production, and OpenCV2 for motion detection. Requires 'templates' folder.
<hr>

##Setup
* Install Python

`sudo apt-get install build-essential checkinstall`<br>
`sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev`<br>
`sudo apt-get install tk-dev libgdbm-dev libc6-dev libbz2-dev`<br>
`sudo apt-get install python2.7-dev`<br>


* Install libraries:
Depencies for Opencv and the streaming<br>
`sudo apt-get install build-essential cmake git pkg-config`<br>
`sudo apt-get install libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev`<br>
`sudo apt-get install libgtk2.0-dev`<br>
`sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev`<br>

Install pip<br>
`wget https://bootstrap.pypa.io/get-pip.py`<br>
`sudo python get-pip.py`<br>

pip install imutils
pip install flask
pip install pyosc
pip install numpy
pip install picamera (optional, use ==1.10 if the image is black)

sudo apt-get install python-opencv

4. Set autorun on boot
crontab -e

Add the command to be run with the path to the .py file.

Ex:
"@reboot python /home/pi/shast/MotionDetection/picam_socket_motion.py"
