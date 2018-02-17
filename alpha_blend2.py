import cv2
import numpy as np

# function to overlay a transparent image on backround.
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

""" ----------- Read all images --------------------"""
bImg = cv2.VideoCapture(0)
#print(bImg.shape)
pngImage = cv2.imread("t5.png" , cv2.IMREAD_UNCHANGED)
#print (pngImage.shape)

pngImage=cv2.resize(pngImage,(300,300))
face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
while(True):
    ret, frame=bImg.read()
    print(frame.shape)
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1 , minNeighbors=3 , minSize=(30,30))
    k=cv2.waitKey(1)
    if k==ord('a'):
        pngImage = cv2.imread("t5.png" , cv2.IMREAD_UNCHANGED)
        pngImage=cv2.resize(pngImage,(300,300))
        print("yes")
    if k==ord('b'):
        pngImage = cv2.imread("t4.png" , cv2.IMREAD_UNCHANGED)
        pngImage=cv2.resize(pngImage,(300,300))
        print("No")
    if k==ord('c'):
        pngImage = cv2.imread("t6.png" , cv2.IMREAD_UNCHANGED)
        pngImage=cv2.resize(pngImage,(300,300))
        print("yes")
    if k==ord('d'):
        pngImage = cv2.imread("t7.png" , cv2.IMREAD_UNCHANGED)
        pngImage=cv2.resize(pngImage,(300,300))
        print("No")
    if k==ord('e'):
        pngImage = cv2.imread("t8.png" , cv2.IMREAD_UNCHANGED)
        pngImage=cv2.resize(pngImage,(300,300))
        print("No")
    
    for (x,y,w,h) in faces:
        cv2.rectangle(frame ,(x,y),(x+w,y+h),(255,0,0),2)
        #cv2.putText(frame,'c',(x+w//2,y+h//2),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        #cv2.imshow('png',pngImage)
        if w<60:
            result = transparentOverlay(frame,pngImage,w,((x+w//2)-150,(y+h//2)+50),0.7)
        if w>60 and w<100:
            result = transparentOverlay(frame,pngImage,w,((x+w//2)-160,(y+h//2)+40),0.7)
        elif w>100 and w<150:
            result = transparentOverlay(frame,pngImage,w,((x+w//2)-210,(y+h//2)+50),0.7)
        else:
            result = transparentOverlay(frame,pngImage,w,((x+w//2)-230,(y+h//2)+60),0.7)
        #cv2.putText(frame, "p", (x,y+h),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        #cv2.putText(frame, "q", (x+w,y+h),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
    #cv2.namedWindow("Result",cv2.WINDOW_NORMAL)
    cv2.imshow("Result" ,result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
bImg.release()
cv2.destroyAllWindows()
