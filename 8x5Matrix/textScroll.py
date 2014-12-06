#!/usr/bin/env python3
onRPi = True
try:
    import RPi.GPIO as GPIO 
except ImportError:
    onRPi = False
import sys
import time
if onRPi:
    GPIO.setmode(GPIO.BCM)
fps = 2
overwrite = 30
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
if onRPi:
    for on in [pin.row0,pin.row1,
                pin.row2,pin.row3,
                pin.row4,pin.columnClk,
                pin.columnLight,pin.columnReset]:
        GPIO.setup(on,GPIO.OUT)

class Frame():
    def __init__(self,size,defaultValue=0):
        self.size = size
        self.list = []
        for z in range(size[0]*size[1]):
            self.list.append(defaultValue)
    def set(self,pos,value):
        if self.withinLimits(pos):
            self[self.size[1]*pos[0]+pos[1]] = value
        else:
            raise IndexError
    
    def get(self,pos):
        if self.withinLimits(pos):
            return self[self.size[1]*pos[0]+pos[1]]
        else:
            raise IndexError
    
    def withinLimits(self,pos):
        return 0<=pos[0]<self.size[0] and 0<=pos[1]<self.size[1] 
    
    def scroll(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.withinLimits((x-1,y)):
                    self.set((x-1,y),self.get((x,y)))
    def flip(self,x=True,y=False):
        newlist = []
        for z in range(0,self.size[1]):
            newlist.append(self[self.size[0]:self.size[0]*z])
        
        retlist = []
        for list in newlist:
            list.reverse()
            retlist.extend(list)
        self = retlist
    
    def __list__(self):
        return self.list
    
def pulse(on):
    GPIO.output(on,GPIO.HIGH)
    GPIO.output(on,GPIO.LOW)
    
def lowAll():
    for on in [pin.row0,pin.row1,
            pin.row2,pin.row3,
            pin.row4]:
        GPIO.output(on,GPIO.LOW)
    
def renderFrames(frames):
    for frame in frames:
        renderFrame(frame)
        
def renderFrame(frame,reverse = True):
    if reverse:
        frame = frame.flip()
    for ow in range(overwrite):
        for column in frame.split("\n"):
            startTime = time.time()
            lowAll()
            pulse(pin.columnClk)
            for x in range(5):
                if column[x] == "1":
                    GPIO.output((pin.row0,pin.row1,pin.row2,pin.row3,pin.row4)[x],GPIO.HIGH)
            time.sleep(time.time()-startTime+(1/(fps*overwrite*columns)))
            
def renderFrameClass(frame):
    for ow in range(overwrite):
        pulse(pin.columnReset)
        for y in range(frame.size[1]):
            lowAll()
            pulse(pin.columnClk)
            for x in range(min(frame.size[0],5)):
                if frame.get((x,y)):
                    GPIO.output((pin.row0,pin.row1,pin.row2,pin.row3,pin.row4)[x],GPIO.HIGH)
                    
            time.sleep(1/(fps*overwrite*columns))

def renderFramesList(frames):
    for frm in frames:
        renderFrameClass(frm)
        
def scrollLeft(frame,filler="0"):
    newFrame = []
    for x in frame.split("\n"):
        newFrame.append(x[1:]+filler)
    return newFrame
    
             
def scrollText(text):
    frame = "00000\n00000\n00000\n00000\n00000\n00000\n00000\n00000"
    for char in text:
        curColumn = 0
        charFrame = charset[char]
        for x in range(len(charFrame.split("\n")[0])):
            frame[x]
    

def importDict(name="letters 5x5.txt"):
    newDict={}
    f = open(name).read()
    x = f.split("\n\n")
    for char in x:
        y = char.split(" ")
        newDict[y[0]] = y[1].strip("\n")
    return newDict

def importTextAni(name):
    newAni = []
    f = open("animations/"+name).read()
    x = f.split("\n\n")
    xs = x[0].split("\n")
    size = len(xs),len(xs[0])
    for frm in x:
        oneline = frm.replace("\n","")
        newFrame = Frame(size, 0)
        for bit in range(len(oneline)):
            newFrame[bit] = int(oneline[bit])
        newAni.append(newFrame)
    return newAni
            
            
        
if __name__ == "__main__":
    try:
        charset = importDict()
        x = importTextAni("revletters")
        while 1:
            renderFramesList(x)
    except KeyboardInterrupt:
        pass
    pulse(pin.columnReset)
    GPIO.cleanup()
