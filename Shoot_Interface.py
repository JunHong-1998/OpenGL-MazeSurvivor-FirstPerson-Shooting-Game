import math
import random
from OpenGL.GLUT import *
from Shoot_LoadOBJ import*

class Interface:
    def __init__(self):
        self.page = 0  #0
        self.box_appr = []
        self.rot_deg = 0
        self.shoot = False
        self.lvl = 0
        self.displaypower = -1
        self.powerlist = []
        self.time_display = 0
        self.time_passed = 0
        self.blit = False
        self.timerecord = [0,0,0]
        self.score = [0,0,0]
        self.loadcount = 0
        self.star = []

    def genList(self):
        self.plyview = OBJ("External/", 'user.obj')
        self.plyview.create_gl_list()
        self.splash = OBJ("External/", 'Splash.obj')
        self.splash.create_gl_list()
        self.invisible = OBJ("External/", 'invisible.obj')
        self.invisible.create_gl_list()
        self.shield = OBJ("External/", 'shield.obj')
        self.shield.create_gl_list()
        self.heal = OBJ("External/", 'heal.obj')
        self.heal.create_gl_list()
        self.reloadammo = OBJ("External/", 'reloadammo.obj')
        self.reloadammo.create_gl_list()
        self.reloadammoX = OBJ("External/", 'reloadammoX.obj')
        self.reloadammoX.create_gl_list()
        self.menuview = OBJ("External/", 'menuview.obj')
        self.menuview.create_gl_list()
        self.lvl_warn = OBJ("External/", 'lvl_warn.obj')
        self.lvl_warn.create_gl_list()
        self.lvl_mission = OBJ("External/", 'level_complete.obj')
        self.lvl_mission.create_gl_list()
        self.Control = OBJ("External/", 'Control.obj')
        self.Control.create_gl_list()
        self.Instruction = OBJ("External/", 'Instruction.obj')
        self.Instruction.create_gl_list()
        self.Load = OBJ("External/", 'load.obj')
        self.Load.create_gl_list()
        self.word = OBJ("External/", 'word.obj')
        self.word.create_gl_list()
        for k in range(500):
            x = random.choice([1,-1])*random.randint(1,15)
            y = random.choice([1,-1])*random.randint(1,10)
            z = random.choice([1,-1])*random.randint(1,23)
            vel = random.uniform(0.01,0.1)
            size = random.uniform(1.5,3.5)
            self.star.append([x,y,z,vel,size])

    def draw_lvl(self, lvl_warn, lvl_complete, lvl_fail):
        if lvl_complete or lvl_fail:
            glPushMatrix()
            glScalef(0.725, 0.725, 0.725)
            glTranslate(0, 0, -4.9)
            glCallList(self.lvl_mission.gl_list)
            glPopMatrix()
            glColor3f(1, 1, 1)
            if lvl_complete:
                self.DisplayText("MISSION COMPLETE", (600, 490), 1)
                self.DisplayText("MISSION COMPLETE", (602, 490), 1)
            else:
                self.DisplayText("MISSION FAILED", (600, 490), 1)
                self.DisplayText("MISSION FAILED", (602, 490), 1)
            self.DisplayText("L E V E L", (560, 450), 1)
            self.DisplayText("L E V E L", (562, 450), 1)
            self.DisplayText(str(self.lvl), (675, 450), 1)
            self.DisplayText(str(self.lvl), (677, 450), 1)
            self.DisplayText("T I M E", (450, 400), 1)
            self.DisplayText("H E A L T H", (450, 360), 1)
            self.DisplayText("S C O R E", (450, 320), 1)
            self.DisplayText("TOTAL_S C O R E", (450, 280), 1)
            self.DisplayText(str(self.timerecord[self.lvl-1]), (720, 400), 1)
            self.DisplayText(str(self.health), (720, 360), 1)
            self.DisplayText(str(self.score[self.lvl-1]), (720, 320), 1)
            self.DisplayText(str(sum(self.score)), (720, 280), 1)
            if self.blit:
                glColor3f(1, 0, 0.5)
                self.DisplayText("CLICK TO CONTINUE", (500, 585), 1)
        if self.lvl>0 and lvl_warn<self.lvl:
            glColor3f(1,1,1)
            self.DisplayText("L I F E", (350, 440), 1)
            self.DisplayText("L I F E", (352, 440), 1)
            self.DisplayText("MOBILITY", (245, 315), 1)
            self.DisplayText("MOBILITY", (247, 315), 1)
            self.DisplayText("W A R N", (820, 440), 1)
            self.DisplayText("W A R N", (822, 440), 1)
            self.DisplayText("DAMAGE", (900, 315), 1)
            self.DisplayText("DAMAGE", (902, 315), 1)
            glPointSize(23)
            glBegin(GL_POINTS)
            glColor3f(1,1,1)
            if self.lvl==1:
                glColor3f(1,0,0)
                glVertex3f(0.45, 0.05, -4)
                glVertex3f(-0.45, 0.05, -4)
                glVertex3f(-0.41, 0.05, -4)
                glVertex3f(-0.37, 0.05, -4)
                glVertex3f(-0.33, 0.05, -4)
                glVertex3f(-0.29, 0.05, -4)
                glVertex3f(0.58, -0.14, -4)
                glVertex3f(0.54, -0.14, -4)
                glVertex3f(0.5, -0.14, -4)
                glVertex3f(0.46, -0.14, -4)
                glVertex3f(0.42, -0.14, -4)
                glVertex3f(-0.42, -0.14, -4)
                glColor3f(1, 1, 1)
                glVertex3f(0.41, 0.05, -4)
                glVertex3f(0.37, 0.05, -4)
                glVertex3f(0.33, 0.05, -4)
                glVertex3f(0.29, 0.05, -4)
                glVertex3f(-0.58, -0.14, -4)
                glVertex3f(-0.54, -0.14, -4)
                glVertex3f(-0.5, -0.14, -4)
                glVertex3f(-0.46, -0.14, -4)
            elif self.lvl==2:
                glColor3f(1,0,0)
                glVertex3f(0.45, 0.05, -4)
                glVertex3f(0.41, 0.05, -4)
                glVertex3f(0.37, 0.05, -4)
                glVertex3f(-0.37, 0.05, -4)
                glVertex3f(-0.33, 0.05, -4)
                glVertex3f(-0.29, 0.05, -4)
                glVertex3f(0.58, -0.14, -4)
                glVertex3f(0.54, -0.14, -4)
                glVertex3f(-0.5, -0.14, -4)
                glVertex3f(-0.46, -0.14, -4)
                glVertex3f(-0.42, -0.14, -4)
                glColor3f(1,1,1)
                glVertex3f(0.33, 0.05, -4)
                glVertex3f(0.29, 0.05, -4)
                glVertex3f(-0.45, 0.05, -4)
                glVertex3f(-0.41, 0.05, -4)
                glVertex3f(0.5, -0.14, -4)
                glVertex3f(0.46, -0.14, -4)
                glVertex3f(0.42, -0.14, -4)
                glVertex3f(-0.58, -0.14, -4)
                glVertex3f(-0.54, -0.14, -4)
            elif self.lvl==3:
                glColor3f(1,0,0)
                glVertex3f(0.45, 0.05, -4)
                glVertex3f(0.41, 0.05, -4)
                glVertex3f(0.37, 0.05, -4)
                glVertex3f(0.33, 0.05, -4)
                glVertex3f(0.29, 0.05, -4)
                glVertex3f(-0.29, 0.05, -4)
                glVertex3f(0.58, -0.14, -4)
                glVertex3f(0.54, -0.14, -4)
                glVertex3f(0.5, -0.14, -4)
                glVertex3f(0.46, -0.14, -4)
                glVertex3f(-0.58, -0.14, -4)
                glVertex3f(-0.54, -0.14, -4)
                glVertex3f(-0.5, -0.14, -4)
                glVertex3f(-0.46, -0.14, -4)
                glVertex3f(-0.42, -0.14, -4)
                glColor3f(1,1,1)
                glVertex3f(-0.45, 0.05, -4)
                glVertex3f(-0.41, 0.05, -4)
                glVertex3f(-0.37, 0.05, -4)
                glVertex3f(-0.33, 0.05, -4)
                glVertex3f(0.42, -0.14, -4)
            glEnd()
            glPushMatrix()
            glScalef(0.725, 0.725, 0.725)
            glTranslate(0, 0, -4.9)
            glCallList(self.lvl_warn.gl_list)
            glPopMatrix()
            if self.blit:
                glColor3f(1,0.5,0)
                self.DisplayText("CLICK TO TAKE DOWN MISSION", (445, 585), 1)

    def draw(self):
        if self.page==0 or self.page==1:
            glColor3f(1,1,1)
            for star in self.star:
                star[2] -= star[3]
                if -4<star[2]<15:
                    glPointSize(star[4])
                    glBegin(GL_POINTS)
                    glVertex3f(star[0], star[1], star[2])
                    glEnd()
                if star[2]<-18:
                    star[2] = 18

        if self.page==0:
            if self.loadcount==0:
                sound = pygame.mixer.Sound('External/Initialize.wav')
                sound.play()
            glPushMatrix()
            glScalef(0.725, 0.725, 0.725)
            glTranslate(0, 0, -4.9)
            if self.blit:
                if self.loadcount>=1000:
                    glCallList(self.Load.gl_list)
                if self.loadcount<3000:
                    glTranslate(0, 0, 0.1)
                    glCallList(self.word.gl_list)
            glPopMatrix()
            if self.blit and self.loadcount%10==0 and self.loadcount<3000:
                self.blit = False
            else:
                self.blit = True
                if self.loadcount<1000:
                    glColor3f(0, 0, 0)
                    glLineWidth(8)
                    glBegin(GL_LINES)
                    glVertex3f(-1, random.uniform(0, 0.01), -4.8)
                    glVertex3f(1, random.uniform(0, 0.01), -4.8)
                    glVertex3f(-1, -random.uniform(0, 0.01), -4.8)
                    glVertex3f(1, -random.uniform(0, 0.01), -4.8)
                    glEnd()
                self.loadcount += 1
            if self.loadcount==5000:
                self.page = 1
        elif self.page==1:
            glPushMatrix()
            glScalef(0.725, 0.725, 0.725)
            glTranslate(0, 0, -4.9)
            glCallList(self.menuview.gl_list)
            glPopMatrix()
        elif self.page==2:
            glPushMatrix()
            glScalef(0.725, 0.725, 0.725)
            glTranslate(0, 0, -4.9)
            glCallList(self.Control.gl_list)
            glPopMatrix()
        elif self.page==3:
            glPushMatrix()
            glScalef(0.725, 0.725, 0.725)
            glTranslate(0, 0, -4.9)
            glCallList(self.Instruction.gl_list)
            glPopMatrix()
        elif self.page==4:
            glPushMatrix()
            glScalef(0.725,0.725,0.725)
            glTranslate(0,0,-4.9)
            glCallList(self.plyview.gl_list)
            glPopMatrix()
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(0,1,0)
            glVertex3f(0.081, -0.043, -4.9)
            for i in range(1,18):
                x = 0.011 * math.cos(math.radians(self.rot_deg-4*i)) + 0.081
                y = 0.011 * math.sin(math.radians(self.rot_deg-4*i)) - 0.043
                glColor4f(0, 1-(18-i)/18, 0,1-(18-i)/18)
                glVertex3f(x, y, -4.9)
            glEnd()
            glPointSize(5)
            glColor3f(1,140/255,0)
            glBegin(GL_POINTS)
            # glVertex3f(0.081,-0.043,-4.9)       #ply > centre
            if self.box_appr:
                for box in self.box_appr:
                    x = box[0]*math.cos(math.radians(box[1]))+0.081
                    y = box[0] * math.sin(math.radians(box[1]))-0.043
                    glVertex3f(x, y, -4.9)
            glEnd()
            if self.shoot and self.bullet_left>0:
                glPushMatrix()
                glScalef(0.725, 0.725, 0.725)
                glTranslate(0, 0, -4.9)
                glCallList(self.splash.gl_list)
                glPopMatrix()
                self.shoot = False
            if self.powerlist:
                slc = self.powerlist[self.displaypower]
                glPushMatrix()
                glTranslate(-0.1625,-0.085,-4.8)
                if slc == 1:
                    glCallList(self.invisible.gl_list)
                elif slc == 2:
                    glCallList(self.shield.gl_list)
                elif slc ==3:
                    glCallList(self.reloadammo.gl_list)
                elif slc ==4:
                    glCallList(self.heal.gl_list)
                glPopMatrix()
            else:
                glPushMatrix()
                glTranslate(-0.1625, -0.085, -4.8)
                glCallList(self.reloadammoX.gl_list)
                glPopMatrix()
            self.bitText()
            glColor3f(1,0,0)
            glBegin(GL_QUADS)
            a = 0.01725
            if self.health>10:
                if self.health ==100:
                    h = 9
                else:
                    h = int(self.health/10)
            else:
                h = 0
            for i in range(10):
                if i>h:
                    break
                b = a - 0.003
                if i==h:
                    if i!=0:
                        if self.health!=100:
                            b = a - 0.003*(self.health%10/10)
                    else:
                        b = a - 0.003 * (self.health / 10)
                glVertex(a, 0.048, -4.9)
                glVertex(a, 0.0455, -4.9)
                glVertex(b, 0.0455, -4.9)
                glVertex(b, 0.048, -4.9)
                a = b - 0.0005
            glEnd()
        
    def update(self, ply_POS, box_Pos, z_deg):
        self.box_left = box_Pos
        self.box_appr = []
        self.rot_deg +=1.5
        if self.blit:
            self.blit = False
        else:
            self.blit = True
        for box in box_Pos:
            dX = dY = 0
            if box[0] > ply_POS[0]:
                dX = box[0] - ply_POS[0]
            elif box[0] < ply_POS[0]:
                dX = -(ply_POS[0] - box[0])
            if box[1] > ply_POS[1]:
                dY = box[1] - ply_POS[1]
            elif box[1] < ply_POS[1]:
                dY = -(ply_POS[1] - box[1])
            dist = math.sqrt((dX ** 2) + (dY ** 2))
            if dist < 50:
                if dX==0:
                    dX = 1
                deg = math.degrees(math.atan(dY / dX))
                self.box_appr.append((dist/5000, 90-deg+z_deg))

    def updateINFO(self, bullet_left, powerlist, ply_health, time, time_passed, power_apply):
        self.bullet_left = bullet_left
        self.powerlist = powerlist
        self.health = ply_health
        self.time_display = time-time_passed
        self.powerapply = power_apply


    def bitText(self):
        glColor3f(1,0.5,0)
        self.DisplayText("M I S S I O N", (90,690),1)
        self.DisplayText("M I S S I O N", (92, 690), 1)
        self.DisplayText(str(len(self.box_left))+" X", (80, 640), 1)
        self.DisplayText(str(len(self.box_left)) + " X", (82, 640), 1)
        self.DisplayText("L E V E L", (360, 715), 1)
        self.DisplayText("L E V E L", (362, 715), 1)
        self.DisplayText(str(self.lvl), (405, 685), 1)
        self.DisplayText(str(self.lvl), (407, 685), 1)
        self.DisplayText("T I M E", (792, 715), 1)
        self.DisplayText("T I M E", (794, 715), 1)
        self.DisplayText(str(self.time_display), (820, 685), 1)

        if self.bullet_left<=10:
            if self.blit:
                glColor3f(1,0,0)
                self.DisplayText(str(self.bullet_left), (1040, 632), 1)
        else:
            self.DisplayText(str(self.bullet_left), (1040, 632), 1)
        if self.powerapply>0 and self.blit:
            glColor3ub(254, 1, 154)
            if self.powerapply==1:
                self.DisplayText("INVISIBLING", (570, 110), 2)
            elif self.powerapply==2:
                self.DisplayText('SHIELDING', (575, 110), 2)
            elif self.powerapply==3:
                self.DisplayText('RELOADING', (572, 110), 2)
            elif self.powerapply==4:
                self.DisplayText('HEALING', (585, 110), 2)



    def DisplayText(self, text, pos, font):
        glWindowPos2fv(pos)
        if font == 1:
            font = GLUT_BITMAP_TIMES_ROMAN_24
        elif font == 2:
            font = GLUT_BITMAP_HELVETICA_18
        for ch in text:
            glutBitmapCharacter(font, ctypes.c_int(ord(ch)))