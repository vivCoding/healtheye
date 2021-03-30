from flask import Flask
from flask import render_template, Response
import socket
from PIL import Image
import cv2
import numpy
import struct
import io
import os
app = Flask(__name__)
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 8081
ADDR = (SERVER, PORT)
@app.route("/")
def home():
  return render_template('home.html')
def gen():
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect(ADDR)
    connection=client_socket.makefile('wb')
    try:
        img = None
        while True:
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            mage_stream.seek(0)
            mage = Image.open(image_stream)
            im = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGRm)
            yield(image.read())
    finally:
        connection.close()
        client_socket.close()

@app.route("/video_feed")
def video_feed():
   return Response(gen(),mimetype='multipart/x-mixed-replace')

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '8081'))
    except ValueError:
        PORT = 8081
    app.run(HOST, PORT)