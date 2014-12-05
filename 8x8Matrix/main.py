import RPi.GPIO as GPIO
import time

class pin():
    clock = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin.clock, GPIO.OUT)
while 1:
    GPIO.output(pin.clock, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(pin.clock, GPIO.LOW)
    time.sleep(0.75)