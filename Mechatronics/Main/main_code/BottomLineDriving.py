import dc_motor
import servo_motor
import Encoder
import camera
import LED
from threading import Thread
from time import sleep
import cv2
import numpy as np
from fractions import Fraction

def encoder():
    speed = 0

    while True:
        
        a = input()
        _servo.Control(float(a))
        """
        _dc.Control(74)
        value = _encoder.printEncoder()
        print("Speed : ",value)
        sleep(1)
        """
        
       
def camera_detection():
    while True:
        frame = _camera.readImage()
        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.bilateralFilter(gray,7,100,100)
        edges = cv2.Canny(blur,120,200,apertureSize=3)    
        lines = cv2.HoughLinesP(edges, 1, 1 * np.pi/180, 50, np.array([]), minLineLength=10, maxLineGap=20)
        
        try:
            if len(lines)==1:
                slope_degree = (np.arctan2(lines[0][0][1] - line_arr[0][0][3], line_arr[0][0][0] - line_arr[0][0][2]) * 180) / np.pi
            else:
                line_arr = np.squeeze(lines)
                slope_degree = (np.arctan2(line_arr[:,1] - line_arr[:,3], line_arr[:,0] - line_arr[:,2]) * 180) / np.pi

            Left, Right = [], []
            com_Y = []

            for i in range(len(slope_degree)):
                if slope_degree[i]>0:
                    Left.append(lines[i])
                if slope_degree[i]<0:
                    Right.append(lines[i])

            if len(Left)!=0 or len(Right)!=0:
                if len(Left)!=0:
                    if len(Left)>1:
                        Left_arr = np.squeeze(Left)    
                        Left_point = [int(np.mean(Left_arr[:,0])), int(np.mean(Left_arr[:,1])), int(np.mean(Left_arr[:,2])), int(np.mean(Left_arr[:,3]))]
                    else: 
                        Left_point = [Left[0][0][0], Left[0][0][1], Left[0][0][2], Left[0][0][3]]
                    com_Y.append(Left_point[1])
                    com_Y.append(Left_point[3])
                    slope_L = (np.arctan2(Left_point[1] - Left_point[3], Left_point[0] - Left_point[2]) * 180) / np.pi

                if len(Right)!=0:
                    if len(Right)>1:
                        Right_arr = np.squeeze(Right)
                        Right_point = [int(np.mean(Right_arr[:,0])), int(np.mean(Right_arr[:,1])), int(np.mean(Right_arr[:,2])), int(np.mean(Right_arr[:,3]))]
                    else:
                        Right_point = [Right[0][0][0], Right[0][0][1], Right[0][0][2], Right[0][0][3]]
                    com_Y.append(Right_point[1])
                    com_Y.append(Right_point[3])
                    slope_R = (np.arctan2(Right_point[1] - Right_point[3], Right_point[0] - Right_point[2]) * 180) / np.pi
            print("___________start____________")
            

            if Left_point[1]==max(com_Y) or Left_point[3]==max(com_Y):
                print("Left_slope:", slope_L)
                #L_val= Fraction(1, 15)*(slope_L-135)+6.5
                #_servo.Control(L_val)
                
                """
                if slope_L>120 and slope_L<140:
                    #_servo.Control(6.4)
                    print("L_Straight")
                elif slope_L>140:
                    #_servo.Control(7.4)
                    print("L_Left")
                elif slope_L<120:
                    #_servo.Control(5.2)
                    print("L_Right")
                """
                cv2.line(frame, (Left_point[0], Left_point[1]), (Left_point[2], Left_point[3]), (0,0,255),3)
            elif Right_point[1]==max(com_Y) or Right_point[3]==max(com_Y):
                print("Right_slope:", slope_R)
               # R_val= Fraction(1, 15)*(slope_R+135)+6.5
                #_servo.Control(R_val)
                
                """
                if slope_R>-140 and slope_R<-120:
                    #_servo.Control(6.4)
                    print("R_Straight")
                elif slope_L>-120:
                    #_servo.Control(7.4)
                    print("R_Left")
                elif slope_R<-140:
                    #_servo.Control(5.2)
                    print("R_Right")
                """
                cv2.line(frame, (Right_point[0], Right_point[1]), (Right_point[2], Right_point[3]), (255,0,0),3)
            print("___________end____________")
                
            
        except:
            print("can't fine lines")
            
        cv2.imshow('result',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

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
    #t3=Thread(target=servo)
    t1.start()
    t2.start()
    #t3.start()
