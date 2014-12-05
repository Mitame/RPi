#!/usr/bin/env python3
import RPi.GPIO as GPIO #@UnresolvedImport
import time

frameSpeed = 25
class pin():
    clock = 18
    reset = 23
    input = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin.clock, GPIO.OUT)
GPIO.setup(pin.reset, GPIO.OUT)
GPIO.setup(pin.input, GPIO.OUT)

f = open("./RowAni")
frames = f.read().split("\n")
def tick(on=pin.clock):
    GPIO.output(on,GPIO.HIGH)
    GPIO.output(on,GPIO.LOW)
def main():
    for frame in frames:
        for l in frame:
            if l == "1":
                GPIO.output(pin.input,GPIO.LOW)
            else:
                GPIO.output(pin.input,GPIO.HIGH)
            tick()
            time.sleep(1/(frameSpeed*len(frame)))
        tick(pin.reset)
if __name__ == "__main__": main()