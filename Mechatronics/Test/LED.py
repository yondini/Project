
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
input_value = True
try:
    while True:
            print("ON")
            GPIO.output(23, True)
            time.sleep(1)

            print("OFF")
            GPIO.output(23, False)
            time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
