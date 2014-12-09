import pygame
import sys
import copy
import time
import os


if os.path.curdir.split("/")[-1] == "Matrix":
    os.chdir("..")

from Matrix.objects import Frame
from Matrix.run import loadConfig

def loadImages():
    global images
    class images():
        on = pygame.Surface(ledSize)
        off = pygame.Surface(ledSize)
    pygame.draw.circle(images.on,(0,255,0),tuple(ledSize[x]//2 for x in range(2)),ledSize[0]//2)
    pygame.draw.circle(images.off,(50,50,50),tuple(ledSize[x]//2 for x in range(2)),ledSize[0]//2)


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
    global newFrameList,curFrame,screen,fps,overwrite,matrixSize,ledSize
    fps,overwrite,matrixSize,ledSize = loadConfig()
    loadImages()
    newFrameList = []
    curFrame = Frame(matrixSize,0)
    screen = pygame.display.set_mode(tuple(ledSize[x]*matrixSize[x] for x in range(2)))
    render()
    while 1:
        getInput()
        time.sleep(1/30)

if __name__ == "__main__":
    main()