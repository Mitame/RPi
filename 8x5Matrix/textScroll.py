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
    
try:
    f = open("conf").read().split("\n")
    fps = int(f[0])
    overwrite = int(f[1])
    columns = int(f[2])
except:
    f = open("conf","w")
    f.write("2\n75\n8")
    f.close()
    fps = 2
    overwrite = 75
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
            self[self.size[0]*pos[1]+pos[0]] = value
        else:
            raise IndexError("Position  %s is outside the limits of the frame" % str(pos))
    
    def get(self,pos):
        if self.withinLimits(pos):
            return self[self.size[0]*pos[1]+pos[0]]
        else:
            raise IndexError("Position  %s is outside the limits of the frame" % str(pos))
    
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
            newlist.append(self[self.size[0]*z:self.size[0]*(z+1)])
        retlist = []
        for list in newlist:
            list.reverse()
            retlist.extend(list)
        self.list = retlist
        
    def blit(self,frame,pos,area=None):
        if area is None:
            area = ((0,0),frame.size)
        for y in range(min(frame.size[1],area[1][1])):
            for x in range(min(frame.size[0],area[1][0])):
                if frame.withinLimits((x+area[0][0],y+area[0][1])):
                    self.set((x+pos[0],y+pos[1]),frame.get((x+area[0][0],y+area[0][1])))
                else:
                    self.set((x+pos[0],y+pos[1]),0)

    def __list__(self):
        return self.list
    
    def __getitem__(self,key):
        return self.list[key]
    
    def __setitem__(self,key,value):
        try:
            self.list[key] = value
        except IndexError:
            print(key,len(self.list))
    
    def __str__(self):
        newStr = ""
        for x in range(self.size[1]):
            newStr += "".join(str(x) for x in self.list[self.size[0]*x:self.size[0]*(x+1)])+"\n"
        return newStr
    
def pulse(on):
    GPIO.output(on,GPIO.HIGH)
    GPIO.output(on,GPIO.LOW)
    
def lowAll():
    for on in [pin.row0,pin.row1,
            pin.row2,pin.row3,
            pin.row4]:
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
                    GPIO.output((pin.row0,pin.row1,pin.row2,pin.row3,pin.row4)[y],GPIO.HIGH)
                    
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
    

def importDict(name="letters 5x5.txt"):
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
    size = len(xs),len(xs[0])
    oneline = string.replace("\n","")
    newFrame = Frame(size, 0)
    for bit in range(len(oneline)):
        newFrame[bit] = int(oneline[bit])
    return newFrame

def importTextAni(name):
    newAni = []
    f = open("animations/"+name).read()
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
    return frames,straightFrame
         
            
        
if __name__ == "__main__":
    try:
        x = genTextScrollAni("Hello, World!")[0]
        while 1:
            renderFramesList(x,False)
    except KeyboardInterrupt:
        pass
    pulse(pin.columnReset)
    GPIO.cleanup()
