from Matrix import run, objects
import time
import pygame


def genLedImages():
    global images
    class images():
        on = pygame.Surface(ledSize)
        off = pygame.Surface(ledSize)
    pygame.draw.circle(images.on,(0,255,0),tuple(ledSize[x]//2 for x in range(2)),ledSize[0]//2)
    pygame.draw.circle(images.off,(50,50,50),tuple(ledSize[x]//2 for x in range(2)),ledSize[0]//2)

def getPygameInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #@UndefinedVariable
            raise SystemExit
def commandLine():
    while 1:
        pygame.event.pump()
        command = input(">")
        comL = list(command.split(" "))
        comL[0] = comL[0].lower()
        try:
            if comL[0] == "play":
                try:
                    ani = run.importTextAni(" ".join(comL[1:]))
                    renderFrameList(ani)
                except FileNotFoundError:
                    print("No animation called %s." % " ".join(comL[1:]))
            elif comL[0] == "set":
                comL[1] = comL[1].lower()
                if comL[1] == "fps":
                    fps = int(comL[2])
                elif comL[1] == "overwrite":
                    overwrite = int(comL[2])
                    print("Note: This does not make any difference to the pygame version")
                else:
                    print("Invalid set command.")
            elif comL[0] == "text":
                try:
                    charset
                except NameError:
                    charset = run.importDict("./Matrix/letters 5x7.txt")
                    run.charset = charset
                ani = run.genTextScrollAni(" ".join(comL[1:]), charset, True, True)
                renderFrameList(ani)
            elif comL[0] == "test":
                try:
                    charset
                except NameError:
                    charset = run.importDict("./Matrix/letters 5x7.txt")
                    run.charset = charset
                keys = []
                keys.extend(charset.keys())
                keys.sort()
                ani = run.genTextScrollAni("Hello, World! This is an alphabet test message." +"".join(keys),charset)
                renderFrameList(ani)
            else:
                print("Unrecognised command '%s'." % comL[0])
            
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
        
def renderScreen():
    pygame.event.pump()
    for x in range(matrixSize[0]):
        for y in range(matrixSize[1]):
            if screenFrame.get((x,y)) == 1:
                screen.blit(images.on,tuple((x,y)[i]*ledSize[i] for i in range(2)))
            elif screenFrame.get((x,y)) == 0:
                screen.blit(images.off,tuple((x,y)[i]*ledSize[i] for i in range(2)))
    pygame.display.flip()
    

def renderFrameClass(frame,reverse = None):
    screenFrame.blit(frame,(0,0),((0,0),frame.size))
    renderScreen()
    
def renderFrameList(frameList):
    for frame in frameList:
        renderFrameClass(frame)
        time.sleep(1/fps)
    
def main():
    global fps,overwrite,matrixSize,ledSize,screenFrame,screen
    pygame.init()
    fps,overwrite,matrixSize,ledSize = run.loadConfig()
    genLedImages()
    screenFrame = objects.Frame(matrixSize)
    screen = pygame.display.set_mode(tuple(matrixSize[i]*ledSize[i] for i in range(2)))
    renderScreen() 
    commandLine()
    
if __name__ == "__main__": main()

    