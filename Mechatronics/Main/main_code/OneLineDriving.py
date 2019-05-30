import dc_motor
import servo_motor
import Encoder
import camera
import LED
from threading import Thread
from time import sleep
import cv2
import numpy as np
#cam=cv2.VideoCapture(0)
#sleep(2)

def encoder():
    speed = 0
    while True:
       value = _encoder.printEncoder()
       if int(value) < 20: 
           _dc.Control(7.45)
       else:
           _dc.Control(0)      
       sleep(1)
def camera_detection():
    angle = 6.4
    while True:
        img = _camera.readImage()
        #img = cv2.imread(r'images\chessboard\frame01.jpg')
        #img = cv2.resize(img,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
        img_original = img.copy()
        #blur2 = cv2.bilateralFilter(blur,9,100,100)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.bilateralFilter(gray,7,100,100)
        edges = cv2.Canny(blur,50,150,apertureSize=3)

        lines = cv2.HoughLines(edges,1,np.pi/180,70)
        resultline=[0]*3
        try:
            for i in range(len(lines)):
                if resultline[1]<lines[i][0][1]:
                    resultline[0]=lines[i][0][0]
                    resultline[1]=lines[i][0][1]
            rho=resultline[0]
            theta=resultline[1]
            print(theta)
            if (theta >= 0 and theta <1.2) or (theta >1.9 and theta <=3.14):
                _servo.Control(6.4)
                angle = 6.4
            elif theta > 1.57:
                if angle <= 7.5:
                    angle = angle + 0.2
                    _servo.Control(angle)
            else:
                if angle >= 5.5:
                    angle = angle - 0.2
                    _servo.Control(angle) 
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
        cv2.imshow('img',img)
    
if __name__ == '__main__':
    _dc = dc_motor.dc()
    _servo = servo_motor.servo()
    _encoder = Encoder.encoder()
    _encoder.startEncoder()
    _camera = camera.camera()
    
    _LED = LED.LED_Control()
    _LED.RED_ON()
    _LED.GREEN_ON()
    _LED.YELLOW_ON()
    t1=Thread(target=encoder)
    t2=Thread(target=camera_detection)
    t1.start()
    t2.start()

cv2.destroyAllWindows()
