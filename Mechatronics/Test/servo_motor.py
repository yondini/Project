import RPi.GPIO as GPIO
import time

pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 50)
p.start(0)

try:
    a=5.1
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

