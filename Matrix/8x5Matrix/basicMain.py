#!/usr/bin/env python3
import RPi.GPIO as GPIO #@UnresolvedImport
import sys
import time
GPIO.setmode(GPIO.BCM)
fps = 30
overwrite = 5
columns = 8
class pin():
    row0 = 4
    row1 = 17
    row2 = 27
    row3 = 22
    row4 = 25
    columnClk = 18
    columnLight = 23
    columnReset = 24

for on in [pin.row0,pin.row1,
            pin.row2,pin.row3,
            pin.row4,pin.columnClk,
            pin.columnLight,pin.columnReset]:
    GPIO.setup(on,GPIO.OUT)
    
def pulse(on):
    GPIO.output(on,GPIO.HIGH)
    GPIO.output(on,GPIO.LOW)
    
def lowAll():
    for on in [pin.row0,pin.row1,
            pin.row2,pin.row3,
            pin.row4]:
        GPIO.output(on,GPIO.LOW)
    
def main():
    file = sys.argv[1]
    frames = open("./animations/%s"%file).read().split("\n\n")
    for frame in frames:
        for ow in range(overwrite):
            for column in frame.split("\n"):
                lowAll()
                pulse(pin.columnClk)
                for x in range(5):
                    if column[x] == "1":
                        GPIO.output((pin.row0,pin.row1,pin.row2,pin.row3,pin.row4)[x],GPIO.HIGH)
                time.sleep(1/(fps*overwrite*columns))
            pulse(pin.columnReset)
                    
                
    

if __name__ == "__main__":
    try:
        while 1:
            main()
    except KeyboardInterrupt:
        pass
    pulse(pin.columnReset)
    GPIO.cleanup()
