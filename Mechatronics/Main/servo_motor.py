import RPi.GPIO as GPIO
import time

class servo():
    def __init__(self):
        pin = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.p = GPIO.PWM(pin, 50)
        self.p.start(0)
    def Control(self,value):
        try:
            self.p.ChangeDutyCycle(float(value))
            print("angle : "+str(value))
        except KeyboardInterrupt:
            self.p.stop()
    def __del__(self):
        self.p.stop()
        GPIO.cleanup()
