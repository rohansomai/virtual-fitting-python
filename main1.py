#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response,request, redirect
from camera import VideoCamera
import cv2
import numpy as np
#from gui_final import Application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def transparentOverlay(src , overlay ,w, pos=(0,0),scale = 5):
    """
    :param src: Input Color Background Image
    :param overlay: transparent Image (BGRA)
    :param pos:  position where the image to be blit.
    :param scale : scale factor of transparent image.
    :return: Resultant Image
    """
    
    if w<60:
        overlay = cv2.resize(overlay,(50,50),fx=scale,fy=scale)
    if w>60 and w<100:
        overlay = cv2.resize(overlay,(350,350),fx=scale,fy=scale)
    elif w>100 and w<150:
        overlay = cv2.resize(overlay,(450,450),fx=scale,fy=scale)
    else:
        overlay = cv2.resize(overlay,(500,500),fx=scale,fy=scale)
    h,w,_ = overlay.shape  # Size of pngImg
    rows,cols,_ = src.shape  # Size of background Image
    y,x = pos[0],pos[1]    # Position of PngImage
    
    #loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x+i >= rows or y+j >= cols:
                continue
            alpha = float(overlay[i][j][3]/255.0) # read the alpha channel 
            
            src[x+i][y+j] = alpha*overlay[i][j][:3]+(1-alpha)*src[x+i][y+j]
            
    return src
def gen(camera=None,image = None):
    face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #image='t5.png'
    pngImage = cv2.imread(image , cv2.IMREAD_UNCHANGED)
    pngImage=cv2.resize(pngImage,(300,300))
    #myvar =  request.form.get("Button1")
    #print('>>>>>>>>>>>>>>>>>>>>>>>>',myvar)
    print("every time")
    while True:
        frame = camera.get_frame()
        nparr = np.fromstring(frame, np.uint8)
        frame = cv2.imdecode(nparr,cv2.IMREAD_UNCHANGED)
        print(frame.shape)
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1 , minNeighbors=3 , minSize=(30,30))
        for (x,y,w,h) in faces:
            cv2.rectangle(frame ,(x,y),(x+w,y+h),(255,0,0),2)
            if w<60:
                result = transparentOverlay(frame,pngImage,w,((x+w//2)-150,(y+h//2)+50),0.7)
            if w>60 and w<100:
                result = transparentOverlay(frame,pngImage,w,((x+w//2)-160,(y+h//2)+40),0.7)
            elif w>100 and w<150:
                result = transparentOverlay(frame,pngImage,w,((x+w//2)-210,(y+h//2)+50),0.7)
            else:
                result = transparentOverlay(frame,pngImage,w,((x+w//2)-230,(y+h//2)+60),0.7)
            result = cv2.imencode('.jpeg', result)[1].tostring()
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + result + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera(),image='t5.png'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

					
@app.route('/getButton', methods=['POST'])
def getButton():
    email = request.form['email']
    print("The email address is '" + email + "'")
	
    pngImage = "t6.png"
    #pngImage=cv2.resize(pngImage,(300,300))
    gen(pngImage)
    return redirect('/')
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)