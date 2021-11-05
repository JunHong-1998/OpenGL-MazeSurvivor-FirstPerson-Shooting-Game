import math
from OpenGL.GL import *

class Player:
    def __init__(self):
        self.lvl = 1
        self.pos = [0,0,0]
        self.route = []
        self.z_deg = 0
        self.speed = 0.3
        self.health = 100

    def routeUPDATE(self):
        if self.lvl==1:
            self.pos = [-46, -6,2]
        elif self.lvl==2:
            self.pos = [-58, -6,2]
        elif self.lvl==3:
            self.pos = [-70, -6,2]
        self.z_deg = 0

    def moveUPDATE(self, moveUD, moveLR):
        w,e = 1, 4
        x,y = [],[]
        ynear = xnear = 0
        yn, xn = [],[]
        for i in range(len(self.route)):
            road = self.route[i]
            if road[0]<=self.pos[0]<road[0]+road[2]:
                if road[1]-road[3]<=self.pos[1]<road[1]:
                    y = [road[1], road[3]]
                elif road[1]-road[3]-e<=self.pos[1]<road[1]+e:
                    yn.append([road[1], road[3]])
            if road[1] - road[3] <= self.pos[1] < road[1]:
                if road[0] <= self.pos[0] < road[0] + road[2]:
                    x = [road[0], road[2]]
                elif road[0]-e <= self.pos[0] < road[0] + road[2]+e:
                    xn.append([road[0], road[2]])
        for i in range(len(yn)):
            if yn[i]==y:
                yn.pop(i)
                break
        for i in range(len(xn)):
            if xn[i]==x:
                xn.pop(i)
                break
        if yn:
            ynn = yn[0]
            if ynn[0]==y[0]-y[1]:
                ynear = 1
            elif ynn[0]-ynn[1]==y[0]:
                ynear = -1
        if xn:
            xnn = xn[0]
            if xnn[0]==x[0]+x[1]:
                xnear = 1
            elif xnn[0]+xnn[1]==x[0]:
                xnear = -1
        if moveLR==1:
            self.z_deg += 3
        elif moveLR==2:
            self.z_deg -= 3
        if self.z_deg>360:
            self.z_deg -= 360
        elif self.z_deg<0:
            self.z_deg += 360
        if moveUD == 1:
            self.pos[0] += self.speed*math.cos(math.radians(self.z_deg))
            self.pos[1] += self.speed*math.sin(math.radians(self.z_deg))
        elif moveUD == 2:
            self.pos[0] -= self.speed * math.cos(math.radians(self.z_deg))
            self.pos[1] -= self.speed * math.sin(math.radians(self.z_deg))

        if self.pos[0]<x[0]+w+0.3*e and not xnear==-1:
            self.pos[0] = x[0]+w+0.3*e
        elif self.pos[0]>x[0]+x[1]-w-0.3*e and not xnear==1:
            self.pos[0] = x[0]+x[1]-w-0.3*e
        if self.pos[1]<y[0]-y[1]+w+0.3*e and not ynear==1:
            self.pos[1] = y[0]-y[1]+w+0.3*e
        elif self.pos[1]>y[0]-w-0.3*e and not ynear==-1:
            self.pos[1] = y[0]-w-0.3*e
