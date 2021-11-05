import os
import math
import pygame
from pygame.locals import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Shoot_Player import *
from Shoot_Map import *
from Shoot_Props import *
from Shoot_Interface import *

Ply = Player()
maps = Map()
prop = Props()
itf = Interface()

class Game:

    def __init__(self):
        self.time = 0
        self.lastime = 0
        self.timepassed = 0
        self.lvl = 0  #0
        self.lvl_warn = 0
        self.z_target = 0
        self.pause = False
        self.rot_deg = 0
        self.lvl_complete = False
        self.lvl_fail = False
        self.mute = False
        self.load = False
        self.load_effect = True
        self.warn = [False, 0, False]

    def camera(self, targetUD):
        if targetUD!=0:
            if targetUD==-1:
                if self.z_target>0:
                    self.z_target -= 3
            elif targetUD==1:
                if self.z_target<75:
                    self.z_target += 3
        glLoadIdentity()  # Reset the matrix system
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(Ply.pos[0], Ply.pos[1], Ply.pos[2], Ply.pos[0]+30*math.cos(math.radians(Ply.z_deg)), Ply.pos[1]+30*math.sin(math.radians(Ply.z_deg)), Ply.pos[2]+30*math.tan(math.radians(self.z_target)), 0, 0, 1)

    def cameraUI(self):
        glLoadIdentity()  # Reset the matrix system
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0, 0, -5, 0, 0, 20, 0, 1, 0)

    def GameReset(self):
        self.pause = True
        self.lastime = 0
        Ply.lvl = prop.lvl = maps.lvl = itf.lvl = self.lvl
        maps.mazeUPDATE()
        prop.route = Ply.route = maps.route
        Ply.routeUPDATE()
        prop.gameUPDATE()
        self.z_target = 0
        self.rot_deg = 0
        self.warn[2] = False
        if self.lvl==1:
            Ply.health = 100
            itf.timerecord = [0,0,0]
            itf.score = [0,0,0]
            pygame.mixer.music.load('External\BGM1.wav')
            pygame.mixer.music.play(-1)
        elif self.lvl==2:
            pygame.mixer.music.load('External\BGM2.wav')
            pygame.mixer.music.play(-1)
        elif self.lvl==3:
            pygame.mixer.music.load('External\BGM3.wav')
            pygame.mixer.music.play(-1)
        if self.mute:
            pygame.mixer.music.pause()

    def Levelupdate(self):
        complete = False
        if not self.warn[0]:
            if Ply.health<20 and not self.mute or prop.bullet_count<=10 and not self.mute:
                self.warn[0] = True
                self.warn[1] = self.time + 8
                sound = pygame.mixer.Sound('External/critical.wav')
                sound.play()
        else:
            if self.time>self.warn[1]:
                self.warn[0] = False

        if Ply.health<=0:
            self.lvl_fail = True
            self.pause = True
            itf.timerecord[self.lvl - 1] = self.time - self.timepassed
            if itf.timerecord[self.lvl - 1] == 0:
                itf.timerecord[self.lvl - 1] = 1
            itf.score[self.lvl - 1] += int(60000 / itf.timerecord[self.lvl - 1])
            itf.score[self.lvl - 1] += int(Ply.health / 100 * 500)
        if not prop.box_POS:
            if self.lvl==1:
                if Ply.pos[0]>44 and 2<Ply.pos[1]<10:
                    complete = True
            elif self.lvl==2:
                if Ply.pos[0]>58 and 2<Ply.pos[1]<10:
                    complete = True
            elif self.lvl==3:
                if Ply.pos[0]>70 and -10<Ply.pos[1]<-2:
                    complete = True
            if complete:
                if not self.mute:
                    sound = pygame.mixer.Sound('External/level.wav')
                    sound.play()
                self.lvl_complete = True
                self.pause = True
                itf.timerecord[self.lvl - 1] = self.time - self.timepassed
                if itf.timerecord[self.lvl - 1] == 0:
                    itf.timerecord[self.lvl - 1] = 1
                itf.score[self.lvl - 1] += int(60000 / itf.timerecord[self.lvl - 1])
                itf.score[self.lvl - 1] += int(Ply.health / 100 * 500)

    def Leveldraw(self):
        if not self.warn[2]:
            self.warn[2] = True
            if not self.mute:
                sound = pygame.mixer.Sound('External/warn.wav')
                sound.play()
        if self.lvl_warn<self.lvl:
            self.rot_deg +=1
            if self.lvl==1:
                glPushMatrix()
                glTranslate(-42, -6, 2)
                glRotate(-15,0,1,0)
                glRotate(self.rot_deg, 0,0,1)
                glCallList(prop.DroneA.gl_list)
                glPopMatrix()
            elif self.lvl==2:
                glPushMatrix()
                glTranslate(-55, -6, 2)
                glRotate(-15, 0, 1, 0)
                glRotate(self.rot_deg, 0, 0, 1)
                glCallList(prop.DroneB.gl_list)
                glPopMatrix()
            elif self.lvl==3:
                glPushMatrix()
                glTranslate(-66, -6, 2)
                glRotate(self.rot_deg, 0, 0, 1)
                glCallList(prop.DroneC.gl_list)
                glPopMatrix()

    def play(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.mixer.init()
        glutInit()
        display = (1250, 750)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption('MAZE SURVIVOR by Low Jun Hong BS18110173')
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        glViewport(0, 0, display[0], display[1])
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, (display[0] / display[1]), 0.1, 1000)
        glMatrixMode(GL_MODELVIEW)
        prop.genList()
        itf.genList()
        moveUD = moveLR = targetUD = 0
        pointer = [False, 0]
        while True:
            self.time = int(pygame.time.get_ticks() / 1000)
            cursor = pygame.mouse.get_pos()
            pointer[0] = False
            if moveLR>0:
                moveLR = 0
            if targetUD!=0:
                targetUD = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if self.lvl_warn < self.lvl or self.lvl_complete or self.lvl_fail:
                        break
                    if event.key == pygame.K_ESCAPE:
                        if itf.page==2 or itf.page==3:
                            itf.page = 1
                        elif itf.page==4:
                            if not self.pause:
                                self.pause = True
                                self.lastime = self.time-self.timepassed
                            else:
                                self.lastime = self.timepassed
                                self.pause = False
                    elif event.key == K_SPACE and itf.page==4:
                        if not self.pause:
                            if prop.powerup and prop.powerapply==0:
                                prop.powerapply = prop.powerup[itf.displaypower]
                                prop.powerup.pop(itf.displaypower)
                                if not self.mute:
                                    sound = pygame.mixer.Sound('External/powerup.wav')
                                    sound.play()
                                if prop.powerapply==1:
                                    prop.powertime = self.time + 10  # 10 secs invisible
                                elif prop.powerapply==3 or prop.powerapply==4:
                                    prop.powertime = self.time+5
                                elif prop.powerapply==2:
                                    prop.shield = 20
                                if itf.displaypower>0:
                                    itf.displaypower -= 1
                            elif not prop.powerup and prop.powerapply==0 and Ply.health>0:
                                Ply.health -= 10
                                prop.bullet_count += 100
                        else:
                            if not self.lvl_complete and not self.lvl_fail and not self.lvl_warn < self.lvl:
                                itf.page = 1
                                self.pause = False
                    elif event.key==K_m:
                        if self.mute:
                            self.mute = False
                            pygame.mixer.music.unpause()
                        else:
                            self.mute = True
                            pygame.mixer.music.pause()
                elif event.type == pygame.KEYUP:
                    if event.key==K_w or event.key==K_s:
                        moveUD = 0
                elif event.type == MOUSEBUTTONDOWN:
                    if self.lvl_warn<self.lvl and self.pause:
                        self.lvl_warn = self.lvl
                        self.pause = False
                    elif self.lvl_complete:
                        self.lvl += 1
                        self.lvl_complete = False
                        if self.lvl<4:
                            self.GameReset()
                        if self.lvl==4:
                            itf.page = 1
                            self.pause = False
                    elif self.lvl_fail:
                        self.lvl_fail = False
                        itf.page = 1
                        self.pause = False
                    elif event.button == 1:
                        if itf.page==1:
                            if 514<cursor[0]<735:
                                if 290<cursor[1]<354:
                                    itf.page = 4
                                    self.lvl = 1
                                    self.lvl_warn = 0
                                    self.GameReset()
                                elif 387<cursor[1]<449:
                                    itf.page = 2
                                elif 487<cursor[1]<547:
                                    itf.page = 3
                                elif 582<cursor[1]<644:
                                    # add confirmation to exit
                                    pygame.quit()
                                    quit()
                        elif itf.page==4:
                            if not self.pause:
                                prop.shoot = True
                                itf.shoot = True
                                if prop.powerapply==1 or prop.powerapply==3:
                                    if not self.mute:
                                        sound = pygame.mixer.Sound('External/deny.wav')
                                        sound.play()
                                    prop.powerapply = 0
                    elif event.button == 3:
                        if prop.powerup:
                            itf.displaypower += 1
                            if itf.displaypower>=len(prop.powerup):
                                itf.displaypower = 0
                elif event.type == MOUSEMOTION and itf.page==4 and not self.pause:
                    i,j = event.rel
                    pointer = [True,i]
                    if i<0:
                        moveLR = 1
                    elif i>0:
                        moveLR = 2
                    if j>0:
                        targetUD = -1
                    elif j<0:
                        targetUD = 1
                keys = pygame.key.get_pressed()  # press hold
                if itf.page==4 and not self.pause:
                    if keys[K_w]:
                        moveUD = 1
                    elif keys[K_s]:
                        moveUD = 2
            if itf.page == 4 and not self.pause:
                if moveLR==0:
                    if cursor[0]==0:
                        moveLR = 1
                    elif cursor[0] >= display[0]*.99 or not pointer[0] and pointer[1]>12:
                        moveLR = 2
                if targetUD ==0:
                    if cursor[1]==0:
                        targetUD = 1
                    elif cursor[1]>=display[1]*.99:
                        targetUD = -1
                if prop.bar:
                    moveUD = 0
                    if Ply.pos[2]<3.2:
                        if prop.DronePOSX[6] <= 0:
                            Ply.pos[2] += 0.01
                    else:
                        prop.bar = False
                        prop.Drone_track = -1
                        Ply.routeUPDATE()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glClearColor(0,0,0,1)
            glClearDepthf(1)
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LEQUAL)
            if self.pause:
                self.timepassed = self.time - self.lastime
            if itf.page==0:
                if not self.load:
                    pygame.mixer.music.load('External\BGM0.wav')
                    pygame.mixer.music.play(-1)
                    self.load = True
                if not self.load_effect:
                    itf.page = 1
            if itf.page==1:
                pygame.mouse.set_visible(True)
            elif itf.page==2 or itf.page==3:
                pygame.mouse.set_visible(False)
            elif itf.page==4:
                pygame.mouse.set_visible(False)
                if not self.pause:
                    self.Levelupdate()
                    Ply.moveUPDATE(moveUD, moveLR)
                    prop.bulletInit(Ply.pos, Ply.z_deg, self.z_target)
                    Ply.health, itf.score[self.lvl - 1] = prop.update(Ply.pos, Ply.health, self.time, itf.score[self.lvl - 1])
                    prop.mute = self.mute

                itf.update(Ply.pos, prop.box_POS, Ply.z_deg)
                itf.updateINFO(prop.bullet_count, prop.powerup, Ply.health, self.time, self.timepassed, prop.powerapply)
                self.camera(targetUD)
                maps.draw()
                prop.draw(Ply.pos)
                self.Leveldraw()
            self.cameraUI()
            if itf.page==4:
                itf.draw_lvl(self.lvl_warn, self.lvl_complete, self.lvl_fail)
            itf.draw()
            pygame.display.flip()

        pass

if __name__ == "__main__":
    game = Game()
    game.play()
    del itf
    del prop
    del Ply
    del maps