#!/usr/bin/env python3

import sys
import time
import os
import pygame.time

try:
    import RPi.GPIO as GPIO  #@UnresolvedImport
    rootDir = os.path.abspath("/home/pi/RPi")
except RuntimeError:
    rootDir = os.path.abspath("/home/leviwright/Documents/workspace/RPi")

os.chdir(rootDir)
    
try:
    from Matrix.objects import Frame  #@UnresolvedImport
except ImportError:
    from objects import Frame  #@UnresolvedImport

class pin():
    #row = [2,3,4,17,27,22,10,9]
    row = [4,17,27,22,25,10,8,7]
    col0Clk = 14
    col0Reset = 15
    col1Clk = 18
    col1Reset = 23
    all = []
pin.all.extend(pin.row)
pin.all.extend((pin.columnClk,pin.columnLight,pin.columnReset))

def loadPi():
    GPIO.setmode(GPIO.BCM)
    for on in pin.all:
        GPIO.setup(on,GPIO.OUT)


def loadConfig():
    global fps, overwrite,matrixSize
    try:
        f = open("./Matrix/conf").read().strip().split("\n")
        co = {}
        for x in f:
            y = x.split("=")
            co[y[0].lower()] = y[1]
        print(co)
        fps = int(co["fps"])
        overwrite = int(co["overwrite"])
        matrixSize= tuple(int(x.strip()) for x in co["matrixsize"].strip("()").split(","))
        ledSize= tuple(int(x.strip()) for x in co["ledsize"].strip("()").split(","))
    except IndexError:
        print((x,y))
    except FileNotFoundError:
        fps = 2
        overwrite = 75
        matrixSize = (8,8)
        ledSize = (25,25)
        print(os.path.abspath("./Matrix/conf"))
        f = open("./Matrix/conf","w")
        f.write("fps="+str(fps)+
                "\noverwrite="+str(overwrite)+
                "\nmatrixsSize="+str(matrixSize)+
                "\nledSize="+str(ledSize))
        f.close()
    return fps,overwrite,matrixSize,ledSize


    
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
            for y in range(min(frame.size[1],len(pin.row))):
                if frame.get((x,y)):
                    GPIO.output(pin.row[y],GPIO.HIGH)
                    
            time.sleep(time.time()-startTime+(1/(fps*overwrite*matrixSize[0])))

def renderFramesList(frames,reverse = True):
    for frm in frames:
        renderFrameClass(frm,reverse)        

def importDict(name="./Matrix/letters 5x7.txt"):
    newDict={}
    f = open(name).read()
    x = f.split("\n\n")
    for char in x:
        y = char.split(" ")
        newDict[y[0]] = strToFrame(y[1].strip("\n"))
    newDict[" "] = strToFrame("000")
    return newDict

def strToFrame(string,forceSize=None):
    xs = string.split("\n")
    if forceSize != None:
        size = forceSize
    else:
        size = len(xs[0]),len(xs)
    newFrame = Frame(size, 0)
    x,y = 0,0
    for char in string:
        if char == "\n":
            x = 0
            y += 1
        else:
            newFrame.set((x,y), int(char))
            x += 1
    return newFrame

def importTextAni(name):
    newAni = []
    f = open("Matrix/animations/"+name).read()
    x = f.split("\n\n")
    if x[0].count("(") != 0:
        forceSize = tuple(int(z) for z in x[0].strip("()").split(",").strip())
        for frm in x[1:]:
            newAni.append(strToFrame(frm,forceSize))
    else:
        for frm in x[1:]:
            newAni.append(strToFrame(frm))
    return newAni

def genTextScrollAni(text,charset = None,gapBetweenChars=1,startBlank=True):
    if type(charset) != dict:
        charset = importDict()
    textl = list(text)
    frames = []
    straightFrame = Frame((len(text)*(charset["A"].size[0]+gapBetweenChars),charset["A"].size[1]))
    for x in range(len(textl)):
        straightFrame.blit(charset[textl[x]], (x*(charset["A"].size[0]+gapBetweenChars),0))
    if startBlank:
        for x in range(matrixSize[0]):
            newFrame = Frame((matrixSize[0],len(pin.row)))
            newFrame.blit(straightFrame,(matrixSize[0]-x,0),((0,0),(x,len(pin.row))))
            frames.append(newFrame)
    for x in range(straightFrame.size[0]):
        newFrame = Frame((matrixSize[0],len(pin.row)))
        newFrame.blit(straightFrame,(0,0),((x,0),newFrame.size))
        frames.append(newFrame)
    return frames
         
            
def main():
    try:
        global clock
        pygame.time.init()
        loadConfig()
        loadPi()
        clock = pygame.time.Clock()
        if len(sys.argv) == 1:
            x = genTextScrollAni("Hello, World!")
        else:
            if sys.argv[1].lower() == "text":
                x = genTextScrollAni(" ".join(sys.argv[2:]))
            elif sys.argv[1].lower() == "ani":
                x = importTextAni(" ".join(sys.argv[2:]))
            elif sys.argv[1].lower() == "test":
                chrs = importDict()
                x.genTextScrollAni("Hello, World! This is an alphabet test message." +"".join(list(chrs.keys()).sort()),chrs)
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
if __name__ == "__main__": main()
    
