import RPi.GPIO as GPIO #@UnresolvedImport
import sys
import time
GPIO.setmode(GPIO.BCM)
fps = 25
overwrite = 5
columns = 8
class pin():
    row0 = 4
    row1 = 17
    row2 = 21
    row3 = 22
    row4 = 25
    columnClk = 18
    columnLight = 23
    columnReset = 24

for pin in [pin.row0,pin.row1,
            pin.row2,pin.row3,
            pin.row4,pin.columnClk,
            pin.columnLight,pin.columnReset]:
    GPIO.setup(pin,GPIO.OUT)
    
def pulse(pin):
    GPIO.output(pin,GPIO.HIGH)
    GPIO.output(pin,GPIO.LOW)
    
def lowAll():
    for pin in [pin.row0,pin.row1,
            pin.row2,pin.row3,
            pin.row4]:
        GPIO.output(pin,GPIO.LOW)
    
def main():
    file = sys.argv[1]
    frames = open("./animations/%s"%file).read().split("\n\n")
    for frame in frames:
        for ow in range(overwrite):
            for column in frame.split("\n"):
                pulse(pin.columnClk)
                for x in range(5):
                    if column[x] == 1:
                        GPIO.output((pin.row0,pin.row1,pin.row2,pin.row3,pin.row4),GPIO.high)
                    time.sleep(1/(fps*overwrite*columns))
                
    

if __name__ == "__main__":
    try:
        while 1:
            main()
    except KeyboardInterrupt:
        pass
    pulse(pin.columnReset)
    GPIO.cleanup()