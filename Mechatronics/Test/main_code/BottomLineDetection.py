import numpy as np
import cv2
import random
import os, sys

cap=cv2.VideoCapture('line_640x480.mp4')
fit_result, l_fit_result, r_fit_result, L_lane,R_lane = [], [], [], [], []

while True:
    ret, frame = cap.read()
    height, width = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray,(3, 3), 0)
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
            #print("Left(y1, y2):", Left_point[1], Left_point[3])
            #print("Left_slope:", slope_L)
            #cv2.line(frame, (Left_point[0], Left_point[1]), (Left_point[2], Left_point[3]), (0,0,255),3)

            if len(Right)!=0:
                if len(Right)>1:
                    Right_arr = np.squeeze(Right)
                    Right_point = [int(np.mean(Right_arr[:,0])), int(np.mean(Right_arr[:,1])), int(np.mean(Right_arr[:,2])), int(np.mean(Right_arr[:,3]))]
                else:
                    Right_point = [Right[0][0][0], Right[0][0][1], Right[0][0][2], Right[0][0][3]]
                com_Y.append(Right_point[1])
                com_Y.append(Right_point[3])
                slope_R = (np.arctan2(Right_point[1] - Right_point[3], Right_point[0] - Right_point[2]) * 180) / np.pi
                #print("Right(y1, y2):", Right_point[1], Right_point[3])
                #print("Right_slope:", slope_R)
                #cv2.line(frame, (Right_point[0], Right_point[1]), (Right_point[2], Right_point[3]), (255,0,0),3)

        print("__________start___________")
        
        if Left_point[1]==max(com_Y) or Left_point[3]==max(com_Y):
            print("Left_slope:", slope_L)
            if slope_L>120 and slope_L<140:
                servo = 6.4
                print("L_Straight")
            elif slope_L>140:
                servo = 5.2
                print("L_Right")
            elif slope_L<120:
                servo = 7.4
                print("L_Left")
            cv2.line(frame, (Left_point[0], Left_point[1]), (Left_point[2], Left_point[3]), (0,0,255),3)
        elif Right_point[1]==max(com_Y) or Right_point[3]==max(com_Y):
            print("Right_slope:", slope_R)
            if slope_R>-140 and slope_R<-120:
                servo = 6.4
                print("R_Straight")
            elif slope_L>-120:
                servo = 5.2
                print("R_Right")
            elif slope_R<-140:
                servo = 7.4
                print("R_Left")
            cv2.line(frame, (Right_point[0], Right_point[1]), (Right_point[2], Right_point[3]), (255,0,0),3)
        print("servo value:", servo)
        print("___________end____________")
        

    except:
        print("can't fine lines")
            
    cv2.imshow('result',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


"""
    for i in range(len(slope_degree)):
        if slope_degree[i]>0:
            Left_arr = np.squeeze(Left)
            cv2.line(frame,(int(np.mean(Left_arr[:,0])), int(np.mean(Left_arr[:,1]))),(int(np.mean(Left_arr[:,2])), int(np.mean(Left_arr[:,3]))),(0,0,255),3)
        if slope_degree[i]<0:
            Right_arr = np.squeeze(Right)
            cv2.line(frame,(int(np.mean(Right_arr[:,0])), int(np.mean(Right_arr[:,1]))),(int(np.mean(Right_arr[:,2])), int(np.mean(Right_arr[:,3]))),(255,0,0),3)
"""
