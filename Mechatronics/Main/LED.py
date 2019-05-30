import RPi.GPIO as GPIO
import time

class LED_Control():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(20, GPIO.OUT)
        self.green = GPIO.PWM(20,50)
        self.green.start(0)

        GPIO.setup(16, GPIO.OUT)
        self.yellow = GPIO.PWM(16,50)
        self.yellow.start(0)
        
        GPIO.setup(12, GPIO.OUT)
        self.red = GPIO.PWM(12,50)
        self.red.start(0)
        input_value = True
    
    def RED_ON(self):
        print("RED ON")
        self.red.ChangeDutyCycle(50)
    
    def RED_OFF(self):
        print("RED OFF")
        self.red.ChangeDutyCycle(0)
    
    def GREEN_ON(self):
        print("GREEN ON")
        self.green.ChangeDutyCycle(50)
   
    def GREEN_OFF(self):
        print("GREEN OFF")
        self.green.ChangeDutyCycle(0)

    def YELLOW_ON(self):
        print("YELLOW ON")
        self.yellow.ChangeDutyCycle(50)

    def YELLOW_OFF(self):
        print("YELLOW OFF")
        self.yellow.ChangeDutyCycle(0)
    
    def __del__(self):
        #self.red.stop()
        #self.green.stop()
        #self.yellow.stop()
        GPIO.cleanup()
