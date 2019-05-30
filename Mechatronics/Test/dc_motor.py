import RPi.GPIO as GPIO
import time

pin = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

p = GPIO.PWM(pin, 50)
p.start(20)

try:
    a=7.2
    while True:
        a=a+0.01
        time.sleep(1)
        #a = input()
        angle = float(a)
        p.ChangeDutyCycle(angle)
        print("angle : "+str(a))

except KeyboardInterrupt:
    p.stop()

GPIO.cleanup()

