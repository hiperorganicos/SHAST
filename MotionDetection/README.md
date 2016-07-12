# Motion Detection
Cuida da detecção de movimento dentro da colméia. Composto por uma Raspberry Pi e uma WebCam, realiza o envio via OSC das coordenadas das abelhas para o servidor do NANO.

''python socket-motion.py''

<strong>Caminho OSC:</strong>

/shast/coordenadas (4 argumentos: X, Y, Altura, Largura)


### socket-motion.py
Uses Python's BaseHTTPServer and SocketServer to host the server provider for the MJPEG Streaming, and OpenCV 2 for motion detection.

### old-motion.py
Previous version of our motion tracker, used Flask as the MJPEG streaming server, not recommended for production, and OpenCV2 for motion detection.
<hr>

1. Install Python
- Dependencies
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

- Then, Python:
sudo apt-get install python2.7-dev

OR (try)

sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python2.7

2. Install libraries:
- Depencies for Opencv and the streaming
sudo apt-get install build-essential cmake git pkg-config
sudo apt-get install libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev
sudo apt-get install libgtk2.0-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev

- Install pip
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

pip install imutils
pip install flask
pip install osc
pip install cv2
pip install numpy

- Install opencv2
wget -O opencv-2.4.10.zip http://sourceforge.net/projects/opencvlibrary/files/opencv-unix/2.4.10/opencv-2.4.10.zip/download
unzip opencv-2.4.10.zip
cd opencv-2.4.10

mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_NEW_PYTHON_SUPPORT=ON -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON  -D BUILD_EXAMPLES=ON ..
make
make install

3. scp motion.py
4.
4. Set autorun
5.
