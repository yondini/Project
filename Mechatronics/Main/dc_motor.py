import RPi.GPIO as GPIO
import time

class dc():
    def __init__(self):
        
        pin = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.p = GPIO.PWM(pin, 500)
        self.p.start(0)
    def Control(self,value):
        try:
            self.p.ChangeDutyCycle(value)
            print("angle : "+str(value))
        except KeyboardInterrupt:
            print("dc Error")
            self.p.stop()
    def __del__(self):
        self.p.stop()
        GPIO.cleanup()

