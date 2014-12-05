#!/usr/bin/env python3
import RPi.GPIO as GPIO #@UnresolvedImport
import time

frameSpeed = 25
goOverCount = 5
class pin():
    clock = 18
    reset = 23
    input = 24
    out = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin.clock, GPIO.OUT)
GPIO.setup(pin.reset, GPIO.OUT)
GPIO.setup(pin.input, GPIO.OUT)
GPIO.setup(pin.out, GPIO.OUT)

f = open("./RowAni")
frames = f.read().split("\n")
def tick(on=pin.clock):
    GPIO.output(on,GPIO.HIGH)
    GPIO.output(on,GPIO.LOW)
def main():
    for frame in frames:
        for x in range(goOverCount):
            for l in frame:
                if l == "1":
                    GPIO.output(pin.out,GPIO.LOW)
                else:
                    GPIO.output(pin.out,GPIO.HIGH)
                tick()
                time.sleep(1/(frameSpeed*len(frame)*goOverCount))
            tick(pin.reset)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()
        