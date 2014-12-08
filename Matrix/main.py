#!/usr/bin/env python3

import sys
import time
import os
import RPi.GPIO as GPIO  #@UnresolvedImport

if os.path.curdir.split("/")[-1] == "Matrix":
    os.chdir("..")

from objects import Frame  #@UnresolvedImport 

GPIO.setmode(GPIO.BCM)



def loadConfig():
    global fps, overwrite,columns
    try:
        f = open("./Matrix/conf").read().split("\n")
        co = {}
        for x in f:
            y = x.split("=")
            co[y[0].lower()] = y[1]
        fps = int(co["fps"])
        overwrite = int(co["overwrite"])
        columns = int(co["columns"])
    except:
        fps = 2
        overwrite = 75
        columns = 8
        f = open("conf","w")
        f.write("fps="+str(fps)+
                "\noverwrite="+str(overwrite)+
                "\ncolumns="+str(columns))
        f.close()

class pin():
    row = [4,17,27,22,25]
    columnClk = 18
    columnLight = 23
    columnReset = 24
    all = []

pin.all.extend(pin.row)
pin.all.extend((pin.columnClk,pin.columnLight,pin.columnReset))

for on in pin.all:
    GPIO.setup(on,GPIO.OUT)
    
def pulse(on):
    GPIO.output(on,GPIO.HIGH)
    GPIO.output(on,GPIO.LOW)
    
def lowAll():
    for on in pin.row:
        GPIO.output(on,GPIO.LOW)        
            
def renderFrameClass(frame,reverse = True):
    if reverse:
        frame.flip()
    for ow in range(overwrite):
        pulse(pin.columnReset)
        for x in range(frame.size[0]):
            startTime = time.time()
            lowAll()
            pulse(pin.columnClk)
            for y in range(min(frame.size[1],5)):
                if frame.get((x,y)):
                    GPIO.output(pin.row[y],GPIO.HIGH)
                    
            time.sleep(time.time()-startTime+(1/(fps*overwrite*columns)))

def renderFramesList(frames,reverse = True):
    for frm in frames:
        renderFrameClass(frm,reverse)
        
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
    

def importDict(name="./Matrix/letters 5x5.txt"):
    newDict={}
    f = open(name).read()
    x = f.split("\n\n")
    for char in x:
        y = char.split(" ")
        newDict[y[0]] = strToFrame(y[1].strip("\n"))
    newDict[" "] = strToFrame("000")
    return newDict

def strToFrame(string):
    xs = string.split("\n")
    size = len(xs[0]),len(xs)
    oneline = string.replace("\n","")
    newFrame = Frame(size, 0)
    for bit in range(len(oneline)):
        newFrame[bit] = int(oneline[bit])
    return newFrame

def importTextAni(name):
    newAni = []
    f = open("Matrix/animations/"+name).read()
    x = f.split("\n\n")
    for frm in x:
        newAni.append(strToFrame(frm))
    return newAni

def genTextScrollAni(text,gapBetweenChars=1,startBlank=True):
    try:
        charset
    except NameError:
        global charset
        charset = importDict()
    textl = list(text)
    frames = []
    straightFrame = Frame((len(text)*(charset["A"].size[0]+gapBetweenChars),charset["A"].size[1]))
    for x in range(len(textl)):
        straightFrame.blit(charset[textl[x]], (x*(charset["A"].size[0]+gapBetweenChars),0))
    if startBlank:
        for x in range(columns):
            newFrame = Frame((8,5))
            newFrame.blit(straightFrame,(columns-x,0),((0,0),(x,5)))
            frames.append(newFrame)
    for x in range(straightFrame.size[0]):
        newFrame = Frame((8,5))
        newFrame.blit(straightFrame,(0,0),((x,0),newFrame.size))
        frames.append(newFrame)
    return frames
         
            
        
if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        loadConfig()
        if len(sys.argv) == 1:
            x = genTextScrollAni("Hello, World!")
        else:
            if sys.argv[1].lower() == "text":
                x = genTextScrollAni(" ".join(sys.argv[2:]))
            elif sys.argv[1].lower() == "ani":
                x = importTextAni(" ".join(sys.argv[2:]))
            else:
                print("Unrecoginsed command: %s"%sys.argv[1])
                print("Quitting...")
                raise SystemExit
        renderFramesList(x,True)
        while 1:
            renderFramesList(x,False)
    except KeyboardInterrupt:
        pass
    pulse(pin.columnReset)
    GPIO.cleanup()
