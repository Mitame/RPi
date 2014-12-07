#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)

p = GPIO.PWM(13,100)
p.start(0)
try:
    while 1:
        for x in range(0,100,1):
            p.ChangeDutyCycle(x)
            time.sleep(0.01)
        for x in range(100,-1,-1):
            p.ChangeDutyCycle(x)
            time.sleep(0.01)
        time.sleep(1)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
    pass


