import math
import random
import pygame
from Shoot_LoadOBJ import*

class Props:
    def __init__(self):
        self.lvl = 1
        self.route = None
        self.DronePOS = []
        self.DronePOSX = [0, 0, 0, 0, 0, 5, 15]
        self.Drone_track = -1
        self.DroneA_POS = []
        self.DroneB_POS = []
        self.DroneC_POS = []
        self.DroneA_Shoot = []   #create when drone mother meet plyr
        self.bullet_INFO = []
        self.bullet_POS = []
        self.LPoint_POS = []
        self.LBoom_POS = []
        self.shoot = False
        self.box_POS = []
        self.rot_deg = [0,0]
        self.bullet_count = 0
        self.bar = False
        self.powerup = []
        self.powerapply = 0
        self.powertime = 0
        self.shield = 0
        self.splash_POS = []
        self.splash = False
        self.effect = None
        self.mute = None

    def genList(self):
        self.Drone = [OBJ("External/", 'ufo.obj'), OBJ("External/", 'ufo2.obj')]
        for drone in self.Drone:
            drone.create_gl_list()
        self.DroneA = OBJ("External/", 'DroneA.obj')
        self.DroneA.create_gl_list()
        self.laser = OBJ("External/", 'laser.obj')
        self.laser.create_gl_list()
        self.box = OBJ("External/", 'box.obj')
        self.box.create_gl_list()
        self.splasheff = OBJ("External/", 'splasheff.obj')
        self.splasheff.create_gl_list()
        self.DroneB = OBJ("External/", 'DroneB.obj')
        self.DroneB.create_gl_list()
        self.Laserpoint = OBJ("External/", 'Laserpoint.obj')
        self.Laserpoint.create_gl_list()
        self.Lpointeff = OBJ("External/", 'Lpointeff.obj')
        self.Lpointeff.create_gl_list()
        self.DroneC = OBJ("External/", 'DroneC.obj')
        self.DroneC.create_gl_list()
        self.LBoom = OBJ("External/", 'LBoom.obj')
        self.LBoom.create_gl_list()
        self.LBoomside = OBJ("External/", 'LBoomside.obj')
        self.LBoomside.create_gl_list()

    def gameUPDATE(self):
        if self.lvl==1:
            self.DronePOS = [[-30,30,15, True], [-30,-30,15, True], [30,-30,15, True], [30,30,15, True]]
            self.box_POS = [[-28,-32,2,True], [-16,32,2,True], [48,28,2,True], [44,-40,2,True]]
            self.DroneB_POS = []
            self.LPoint_POS = []
            self.DroneC_POS = []
            self.LBoom_POS = []
            self.bullet_count = 150
            self.powerup = []
            self.powerapply = 0
        elif self.lvl==2:
            self.DronePOS = [[-42, 42, 15, True], [-42, -42, 15, True], [42, -42, 15, True], [42, 42, 15, True]]
            self.box_POS = [[-48, -48, 2, True], [-28, 16, 2, True], [28, 56, 2, True], [28, -52, 2, True], [40, -32, 2, True]]
            self.DroneB_POS = [[-42, -56, 3, 0, 0, False, 10],[-18, 32, 3, 0, 0, False, 10], [28, -16, 3, 0, 0, False, 10], [56, -56, 3, 0, 0, False, 10]]
            self.LPoint_POS = [[0, 0, 0, 0, False, 0, 0, 0,0,0], [0, 0, 0, 0, False, 0, 0, 0,0,0], [0, 0, 0, 0, False, 0, 0, 0,0,0], [0, 0, 0, 0, False, 0, 0, 0,0,0]]
            self.DroneC_POS = []
            self.LBoom_POS = []
            self.bullet_count += 150
        elif self.lvl==3:
            self.DronePOS = [[-54, 54, 15, True], [-54, -54, 15, True], [54, -54, 15, True], [54, 54, 15, True]]
            self.box_POS = [[-64, -40, 2, True], [-32, -44, 2, True], [-16, 68, 2, True], [16, -8, 2, True], [28, 44, 2, True], [68, -16, 2, True]]
            self.DroneB_POS = [[-66, -68, 3, 0, 0, False, 10], [-44, 40, 3, 0, 0, False, 10], [28, -48, 3, 0, 0, False, 10], [56, 8, 3, 0, 0, False, 10]]
            self.LPoint_POS = [[0, 0, 0, 0, False, 0, 0, 0,0,0], [0, 0, 0, 0, False, 0, 0, 0,0,0], [0, 0, 0, 0, False, 0, 0, 0,0,0], [0, 0, 0, 0, False, 0, 0, 0,0,0]]
            self.DroneC_POS = [[-30, -42, 4, 0, 0, False, 15],[18, 22, 4, 0, 0, False, 15]]
            self.LBoom_POS = [[0, 0, 0, 0, False, 0, 0, 0, 0, 0],[0, 0, 0, 0, False, 0, 0, 0, 0, 0]]
            self.bullet_count += 150
        self.Drone_track = -1
        self.DroneA_POS = []

    def update(self, ply_POS, health, time, Score_out):
        damage = score = 0
        self.rot_deg[0] += 1
        self.rot_deg[1] -= 15
        self.dronePath()
        self.droneDetect(ply_POS)
        self.droneAttack(ply_POS)
        damage += self.droneA_POS(ply_POS)
        score += self.bulletShoot()
        score += self.boxDetect(ply_POS)
        self.droneB_route(ply_POS)
        damage += self.droneB_attack(ply_POS)
        self.droneC_route(ply_POS)
        damage += self.DroneC_attack(ply_POS)

        if self.powerapply==1:
            if time>self.powertime or not damage == 0:
                self.powerapply = 0
        elif self.powerapply==2:
            if self.shield>0:
                self.shield -= damage
                if self.shield<0:
                    damage = abs(self.shield)
                else:
                    damage = 0
            if self.shield<=0:
                if not self.mute:
                    sound = pygame.mixer.Sound('External/deny.wav')
                    sound.play()
                self.powerapply = 0
        elif self.powerapply == 3:
            self.bullet_count += 1
            if time>self.powertime:
                self.powerapply = 0
                if not self.mute:
                    sound = pygame.mixer.Sound('External/deny.wav')
                    sound.play()
        elif self.powerapply == 4:
            if damage==0 and health<100:
                damage = -0.25
            else:
                if not self.mute:
                    sound = pygame.mixer.Sound('External/deny.wav')
                    sound.play()
                self.powerapply = 0
            if time>self.powertime:
                if not self.mute:
                    sound = pygame.mixer.Sound('External/deny.wav')
                    sound.play()
                self.powerapply = 0
        if health<=0:
            health = damage = 0
        return health-damage, Score_out+score

    def draw(self, ply_POS):
        self.drone(ply_POS)
        self.droneA()
        self.boxKEY(ply_POS)
        self.droneB()
        self.droneC()
        if self.bar:
            self.ufolight()
        if self.splash:
            glPushMatrix()
            glTranslate(self.splash_POS[0], self.splash_POS[1],self.splash_POS[2])
            glCallList(self.splasheff.gl_list)
            glPopMatrix()
            self.splash = False
    def droneC(self):
        if self.DroneC_POS:
            for i in range(len(self.DroneC_POS)):
                dC = self.DroneC_POS[i]

                if dC[5]:
                    glPushMatrix()
                    glTranslate(dC[0], dC[1], dC[2])
                    glRotate(dC[3], 0, 0, 1)
                    glRotate(dC[4], 0, 1, 0)
                    glCallList(self.DroneC.gl_list)
                    glPopMatrix()
                    LBoom = self.LBoom_POS[i]
                    if LBoom[4]:
                        glPushMatrix()
                        glTranslate(LBoom[0], LBoom[1], LBoom[2])
                        glCallList(self.LBoom.gl_list)
                        glRotate(self.rot_deg[1], 1, 0, 0)
                        glCallList(self.LBoomside.gl_list)
                        glRotate(self.rot_deg[1], 0, 1, 0)
                        glCallList(self.LBoomside.gl_list)
                        glPopMatrix()
                    
    def droneC_route(self, ply_POS):
        if self.DroneC_POS:
            for i in range(len(self.DroneC_POS)):
                dC = self.DroneC_POS[i]
                if not dC[5]:
                    if ply_POS[0]-15<dC[0]<ply_POS[0]+15 and ply_POS[1]-15<dC[1]<ply_POS[1]+15:
                        if not self.mute:
                            self.effect = pygame.mixer.Sound('External/droneCfly.wav')
                            self.effect.play()
                        dC[5] = True
                else:
                    if dC[6] == 0:
                        dC[2] -= 0.1
                        if dC[2] < 0:
                            dC[5] = False
                            self.DroneC_POS.pop(i)
                            self.LBoom_POS.pop(i)
                            break                        
                    dX = dY = dZ = 0
                    if ply_POS[0] > dC[0]:
                        dX = -(ply_POS[0] - dC[0])
                    elif ply_POS[0] < dC[0]:
                        dX = dC[0] - ply_POS[0]
                    if ply_POS[1] > dC[1]:
                        dY = -(ply_POS[1] - dC[1])
                    elif ply_POS[1] < dC[1]:
                        dY = dC[1] - ply_POS[1]
                    if ply_POS[2] > dC[2]:
                        dZ = ply_POS[2] - dC[2]
                    elif ply_POS[2] < dC[2]:
                        dZ = dC[2] - ply_POS[2]
                    if dX == 0:
                        dX = 1
                    if ply_POS[0] <= dC[0]:
                        dC[3] = math.degrees(math.atan(dY / dX)) + 180
                    else:
                        dC[3] = math.degrees(math.atan(dY / dX))
                    if abs(dX) > abs(dY):
                        dC[4] = math.degrees(math.atan(dZ / abs(dX)))
                    elif abs(dX) < abs(dY):
                        dC[4] = math.degrees(math.atan(dZ / abs(dY)))
                    if not ply_POS[0] - 4 < dC[0] < ply_POS[0] + 4 or not ply_POS[1] - 4 < dC[1] < ply_POS[1] + 4:
                        w, e, s = 1, 4, 0.3
                        x, y = [], []
                        ynear = xnear = 0
                        yn, xn = [], []
                        for i in range(len(self.route)):
                            road = self.route[i]
                            if road[0] <= dC[0] < road[0] + road[2]:
                                if road[1] - road[3] <= dC[1] < road[1]:
                                    y = [road[1], road[3]]
                                elif road[1] - road[3] - e <= dC[1] < road[1] + e:
                                    yn.append([road[1], road[3]])
                            if road[1] - road[3] <= dC[1] < road[1]:
                                if road[0] <= dC[0] < road[0] + road[2]:
                                    x = [road[0], road[2]]
                                elif road[0] - e <= dC[0] < road[0] + road[2] + e:
                                    xn.append([road[0], road[2]])
                        for i in range(len(yn)):
                            if yn[i] == y:
                                yn.pop(i)
                                break
                        for i in range(len(xn)):
                            if xn[i] == x:
                                xn.pop(i)
                                break
                        if yn:
                            ynn = yn[0]
                            if ynn[0] == y[0] - y[1]:
                                ynear = 1
                            elif ynn[0] - ynn[1] == y[0]:
                                ynear = -1
                        if xn:
                            xnn = xn[0]
                            if xnn[0] == x[0] + x[1]:
                                xnear = 1
                            elif xnn[0] + xnn[1] == x[0]:
                                xnear = -1
                        dC[0] += s * math.cos(math.radians(dC[3]))
                        dC[1] += s * math.sin(math.radians(dC[3]))
                        if dC[0] < x[0] + w and not xnear == -1:
                            dC[0] = x[0] + w
                        elif dC[0] > x[0] + x[1] - w and not xnear == 1:
                            dC[0] = x[0] + x[1] - w
                        if dC[1] < y[0] - y[1] + w and not ynear == 1:
                            dC[1] = y[0] - y[1] + w
                        elif dC[1] > y[0] - w and not ynear == -1:
                            dC[1] = y[0] - w

    def DroneC_attack(self, ply_POS):
        damage = 0
        if self.DroneC_POS:
            for k in range(len(self.DroneC_POS)):
                dC = self.DroneC_POS[k]
                LBoom = self.LBoom_POS[k]
                if dC[5] and not LBoom[4] and dC[6] > 0:
                    if not self.mute:
                        self.effect = pygame.mixer.Sound('External/plasma.wav')
                        self.effect.play()
                    LBoom[4] = True
                    LBoom[3] = 0
                    for d in range(5, 8):
                        LBoom[d] = dC[d - 5]
                    LBoom[8] = dC[3]
                    LBoom[9] = dC[4]
                if LBoom[4]:
                    LBoom[0] = LBoom[3] * math.cos(math.radians(LBoom[8])) + LBoom[5]
                    LBoom[1] = LBoom[3] * math.sin(math.radians(LBoom[8])) + LBoom[6]
                    LBoom[2] = -1 * LBoom[3] * math.tan(math.radians(LBoom[9])) + LBoom[7]
                    LBoom[3] += 0.45  # plasma speed
                    if self.collisionCircle(LBoom, ply_POS, 0.08 + 0.5, 3):
                        LBoom[4] = False
                        damage += 5
                    elif LBoom[2] < 0 or dC[6] <= 0:
                        LBoom[4] = False
                    else:
                        contact = True
                        for j in range(len(self.route)):
                            road = self.route[j]
                            if road[0] <= LBoom[0] < road[0] + road[2]:
                                if road[1] - road[3] <= LBoom[1] < road[1]:
                                    contact = False
                                    break
                        if contact:
                            LBoom[4] = False
        return damage
                                          
    def droneB(self):
        if self.DroneB_POS:
            for i in range(len(self.DroneB_POS)):
                dB = self.DroneB_POS[i]
                if dB[5]:
                    Lpoint = self.LPoint_POS[i]
                    glPushMatrix()
                    glTranslate(dB[0], dB[1], dB[2])
                    glRotate(dB[3], 0, 0, 1)
                    glRotate(dB[4], 0, 1, 0)
                    glCallList(self.DroneB.gl_list)
                    if Lpoint[3]<1:
                        glCallList(self.Lpointeff.gl_list)
                    glPopMatrix()
                    if Lpoint[4]:
                        glPushMatrix()
                        glTranslate(Lpoint[0], Lpoint[1], Lpoint[2])
                        glCallList(self.Laserpoint.gl_list)
                        glPopMatrix()

    def droneB_attack(self, ply_POS):
        damage = 0
        if self.DroneB_POS:
            for k in range(len(self.DroneB_POS)):
                dB = self.DroneB_POS[k]
                Lpoint = self.LPoint_POS[k]
                if dB[5] and not Lpoint[4] and dB[6]>0:
                    if not self.mute:
                        self.effect = pygame.mixer.Sound('External/plasma.wav')
                        self.effect.play()
                    Lpoint[4] = True
                    Lpoint[3] = 0
                    for d in range(5,8):
                        Lpoint[d] = dB[d-5]
                    Lpoint[8] = dB[3]
                    Lpoint[9] = dB[4]
                if Lpoint[4]:
                    Lpoint[0] = Lpoint[3] * math.cos(math.radians(Lpoint[8])) + Lpoint[5]
                    Lpoint[1] = Lpoint[3] * math.sin(math.radians(Lpoint[8])) + Lpoint[6]
                    Lpoint[2] = -1*Lpoint[3] * math.tan(math.radians(Lpoint[9])) + Lpoint[7]
                    Lpoint[3] += 0.3       #plasma speed
                    if self.collisionCircle(Lpoint, ply_POS, 0.05+0.5, 3):
                        Lpoint[4] = False
                        damage += 2.5
                    elif Lpoint[2]<0 or dB[6]<=0:
                        Lpoint[4] = False
                    else:
                        contact = True
                        for j in range(len(self.route)):
                            road = self.route[j]
                            if road[0] <= Lpoint[0] < road[0] + road[2]:
                                if road[1] - road[3] <= Lpoint[1] < road[1]:
                                    contact = False
                                    break
                        if contact:
                            Lpoint[4] = False
        return damage

    def droneB_route(self, ply_POS):
        if self.DroneB_POS and not self.powerapply==1:
            for i in range(len(self.DroneB_POS)):
                dB = self.DroneB_POS[i]
                if not dB[5] and dB[6]>0:
                    if ply_POS[0]-20<dB[0]<ply_POS[0]+20 and ply_POS[1]-20<dB[1]<ply_POS[1]+20:
                        dB[5] = True
                        if not self.mute:
                            self.effect = pygame.mixer.Sound('External/droneBfly.wav')
                            self.effect.play()
                else:
                    if not ply_POS[0]-15<dB[0]<ply_POS[0]+15 and not ply_POS[1]-15<dB[1]<ply_POS[1]+15:
                        dB[5] = False
                        break
                    elif dB[6]==0:
                        dB[2] -= 0.1
                        if dB[2]<0:
                            dB[5] = False
                            self.DroneB_POS.pop(i)
                            self.LPoint_POS.pop(i)
                        break
                    dX = dY = dZ = 0
                    if ply_POS[0] > dB[0]:
                        dX = -(ply_POS[0] - dB[0])
                    elif ply_POS[0] < dB[0]:
                        dX = dB[0] - ply_POS[0]
                    if ply_POS[1] > dB[1]:
                        dY = -(ply_POS[1] - dB[1])
                    elif ply_POS[1] < dB[1]:
                        dY = dB[1] - ply_POS[1]
                    if ply_POS[2] > dB[2]:
                        dZ = ply_POS[2] - dB[2]
                    elif ply_POS[2] < dB[2]:
                        dZ = dB[2] - ply_POS[2]
                    if dX == 0:
                        dX = 1
                    if ply_POS[0] <= dB[0]:
                        dB[3] = math.degrees(math.atan(dY / dX))+180
                    else:
                        dB[3] = math.degrees(math.atan(dY / dX))
                    if abs(dX) > abs(dY):
                        dB[4] = math.degrees(math.atan(dZ / abs(dX)))
                    elif abs(dX)<abs(dY):
                        dB[4] = math.degrees(math.atan(dZ / abs(dY)))
                    if not ply_POS[0]-4<dB[0]<ply_POS[0]+4 or not ply_POS[1]-4<dB[1]<ply_POS[1]+4:
                        w, e, s = 1, 4, 0.25
                        x, y = [], []
                        ynear = xnear = 0
                        yn, xn = [], []
                        for i in range(len(self.route)):
                            road = self.route[i]
                            if road[0] <= dB[0] < road[0] + road[2]:
                                if road[1] - road[3] <= dB[1] < road[1]:
                                    y = [road[1], road[3]]
                                elif road[1] - road[3] - e <= dB[1] < road[1] + e:
                                    yn.append([road[1], road[3]])
                            if road[1] - road[3] <= dB[1] < road[1]:
                                if road[0] <= dB[0] < road[0] + road[2]:
                                    x = [road[0], road[2]]
                                elif road[0] - e <= dB[0] < road[0] + road[2] + e:
                                    xn.append([road[0], road[2]])
                        for i in range(len(yn)):
                            if yn[i] == y:
                                yn.pop(i)
                                break
                        for i in range(len(xn)):
                            if xn[i] == x:
                                xn.pop(i)
                                break
                        if yn:
                            ynn = yn[0]
                            if ynn[0] == y[0] - y[1]:
                                ynear = 1
                            elif ynn[0] - ynn[1] == y[0]:
                                ynear = -1
                        if xn:
                            xnn = xn[0]
                            if xnn[0] == x[0] + x[1]:
                                xnear = 1
                            elif xnn[0] + xnn[1] == x[0]:
                                xnear = -1
                        dB[0] += s * math.cos(math.radians(dB[3]))
                        dB[1] += s * math.sin(math.radians(dB[3]))
                        if dB[0] < x[0] + w  and not xnear == -1:
                            dB[0] = x[0] + w 
                        elif dB[0] > x[0] + x[1] - w  and not xnear == 1:
                            dB[0] = x[0] + x[1] - w 
                        if dB[1] < y[0] - y[1] + w  and not ynear == 1:
                            dB[1] = y[0] - y[1] + w 
                        elif dB[1] > y[0] - w  and not ynear == -1:
                            dB[1] = y[0] - w 

    def ufolight(self):
        vtx,surf = [], []
        for k in range(1,3):
            for i in range(180):
                if k==1:
                    r = 0.5
                    if i==179:
                        surf.append((i, i -179, i + 1, i + 180))
                    else:
                        surf.append((i,i+1,i+181,i+180))
                    z = self.DronePOSX[2]
                else:
                    r = 3.5
                    z = self.DronePOSX[6]
                x = r * math.cos(math.radians(i * 2)) + self.DronePOSX[0]
                y = r * math.sin(math.radians(i * 2)) + self.DronePOSX[1]
                vtx.append((x, y, z))
        color = ((3/255,215/255,26/255,1), (3/255,215/255,26/255,1), (151/255,1,202/255,0.6), (151/255,1,202/255,0.6))
        glBegin(GL_QUADS)
        for surface in surf:
            n = 0
            for vertex in surface:
                glColor4fv(color[n])
                glVertex3fv(vtx[vertex])
                n += 1
        glEnd()


    def boxDetect(self, ply_POS):
        score = 0
        if self.box_POS:
            for i in range(len(self.box_POS)):
                box = self.box_POS[i]
                if self.collisionCircle(box, ply_POS, 4, 2):
                    self.box_POS.pop(i)
                    self.powerup.append(random.randint(1,4))
                    score = 80
                    if not self.mute:
                        self.effect = pygame.mixer.Sound('External/box.wav')
                        self.effect.play()
                    break
        return score

    def boxKEY(self, ply_POS):
        for i in range(len(self.box_POS)):
            box = self.box_POS[i]
            if box[0]-30<ply_POS[0]<box[0]+30 and box[1]-30<ply_POS[1]<box[1]+30:
                glPushMatrix()
                if box[3]:
                    box[2] += 0.02
                    if box[2]>2.5:
                        box[3] = False
                else:
                    box[2] -= 0.02
                    if box[2] < 1.5:
                        box[3] = True
                glTranslate(box[0], box[1], box[2])
                glRotate(self.rot_deg[0], 1,1,1)
                glCallList(self.box.gl_list)
                glPopMatrix()

    def bulletInit(self, pos, xy_deg, z_deg):
        if self.shoot and self.bullet_count>0:
            if not self.mute:
                self.effect = pygame.mixer.Sound('External/bullet.wav')
                self.effect.play()
            self.bullet_INFO.append([pos[0], pos[1], pos[2], xy_deg, z_deg, 0])
            self.bullet_POS.append([0,0,0])
            self.bullet_count -= 1
            self.shoot = False

    def bulletShoot(self):
        score = 0
        if self.bullet_INFO and not self.bar:
            n = 0
            for i in range(len(self.bullet_INFO)):
                bullet = self.bullet_INFO[i-n]
                bullpos = self.bullet_POS[i-n]
                bullpos[0] = bullet[5]*math.cos(math.radians(bullet[3]))+bullet[0]
                bullpos[1] = bullet[5]*math.sin(math.radians(bullet[3]))+bullet[1]
                bullpos[2] = bullet[5]*math.tan(math.radians(bullet[4]))+bullet[2]
                bullet[5] += 2
                dist = math.sqrt((bullet[0]-bullpos[0])**2+(bullet[1]-bullpos[1])**2)
                if dist>30:
                    boom = True
                else:
                    boom = True
                    if bullpos[2]<=4:
                        for j in range(len(self.route)):
                            road = self.route[j]
                            if road[0] <= bullpos[0] < road[0] + road[2]:
                                if road[1] - road[3] <= bullpos[1] < road[1]:
                                    boom = False
                                    break
                    else:
                        boom = False
                    if self.DroneB_POS and not boom:
                        for dB in self.DroneB_POS:
                            if dB[5] and dB[6]>0:
                                boom =  self.collisionCircle(bullpos, dB, 0.5+0.1, 3)
                                if boom:
                                    dB[6] -= 1
                                    break
                    if self.DroneC_POS and not boom:
                        for dC in self.DroneC_POS:
                            if dC[5] and dC[6]>0:
                                boom =  self.collisionCircle(bullpos, dC, 0.45+0.1, 3)
                                if boom:
                                    dC[6] -= 1
                                    break
                    if self.Drone_track>-1 and self.DroneA_POS and not boom:
                        for k in range(len(self.DroneA_POS)):
                            dA_POS = self.DroneA_POS[k]
                            if dA_POS[5]>0:
                                boom = self.collisionCircle(bullpos, dA_POS, 0.5+0.3,3)
                                if boom:
                                    dA_POS[5] -= 1
                                    break
                    elif self.Drone_track>-1 and self.DronePOSX[5]>0 and not boom:
                        boom = self.collisionCircle(bullpos, self.DronePOSX, 2+0.3,3)
                        if boom:
                            self.DronePOSX[5] -= 1
                            if self.DronePOSX[5]==0:
                                self.Drone_track = -1
                if boom:
                    self.splash = True
                    self.splash_POS = [bullpos[0], bullpos[1], bullpos[2]]
                    self.bullet_INFO.pop(i-n)
                    self.bullet_POS.pop(i-n)
                    score = 100
                    n += 1
        return score

    def collisionCircle(self, A, B, distance, dim):
        dX = dY = dZ = 0
        dist = distance
        if A[0] > B[0]:
            dX = A[0] - B[0]
        elif A[0] < B[0]:
            dX = B[0] - A[0]
        if A[1] > B[1]:
            dY = A[1] - B[1]
        elif A[1] < B[1]:
            dY = B[1] - A[1]
        if dim==3:
            if A[2] > B[2]:
                dZ = A[2] - B[2]
            elif A[2] < B[2]:
                dZ = B[2] - A[2]
            dist = math.sqrt((dX ** 2) + (dY ** 2) + (dZ ** 2))
        elif dim==2:
            dist = math.sqrt((dX ** 2) + (dY ** 2))
        if dist < distance:
            return True
        else:
            return False
        
    def droneA(self):
        if self.Drone_track>-1:
            for i in range(len(self.DroneA_POS)):
                dA_POS = self.DroneA_POS[i]
                if dA_POS[5]>-1:
                    glPushMatrix()
                    glTranslate(dA_POS[0], dA_POS[1], dA_POS[2])
                    if dA_POS[3]==0:
                        glRotate(45, 1, 0, 0)
                    elif dA_POS[3]==90:
                        glRotate(-45, 0, 1, 0)
                    elif dA_POS[3]==180:
                        glRotate(-45, 1, 0, 0)
                    elif dA_POS[3]==270:
                        glRotate(45, 0, 1, 0)
                    glRotate(-dA_POS[3], 0, 0, 1)
                    glCallList(self.DroneA.gl_list)
                    glPopMatrix()
                    dA_SHOOT = self.DroneA_Shoot[i]
                    if dA_POS[5]>0:
                        glPushMatrix()
                        glTranslate(dA_SHOOT[0], dA_SHOOT[1], dA_SHOOT[2])
                        if dA_POS[3]==0:
                            glRotate(45, 1, 0, 0)
                        elif dA_POS[3]==90:
                            glRotate(-45, 0, 1, 0)
                        elif dA_POS[3]==180:
                            glRotate(-45, 1, 0, 0)
                        elif dA_POS[3]==270:
                            glRotate(45, 0, 1, 0)
                        glRotate(-dA_POS[3], 0, 0, 1)
                        glCallList(self.laser.gl_list)
                        glPopMatrix()

    def droneA_POS(self, ply_POS):
        w,n, damage = 4,0,0
        if self.Drone_track>-1:
            for i in range(len(self.DroneA_POS)):
                dA_POS = self.DroneA_POS[i-n]
                dA_POS[0] = w * math.sin(math.radians(dA_POS[3])) + ply_POS[0]
                dA_POS[1] = w * math.cos(math.radians(dA_POS[3])) + ply_POS[1]
                if dA_POS[5]==0:
                    if not self.mute and dA_POS[6]:
                        dA_POS[6] = False
                        self.effect = pygame.mixer.Sound('External/droneAFall.wav')
                        self.effect.play()
                    dA_POS[2] -= 0.1
                    if dA_POS[2]<-0.5:
                        dA_POS[5] = -1
                elif dA_POS[2]<dA_POS[4]:
                    dA_POS[2] += 0.1        #arise from ground
                else:
                    dA_SHOOT = self.DroneA_Shoot[i-n]
                    if dA_POS[3]==0 or dA_POS[3]==90:
                        deg = 45 + 180
                    else:
                        deg = -45 + 180
                    if dA_POS[3]==90 or dA_POS[3]==270:
                        dA_SHOOT[0] = dA_SHOOT[3] * math.sin(math.radians(deg)) + dA_POS[0]
                        dA_SHOOT[1] = dA_POS[1]
                        dA_SHOOT[2] = dA_SHOOT[3] * math.cos(math.radians(deg)) + dA_POS[2]
                    else:
                        dA_SHOOT[0] = dA_POS[0]
                        dA_SHOOT[1] = dA_SHOOT[3] * math.sin(math.radians(deg)) + dA_POS[1]
                        dA_SHOOT[2] = dA_SHOOT[3] * math.cos(math.radians(deg)) + dA_POS[2]
                    if dA_SHOOT[3]<dA_POS[2]:
                        dA_SHOOT[3] += 1      #shoot speed
                    else:
                        if dA_POS[5]>0:
                            damage += 0.1# deduct plyr live
                            if not self.mute and len(self.DroneA_POS)==i+1:
                                self.effect = pygame.mixer.Sound('External/laser.wav')
                                self.effect.play()
                            dA_SHOOT[3] = 0
                if dA_POS[5]==-1:
                    self.DroneA_POS.pop(i-n)
                    n += 1
        return damage

    def drone(self, ply_pos):
        r = 30
        for i in range(4):
            if self.Drone_track==i:
                drone_POS = self.DronePOSX
            else:
                drone_POS = self.DronePOS[i]
            if ply_pos[0]-r<drone_POS[0]<ply_pos[0]+r and ply_pos[1]-r<drone_POS[1]<ply_pos[1]+r:
                if ply_pos[0] - r/2 < drone_POS[0] < ply_pos[0] + r/2 and ply_pos[1] - r/2 < drone_POS[1] < ply_pos[1] + r/2:
                    if not self.mute and drone_POS[3] and not self.Drone_track==i:
                        drone_POS[3] = False
                        self.effect = pygame.mixer.Sound('External/ufofly.wav')
                        self.effect.play()
                glPushMatrix()
                glTranslate(drone_POS[0], drone_POS[1], drone_POS[2])
                glCallList(self.Drone[0].gl_list)
                glRotate(self.rot_deg[1], 0, 0, 1)
                glCallList(self.Drone[1].gl_list)
                glPopMatrix()

    def droneAttack(self, ply_POS):
        if self.Drone_track>-1:
            drone_POSX = self.DronePOSX
            if drone_POSX[4]>0:
                drone_POSX[0] = drone_POSX[4]*math.sin(math.radians(drone_POSX[3])) + ply_POS[0]
                drone_POSX[1] = drone_POSX[4]*math.cos(math.radians(drone_POSX[3])) + ply_POS[1]
                drone_POSX[3] -= 1      #deg, circular movement
                drone_POSX[4] -= 0.006
                if drone_POSX[4]<0:
                    drone_POSX[4]=0
                    for dA_POS in self.DroneA_POS:
                        dA_POS[5] = 0   #remove drone baby
            elif drone_POSX[4]==0:
                self.bar = True
                if drone_POSX[6]>0:
                    drone_POSX[6] -= 0.1
                    if int(drone_POSX[6])==0 and not self.mute:
                        self.effect.stop()
                        self.effect = pygame.mixer.Sound('External/ufoAbsorb.wav')
                        self.effect.play()


    def droneDetect(self, ply_POS):
        if self.Drone_track == -1 and not self.powerapply==1:
            distX = distY = 0
            for i in range(len(self.DronePOS)):
                drone_POS = self.DronePOS[i]
                if ply_POS[0]>drone_POS[0]:
                    distX = -(ply_POS[0] - drone_POS[0])
                elif ply_POS[0]<drone_POS[0]:
                    distX = drone_POS[0] - ply_POS[0]
                if ply_POS[1] > drone_POS[1]:
                    distY = -(ply_POS[1] - drone_POS[1])
                elif ply_POS[1] < drone_POS[1]:
                    distY = drone_POS[1] - ply_POS[1]
                distance = math.sqrt((distX ** 2) + (distY ** 2))
                if distance < 1+8:
                    self.Drone_track = i
                    drone_POSX = self.DronePOSX
                    drone_POSX[4] = round(distance,2)
                    drone_POSX[3] = math.degrees(math.atan(distY / distX))+90
                    drone_POSX[2] = drone_POSX[6] = drone_POS[2]-2
                    drone_POSX[5] = 5   #life
                    for j in range(4):
                        dist = round(random.uniform(5, 6), 2)
                        self.DroneA_POS.append([0, 0, 0, j * 90, dist, 3, True])  #create baby drone
                    self.DroneA_Shoot = [[0, 0, 0,0], [0, 0, 0,0], [0, 0, 0,0], [0, 0, 0,0]]  # create laser path for baby drone
                    break

    def dronePath(self):
        minX = maxX = minY = maxY = speed = 0
        if self.lvl==1:
            minX, maxX, minY, maxY = -30,30,-30,30
            speed = 0.2
        elif self.lvl == 2:
            minX, maxX, minY, maxY = -42,42,-42,42
            speed = 0.3
        elif self.lvl == 3:
            minX, maxX, minY, maxY = -54,54,-54,54
            speed = 0.5
        for i in range(len(self.DronePOS)):
            drone_POS = self.DronePOS[i]
            move = 0
            if drone_POS[1] == maxY:
                move = 4
                if drone_POS[0]==maxX:
                    move = 2
            elif drone_POS[1] == minY:
                move = 3
                if drone_POS[0]==minX:
                    move = 1
            elif drone_POS[0]==minX:
                move = 1
                if drone_POS[1] == maxY:
                    move = 4
            elif drone_POS[0] == maxX:
                move = 2
                if drone_POS[1] == minY:
                    move = 3
            if move ==1:
                drone_POS[1] += speed
            elif move==2:
                drone_POS[1] -=speed
            elif move==3:
                drone_POS[0] -= speed
            elif move==4:
                drone_POS[0] += speed
            if drone_POS[0]==minX and drone_POS[1]==minY:
                drone_POS[3] = True  #restore warning sound
            self.DronePOS[i] = [round(num, 2) for num in drone_POS]