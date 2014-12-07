import pygame
import sys
import copy
import time
ledSize = (50,50)
matrixSize = (8,5)

class images():
    on = pygame.Surface(ledSize)
    off = pygame.Surface(ledSize)
pygame.draw.circle(images.on,(0,255,0),tuple(ledSize[x]//2 for x in range(2)),ledSize[0]//2)
pygame.draw.circle(images.off,(50,50,50),tuple(ledSize[x]//2 for x in range(2)),ledSize[0]//2)

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
    
def getInput():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = tuple(event.pos[x]//ledSize[x] for x in range(2))
            curFrame.set(pos,int(not bool(curFrame.get(pos))))
            render()
        elif event.type == pygame.KEYDOWN:
            if event.unicode == "n":
                newFrameList.append(copy.deepcopy(curFrame))
                print("Added frame to list")
            elif event.unicode == "c":
                for x in range(len(curFrame.list)):
                    curFrame.list[x] = 0
                render()
                print("Cleared frame")
            elif event.unicode == "s":
                if len(sys.argv) > 1:
                    f = open("./%s" % " ".join(sys.argv[1]),"w")
                else:
                    f = open("./temp","w")
                f.write("\n".join(str(frame) for frame in newFrameList))
                f.close()
                print("Saved %s frames" % str(len(newFrameList)))
            elif event.unicode == "l":
                curFrame.scroll()
                print("Scrolled to the left")
                render()
        elif event.type == pygame.QUIT:
            raise SystemExit
        
def render():
    screen.fill((0,0,0))
    for x in range(matrixSize[0]):
        for y in range(matrixSize[1]):
            if curFrame.get((x,y)):
                screen.blit(images.on,(x*ledSize[0],y*ledSize[1]))
            else:
                screen.blit(images.off,(x*ledSize[0],y*ledSize[1]))
    pygame.display.flip()

def main():
    global newFrameList,curFrame,screen
    newFrameList = []
    curFrame = Frame(matrixSize,0)
    screen = pygame.display.set_mode(tuple(ledSize[x]*matrixSize[x] for x in range(2)))
    render()
    while 1:
        getInput()
        time.sleep(1/30)

if __name__ == "__main__":
    main()