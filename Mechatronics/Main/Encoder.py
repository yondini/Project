import RPi.GPIO as IO
import time
import threading
class encoder():
    def __init__(self):
        self.encPinA = 6
        self.encPinB = 13
        IO.setmode(IO.BCM)
        IO.setwarnings(False)
        IO.setup(self.encPinA, IO.IN, pull_up_down=IO.PUD_UP)
        IO.setup(self.encPinB, IO.IN, pull_up_down=IO.PUD_UP)

        self.encoderPos = 0
        _pinA = 0
        A_pos = 0
    def encoderA(self,channel):
        if IO.input(self.encPinA) == IO.input(self.encPinB):
            self.encoderPos += 1
        else:
            self.encoderPos -= 1
        #_pinA = channel
        #A_pos = encoderPos
    def startEncoder(self):        
        IO.add_event_detect(self.encPinA, IO.BOTH, callback=self.encoderA)    
            #print('PinA : %d, encoder : %d' %(_pinA, A_pos))
            #print('encoder : %d' %(self.encoderPos))
    def printEncoder(self):
        print('encoder : %d cm/s' %(self.encoderPos*0.028372))
        value = self.encoderPos
        self.encoderPos=0
        return value
