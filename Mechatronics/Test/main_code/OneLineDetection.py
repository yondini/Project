import cv2
import numpy as np
import time
cam=cv2.VideoCapture(0)
#cam.set(3,50)
#cam.set(4,50)
time.sleep(2)
while True:
    fet,img = cam.read()
    #img = cv2.imread(r'images\chessboard\frame01.jpg')
    img = cv2.resize(img,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
    img_original = img.copy()
    #blur2 = cv2.bilateralFilter(blur,9,100,100)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray,7,100,100)
    edges = cv2.Canny(blur,50,150,apertureSize=3)

    lines = cv2.HoughLines(edges,1,np.pi/180,70)
    resultline=[0]*3
    for i in range(len(lines)):
        if resultline[1]<lines[i][0][1]:
            resultline[0]=lines[i][0][0]
            resultline[1]=lines[i][0][1]
            #if lines[i][1]>lines[i+1][1]:
            #    lines[0]=lines[i]
    try:
        rho=resultline[0]
        theta=resultline[1]
        print(theta)
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0+1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 -1000*(a))

        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    except:
        print("can't find line")
    res = np.vstack((img_original,img))
    if cv2.waitKey(1)&0xFF == ord('q'):
        break
    cv2.imshow('img',res)
    
cv2.destroyAllWindows()
