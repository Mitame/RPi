#!/usr/bin/env python3

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
                if frame.withinLimits((x+area[0][0],y+area[0][1])) and self.withinLimits((x+pos[0],y+pos[1])):
                    self.set((x+pos[0],y+pos[1]),frame.get((x+area[0][0],y+area[0][1])))
                elif self.withinLimits((x+pos[0],y+pos[1])):
                    self.set((x+pos[0],y+pos[1]),0)
                else:
                    pass

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
