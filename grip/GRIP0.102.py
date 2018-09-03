#-------------------------------------------------------------------------------
# Name:        Grip
# Purpose:
#
# Author:      Stuart Laxton
#
# Created:     01/06/2012
# Copyright:   (c) Stuart Laxton 2012
# Licence:
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from __future__ import division
import pygame, sys, time, random, math
from pygame.locals import *


# set up pygame
pygame.init()
mainClock = pygame.time.Clock()
pygame.joystick.init()

# set up the window
WINDOWWIDTH = 1000
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),0,32)
pygame.display.set_caption('GRIP')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255,255,255)
BGREEN = (0, 200, 0)
GREEN = (0, 160, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LBLUE = (0, 200, 255)
LGREY = (75,75,75)
BROWN = (139,69,19)
DGREY = (25,25,25)

# set up variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
MOVESPEED = 50
bikeSelect = [1,[18,0,12,20,2,60,2,120],[19,0,10,20,2,60,2,90],[20,0,8,20,2,60,2,75],[21,0,6,20,2,60,2,60]]# 0-Index, 1-Bike 1, 2-Bike 2, 3-Bike 3
bikeSettings = [16,0,12,20,2,60,2,120]# 0-Max Speed, 1-Current Count, 2-Acceleration rate, 3-Braking Rate, 4-Free Wheel, 5-Gear Change,6-Turn Speed,7-Max Boost
movespeed = [0,0,2,0]#0-Current movespeed, 1-Max movespeed, 2-Rotation speed, 3-Turn Speed Multiply
kers = [False,5,0,0,6]#0-On / Off, 1-KERS boost, 2-KERS time left, 3-KERS skid count, 4-Skid switcher
position = [650,250,0,0,0,0]# 0-1 Track position, 2-3 Background position, 4-5 Previous position
rotRect = (100,50)
degree = 0# Player rotation angle
radians = 0
moveRadians = 0
gdegree = 0#Ghost rotation angle
timer = [0,0,10000,0,0,0,0,False,'10 Laps Remaining']# 0-Current Lap ,1-Last Lap ,2-Best lap ,3-Section 1 ,4-Section 2 ,5-Section 3,6-Time Dif, 7-Timer running, 8-Laps Remaining text
drawTrack = [1,'laps1.txt','laps2.txt','laps3.txt','laps4.txt','laps5.txt','laps6.txt','laps7.txt','laps8.txt','laps9.txt']#0-Track selector, 1-4 LapRecord file names
cheatCheck = [0,False,False,False,0,30,'         ',WHITE]# 0-Cheat Check ,1-Finish Line Check ,2-Section 1 Check ,3-Section 2 Check, 4-Grass Counter, 5-Grass Limit, 6-Time Dif Output, 7-Lap Text Colour
fps = [0,60,10,60,0]# 0-On/Off, 1-Set Point, 2-Actual FPS, 3-Lowest Recorded, 4-Highest Recorded
playerSettings = [WINDOWWIDTH/2-50,WINDOWHEIGHT/2,0,0]# 0-Player Horizontal, 1-Player Vertical, 2-Rotation position (x5 for degrees)
detail = [3,0,0] # LOD switch (0-3)
lap = [0,0,0,0,0,0,WHITE,WHITE,WHITE,WHITE]#0-Lap Time, 1-Sector 1, 2-Sector 2, 3-Sector 3, 4-Bike No, 5-Valid/Invalid, 6-Lap Time Colour, 7-Sector 1 Colour, 8-Sector 2 colour, 9-Sector 3 colour
lapTimes = [0]#0-Lap No ,1-10 - Lap f
displayTimeDif = 0 # Time difference display counter
newLapRecord = [False,WHITE,'Your quickest time did not rank in the top 5',6]
originalLapRecord = 0
curser = [40, 190, 50, 50]# Start position for the curser on the menu
option = [0,'Choose Bike','Start Time Trial','Settings','Instructions','Quit',0,'',0]# menu options
settings = [0,'Detail Level','Show FPS','Screen Size','Full Screen Mode','Sound On','Exit',False]# Settings page options
banner =[50,18]# Start point for banner text animation
show = [0,1,True,True]# 0-Window / Fullscreen, 1-Display Resolution, 2-Gradient Sky, 3-Background
width = [600,1000,1000,1200,1200,1200]# Screen widths
height = [600,600,768,720,800,1000]# Screen heights
ghostCounter = [False,0,0,0,0,0]# 0-Running, 1-Ghost Horizontal pos, 2-Ghost Vertical pos, 3-ghost image, 4-Ghost degree, 5-Ghost position count
ghostPosition = [0,0,0,0]
ghostLap = []
ghostLapRecord = []
gameOver = False
bikeImage = pygame.image.load('graphics/bike1.png').convert_alpha()
limit = [1,-1950+WINDOWWIDTH,-1450+WINDOWHEIGHT,1750,1350,0,-5]
skiding = [False,0] # Skiding, Counter
skids = []
skidPosition = []
oldFrontPosition = [0,0]
oldRearPosition = [0,0]
dirty = []
dirtPosition = 0
frontWheel = [0,0]
rearWheel = [0,0]
boost = []
sound = True

gripImage = pygame.image.load('graphics/grip.png').convert_alpha()
overheadImage = pygame.image.load('graphics/overhead_tile.png').convert_alpha()
trackImage11 = pygame.image.load('graphics/b-1-1.png').convert_alpha()
trackImage21 = pygame.image.load('graphics/b-2-1.png').convert_alpha()
trackImage31 = pygame.image.load('graphics/b-3-1.png').convert_alpha()
trackImage41 = pygame.image.load('graphics/b-4-1.png').convert_alpha()
trackImage5 = pygame.image.load('graphics/st-v-3.png').convert_alpha()
trackImage51 = pygame.image.load('graphics/st-v-3-k1.png').convert_alpha()
trackImage52 = pygame.image.load('graphics/st-v-3-k2.png').convert_alpha()
trackImage53 = pygame.image.load('graphics/st-v-3-k3.png').convert_alpha()
trackImage54 = pygame.image.load('graphics/st-v-3-k4.png').convert_alpha()
trackImage6 = pygame.image.load('graphics/st-h-3.png').convert_alpha()
trackImage61 = pygame.image.load('graphics/st-h-3-k1.png').convert_alpha()
trackImage62 = pygame.image.load('graphics/st-h-3-k2.png').convert_alpha()
trackImage63 = pygame.image.load('graphics/st-h-3-k3.png').convert_alpha()
trackImage64 = pygame.image.load('graphics/st-h-3-k4.png').convert_alpha()
trackImage12 = pygame.image.load('graphics/b-1-2.png').convert_alpha()
trackImage22 = pygame.image.load('graphics/b-2-2.png').convert_alpha()
trackImage32 = pygame.image.load('graphics/b-3-2.png').convert_alpha()
trackImage42 = pygame.image.load('graphics/b-4-2.png').convert_alpha()
trackImage13 = pygame.image.load('graphics/b-1-3.png').convert_alpha()
trackImage23 = pygame.image.load('graphics/b-2-3.png').convert_alpha()
trackImage33 = pygame.image.load('graphics/b-3-3.png').convert_alpha()
trackImage43 = pygame.image.load('graphics/b-4-3.png').convert_alpha()
trackImage14 = pygame.image.load('graphics/b-1-4.png').convert_alpha()
trackImage24 = pygame.image.load('graphics/b-2-4.png').convert_alpha()
trackImage34 = pygame.image.load('graphics/b-3-4.png').convert_alpha()
trackImage44 = pygame.image.load('graphics/b-4-4.png').convert_alpha()

scenaryImage1 = pygame.image.load('graphics/tree.png').convert_alpha()

menuImage1 = pygame.image.load('graphics/back.png').convert_alpha()

# set up the sounds
rev1Sound = pygame.mixer.Sound('sound/rev1.wav')
rev2Sound = pygame.mixer.Sound('sound/rev2.wav')
rev3Sound = pygame.mixer.Sound('sound/rev3.wav')
rev4Sound = pygame.mixer.Sound('sound/rev4.wav')
rev5Sound = pygame.mixer.Sound('sound/rev5.wav')
rev6Sound = pygame.mixer.Sound('sound/rev6.wav')
freewheel1Sound = pygame.mixer.Sound('sound/freewheel1.wav')
freewheel2Sound = pygame.mixer.Sound('sound/freewheel2.wav')
freewheel3Sound = pygame.mixer.Sound('sound/freewheel3.wav')
freewheel4Sound = pygame.mixer.Sound('sound/freewheel4.wav')
freewheel5Sound = pygame.mixer.Sound('sound/freewheel5.wav')
freewheel6Sound = pygame.mixer.Sound('sound/freewheel6.wav')
slideSound = pygame.mixer.Sound('sound/slide2.wav')
wheelspinSound = pygame.mixer.Sound('sound/wheelspin2.wav')
bikestartSound = pygame.mixer.Sound('sound/bikestart.wav')
tickoverSound = pygame.mixer.Sound('sound/tickover.wav')
revSound = [1,rev1Sound,rev2Sound,rev3Sound,rev4Sound,rev5Sound,rev6Sound]
freewheelSound = [1,freewheel1Sound,freewheel2Sound,freewheel3Sound,freewheel4Sound,freewheel5Sound,freewheel6Sound]
accelerating = [False,False]
changeSound = 1
revChannel = pygame.mixer.Channel(1)
soundTimer = [50,0]

# set up the fonts
smallFont = pygame.font.SysFont('arial', 20)
basicFont = pygame.font.SysFont('arial', 24)
normalFont = pygame.font.SysFont('arial', 30)
guessFont = pygame.font.SysFont('arial', 36)

def setDisplay(w,h):
    playerSettings[0] = WINDOWWIDTH/2-50
    playerSettings[1] = WINDOWHEIGHT/2
    windowSurface = pygame.display.set_mode((w, h),show[0],32)
    pygame.display.set_caption('GRIP')

def framerate():
    mainClock.tick(fps[1])
    fps[2]=int(mainClock.get_fps())
    if fps[0]==1:
        text = smallFont.render('Set FPS - ' + str(fps[1]), True, WHITE,)
        windowSurface.blit(text, (10,WINDOWHEIGHT-60))
        text1 = smallFont.render('Current FPS - ' + str(fps[2]), True, WHITE,)
        windowSurface.blit(text1, (10,WINDOWHEIGHT-40))
        text2 = smallFont.render('Lowest FPS - ' + str(fps[3]), True, WHITE,)
        windowSurface.blit(text2, (10,WINDOWHEIGHT-20))
        if fps[2]<fps[3]:
            fps[3]=fps[2]
        if fps[2]>fps[4]:
            fps[4]=fps[2]

def loadRecords(drawTrack):
    lapTimeFile = open(drawTrack[drawTrack[0]],'r+')
    lapRecord = lapTimeFile.readline().split()
    lapRecord2 = lapTimeFile.readline().split()
    lapRecord3 = lapTimeFile.readline().split()
    lapRecord4 = lapTimeFile.readline().split()
    lapRecord5 = lapTimeFile.readline().split()
    lapTimeFile.close()
    return lapRecord, lapRecord2, lapRecord3, lapRecord4, lapRecord5

# Opening menu
def menu():
    # run the menu loop
    moveUp = False
    moveDown = False
    moveLeft = False
    moveRight = False
    global lapRecord
    global lapRecord2
    global lapRecord3
    global lapRecord4
    global lapRecord5
    global position
    global timer
    global lapTimes
    global cheatCheck
    global lap
    global originalLapRecord
    global newLapRecord
    global limit
    global bikeImage
    global playerImage
    global menuImage1
    global skids
    global dirty
    global boost
    while option[6]==0:# Option [6] is the selection output bit
        # check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.JOYBUTTONDOWN:
                for i in range( buttons ):
                    button = joystick.get_button( i )
                for i in range( axes ):
                    axis = joystick.get_axis( i )
            if event.type == KEYDOWN:
                    # change the keyboard variables
                    if event.key == K_UP or event.key == ord('w'):#Curser Up
                        moveDown = False
                        moveUp = True
                    if event.key == K_DOWN or event.key == ord('s'):#Curser Down
                        moveUp = False
                        moveDown = True
                    if event.key == K_9:#Show FPS
                        if fps[0] == 1:
                            fps[0] = 0
                        else:
                            fps[0] = 1
                    if event.key == K_EQUALS:#Increase max FPS
                        show[1] += 5
                    if event.key == K_MINUS:#Decrease max FPS
                        show[1] -= 5
                    if event.key == K_RETURN or event.key == K_SPACE:#Select current option
                        if curser[1]==240:#Start game
                            position = [(WINDOWWIDTH/2)+50,(WINDOWHEIGHT/2)-50,0,0,0,0]
                            playerImage, bikeImage = playerGraphics(bikeSelect[0])
                            skids = []
                            dirty = []
                            boost = []
                            fps[3] = 60
                            playerSettings[2]=0
                            timer = [0,0,10000,0,0,0,0,False,'10 Laps Remaining']
                            cheatCheck = [0,False,False,False,0,25,'         ',RED]
                            lap = [0,0,0,0,0,0,WHITE,WHITE,WHITE,WHITE]
                            lapTimes = [0]
                            originalLapRecord = int(lapRecord[0])
                            newLapRecord = [False,WHITE,'Your quickest time did not rank in the top 5',6]
                            if sound:
                                revChannel.play(bikestartSound)
                            option[6]=2

                        if curser[1]==290:#Go to settings page
                            settings[7]=True
                            settingsScreen()
                        if curser[1]==340:#Go to instructions page
                            option[8]=600
                            about()
                        if curser[1]==390:#Quit game
                            pygame.quit()
                            sys.exit()
                    if event.key == K_RIGHT:#Change bike selected
                        if curser[1]==190:
                            bikeSelect[0] +=1
                            if bikeSelect[0] >4:
                                bikeSelect[0] = 1
                            playerImage, bikeImage = playerGraphics(bikeSelect[0])
                        if curser[1]==240:#Change track selected
                            drawTrack[0] +=1
                            if drawTrack[0] >9:
                                drawTrack[0] = 1
                            lapRecord, lapRecord2, lapRecord3, lapRecord4, lapRecord5 = loadRecords(drawTrack)
                            position,limit = scrollLimits(drawTrack)
                    if event.key == K_LEFT:#Change bike selected
                        if curser[1]==190:
                            bikeSelect[0] -=1
                            if bikeSelect[0] <1:
                                bikeSelect[0] = 4
                            playerImage, bikeImage = playerGraphics(bikeSelect[0])
                        if curser[1]==240:#Change track selected
                            drawTrack[0] -=1
                            if drawTrack[0] <1:
                                drawTrack[0] = 9
                            lapRecord, lapRecord2, lapRecord3, lapRecord4, lapRecord5 = loadRecords(drawTrack)
                            position,limit = scrollLimits(drawTrack)
            if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_UP or event.key == ord('w'):
                        moveUp = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        moveDown = False

        # move the Curser
        if moveDown and curser[1] < 350:
            curser[1] += MOVESPEED
            moveDown = False
        if moveUp and curser[1] > 200:
            curser[1] -= MOVESPEED
            moveUp = False

        # draw the background onto the surface & draw the banner
        drawBack()
        moveTrack()
        moveScenary()
        drawBanner(gripImage)

        # Output the current curser position
        if curser[1]==190:
            curser[2]=265
            option[7]='Press Left / Right to select your motorbike'
        if curser[1]==240:
            curser[2]=320
            option[7]='Left / Right to select Track - Enter Start'
        if curser[1]==290:
            curser[2]=130
            option[7]='Adjust settings'
        if curser[1]==340:
            curser[2]=175
            option[7]='How to play GRIP'
        if curser[1]==390:
            curser[2]=75
            option[7]='Quit Game'

        # draw the curser onto the surface
        pygame.draw.rect(windowSurface, BLACK, (curser[0],curser[1],curser[2],curser[3]),1)

        # draw the options onto the surface
        text1s = guessFont.render(option[1] + ' - Bike ' + str(bikeSelect[0]), True, BLACK,)
        text1 = guessFont.render(option[1] + ' - Bike ' + str(bikeSelect[0]), True, WHITE,)
        text2s = guessFont.render(option[2]+ ' - Track ' + str(drawTrack[0]), True, BLACK,)
        text2 = guessFont.render(option[2]+ ' - Track ' + str(drawTrack[0]), True, WHITE,)
        text3s = guessFont.render(option[3], True, BLACK,)
        text3 = guessFont.render(option[3], True, WHITE,)
        text4s = guessFont.render(option[4], True, BLACK,)
        text4 = guessFont.render(option[4], True, WHITE,)
        text5s = guessFont.render(option[5], True, BLACK,)
        text5 = guessFont.render(option[5], True, WHITE,)
        text6s = basicFont.render(option[7], True, BLACK,)
        text6 = basicFont.render(option[7], True, WHITE,)
        windowSurface.blit(text1s, (50,200))
        windowSurface.blit(text1, (52,202))
        windowSurface.blit(text2s, (50,250))
        windowSurface.blit(text2, (52,252))
        windowSurface.blit(text3s, (50,300))
        windowSurface.blit(text3, (52,302))
        windowSurface.blit(text4s, (50,350))
        windowSurface.blit(text4, (52,352))
        windowSurface.blit(text5s, (50,400))
        windowSurface.blit(text5, (51,402))
        windowSurface.blit(text6s, (50,450))
        windowSurface.blit(text6, (51,451))

        # blit the track info onto the screen
        head1 = basicFont.render('Laptime', True, WHITE,)
        head2 = basicFont.render('Sector 1', True, WHITE,)
        head3 = basicFont.render('Sector 2', True, WHITE,)
        head4 = basicFont.render('Sector 3', True, WHITE,)
        head5 = basicFont.render('Bike', True, WHITE,)
        head6 = basicFont.render('1st', True, WHITE,)
        head7 = basicFont.render('2nd', True, WHITE,)
        head8 = basicFont.render('3rd', True, WHITE,)
        head9 = basicFont.render('4th', True, WHITE,)
        head10 = basicFont.render('5th', True, WHITE,)
        record11 = basicFont.render("%.2f" %(int(lapRecord[0])/60), True, WHITE,)
        record12 = basicFont.render("%.2f" %(int(lapRecord[1])/60), True, WHITE,)
        record13 = basicFont.render("%.2f" %(int(lapRecord[2])/60), True, WHITE,)
        record14 = basicFont.render("%.2f" %(int(lapRecord[3])/60), True, WHITE,)
        record15 = basicFont.render(str(lapRecord[4]), True, WHITE,)
        record21 = basicFont.render("%.2f" %(int(lapRecord2[0])/60), True, WHITE,)
        record22 = basicFont.render("%.2f" %(int(lapRecord2[1])/60), True, WHITE,)
        record23 = basicFont.render("%.2f" %(int(lapRecord2[2])/60), True, WHITE,)
        record24 = basicFont.render("%.2f" %(int(lapRecord2[3])/60), True, WHITE,)
        record25 = basicFont.render(str(lapRecord2[4]), True, WHITE,)
        record31 = basicFont.render("%.2f" %(int(lapRecord3[0])/60), True, WHITE,)
        record32 = basicFont.render("%.2f" %(int(lapRecord3[1])/60), True, WHITE,)
        record33 = basicFont.render("%.2f" %(int(lapRecord3[2])/60), True, WHITE,)
        record34 = basicFont.render("%.2f" %(int(lapRecord3[3])/60), True, WHITE,)
        record35 = basicFont.render(str(lapRecord3[4]), True, WHITE,)
        record41 = basicFont.render("%.2f" %(int(lapRecord4[0])/60), True, WHITE,)
        record42 = basicFont.render("%.2f" %(int(lapRecord4[1])/60), True, WHITE,)
        record43 = basicFont.render("%.2f" %(int(lapRecord4[2])/60), True, WHITE,)
        record44 = basicFont.render("%.2f" %(int(lapRecord4[3])/60), True, WHITE,)
        record45 = basicFont.render(str(lapRecord4[4]), True, WHITE,)
        record51 = basicFont.render("%.2f" %(int(lapRecord5[0])/60), True, WHITE,)
        record52 = basicFont.render("%.2f" %(int(lapRecord5[1])/60), True, WHITE,)
        record53 = basicFont.render("%.2f" %(int(lapRecord5[2])/60), True, WHITE,)
        record54 = basicFont.render("%.2f" %(int(lapRecord5[3])/60), True, WHITE,)
        record55 = basicFont.render(str(lapRecord5[4]), True, WHITE,)

        windowSurface.blit(previewImage[drawTrack[0]], (400,350))
        windowSurface.blit(menuImage1, (392,247))

        windowSurface.blit(head1, (440,250))
        windowSurface.blit(head2, (520,250))
        windowSurface.blit(head3, (600,250))
        windowSurface.blit(head4, (680,250))
        windowSurface.blit(head5, (760,250))
        windowSurface.blit(head6, (400,270))
        windowSurface.blit(head7, (400,285))
        windowSurface.blit(head8, (400,300))
        windowSurface.blit(head9, (400,315))
        windowSurface.blit(head10, (400,330))
        windowSurface.blit(record11, (455,270))
        windowSurface.blit(record12, (535,270))
        windowSurface.blit(record13, (615,270))
        windowSurface.blit(record14, (695,270))
        windowSurface.blit(record15, (770,270))
        windowSurface.blit(record21, (455,285))
        windowSurface.blit(record22, (535,285))
        windowSurface.blit(record23, (615,285))
        windowSurface.blit(record24, (695,285))
        windowSurface.blit(record25, (770,285))
        windowSurface.blit(record31, (455,300))
        windowSurface.blit(record32, (535,300))
        windowSurface.blit(record33, (615,300))
        windowSurface.blit(record34, (695,300))
        windowSurface.blit(record35, (770,300))
        windowSurface.blit(record41, (455,315))
        windowSurface.blit(record42, (535,315))
        windowSurface.blit(record43, (615,315))
        windowSurface.blit(record44, (695,315))
        windowSurface.blit(record45, (770,315))
        windowSurface.blit(record51, (455,330))
        windowSurface.blit(record52, (535,330))
        windowSurface.blit(record53, (615,330))
        windowSurface.blit(record54, (695,330))
        windowSurface.blit(record55, (770,330))


        windowSurface.blit(bikeImage, (400,120))

        bikeStats(bikeSelect)
        backgroundAnim()
        framerate()
        # draw the window onto the screen
        pygame.display.update()

def scrollLimits(drawTrack):
    global WINDOWWIDTH
    global WINDOWHEIGHT
    position = [(WINDOWWIDTH/2)+50,(WINDOWHEIGHT/2)-50,0,0,0,0]
    if drawTrack[0] == 1:
        limit = [1,-1950+WINDOWWIDTH,-1450+WINDOWHEIGHT,1750,1350,0,-5]
    elif drawTrack[0] == 2:
        limit = [1,-1300+WINDOWWIDTH,-1450+WINDOWHEIGHT,1850,1350,0,-5]
    elif drawTrack[0] == 3:
        limit = [1,-1750+WINDOWWIDTH,-1950+WINDOWHEIGHT,1350,150,0,-5]
    elif drawTrack[0] == 4:
        limit = [1,-3350+WINDOWWIDTH,-2350+WINDOWHEIGHT,750,150,0,-5]
    elif drawTrack[0] == 5:
        limit = [1,-1950+WINDOWWIDTH,-2350+WINDOWHEIGHT,1350,150,0,-5]
    elif drawTrack[0] == 6:
        limit = [1,-1500+WINDOWWIDTH,-2850+WINDOWHEIGHT,1850,150,0,-5]
    elif drawTrack[0] == 7:
        limit = [1,-2250+WINDOWWIDTH,-1550+WINDOWHEIGHT,1550,1450,0,-5]
    elif drawTrack[0] == 8:
        limit = [1,-4150+WINDOWWIDTH,-2150+WINDOWHEIGHT,1250,900,0,-5]
    else:
        limit = [1,-1800+WINDOWWIDTH,-3150+WINDOWHEIGHT,1250,600,0,-5]
    return position, limit


def drawBanner(gripImage):
    windowSurface.blit(gripImage, (banner[0],banner[1]))

def backgroundAnim():
        if banner[0]<=WINDOWWIDTH:# Animate the banner text and background
            banner[0]+=1
        if banner[0]>WINDOWWIDTH:
            banner[0]=-340

        position[limit[5]] = int(position[limit[5]])

        if position[limit[5]] == limit[limit[0]]:
            limit[0] += 1
            if limit[0] > 4:
                limit[0]=1
            if limit[5] == 1:
                limit[5]=0
            else:
                limit[5]=1
            if limit[0] == 1:
                limit[6]=-5
            elif limit[0] == 2:
                limit[6]=-5
            elif limit[0] == 3:
                limit[6]=5
            else:
                limit[6]=5
        else:
            position[limit[5]] += limit[6]
            position[limit[5]+2] += limit[6]


def playerGraphics(bikeSelect):
    if bikeSelect == 1:
        playerImage1 = pygame.image.load('graphics/bike1-1.png').convert_alpha()
        playerImage2 = pygame.image.load('graphics/bike1-2.png').convert_alpha()
        playerImage3 = pygame.image.load('graphics/bike1-3.png').convert_alpha()
        playerImage4 = pygame.image.load('graphics/bike1-4.png').convert_alpha()
        playerImage5 = pygame.image.load('graphics/bike1-5.png').convert_alpha()
        playerImage6 = pygame.image.load('graphics/bike1-6.png').convert_alpha()
        playerImage7 = pygame.image.load('graphics/bike1-7.png').convert_alpha()
        playerImage8 = pygame.image.load('graphics/bike1-8.png').convert_alpha()
        playerImage9 = pygame.image.load('graphics/bike1-9.png').convert_alpha()
        bikeImage = pygame.image.load('graphics/bike1.png').convert_alpha()
    elif bikeSelect == 2:
        playerImage1 = pygame.image.load('graphics/bike2-1.png').convert_alpha()
        playerImage2 = pygame.image.load('graphics/bike2-2.png').convert_alpha()
        playerImage3 = pygame.image.load('graphics/bike2-3.png').convert_alpha()
        playerImage4 = pygame.image.load('graphics/bike2-4.png').convert_alpha()
        playerImage5 = pygame.image.load('graphics/bike2-5.png').convert_alpha()
        playerImage6 = pygame.image.load('graphics/bike2-6.png').convert_alpha()
        playerImage7 = pygame.image.load('graphics/bike2-7.png').convert_alpha()
        playerImage8 = pygame.image.load('graphics/bike2-8.png').convert_alpha()
        playerImage9 = pygame.image.load('graphics/bike2-9.png').convert_alpha()
        bikeImage = pygame.image.load('graphics/bike2.png').convert_alpha()
    elif bikeSelect == 3:
        playerImage1 = pygame.image.load('graphics/bike3-1.png').convert_alpha()
        playerImage2 = pygame.image.load('graphics/bike3-2.png').convert_alpha()
        playerImage3 = pygame.image.load('graphics/bike3-3.png').convert_alpha()
        playerImage4 = pygame.image.load('graphics/bike3-4.png').convert_alpha()
        playerImage5 = pygame.image.load('graphics/bike3-5.png').convert_alpha()
        playerImage6 = pygame.image.load('graphics/bike3-6.png').convert_alpha()
        playerImage7 = pygame.image.load('graphics/bike3-7.png').convert_alpha()
        playerImage8 = pygame.image.load('graphics/bike3-8.png').convert_alpha()
        playerImage9 = pygame.image.load('graphics/bike3-9.png').convert_alpha()
        bikeImage = pygame.image.load('graphics/bike3.png').convert_alpha()
    else:
        playerImage1 = pygame.image.load('graphics/bike4-1.png').convert_alpha()
        playerImage2 = pygame.image.load('graphics/bike4-2.png').convert_alpha()
        playerImage3 = pygame.image.load('graphics/bike4-3.png').convert_alpha()
        playerImage4 = pygame.image.load('graphics/bike4-4.png').convert_alpha()
        playerImage5 = pygame.image.load('graphics/bike4-5.png').convert_alpha()
        playerImage6 = pygame.image.load('graphics/bike4-6.png').convert_alpha()
        playerImage7 = pygame.image.load('graphics/bike4-7.png').convert_alpha()
        playerImage8 = pygame.image.load('graphics/bike4-8.png').convert_alpha()
        playerImage9 = pygame.image.load('graphics/bike4-9.png').convert_alpha()
        bikeImage = pygame.image.load('graphics/bike4.png').convert_alpha()
    playerImage = [5,playerImage1,playerImage2,playerImage3,playerImage4,playerImage5,playerImage6,playerImage7,playerImage8,playerImage9]
    return playerImage, bikeImage

def shadowGraphics():
    shadowImage1 = pygame.image.load('graphics/shadow1.png').convert_alpha()
    shadowImage2 = pygame.image.load('graphics/shadow2.png').convert_alpha()
    shadowImage3 = pygame.image.load('graphics/shadow3.png').convert_alpha()
    shadowImage4 = pygame.image.load('graphics/shadow4.png').convert_alpha()
    shadowImage5 = pygame.image.load('graphics/shadow5.png').convert_alpha()
    shadowImage6 = pygame.image.load('graphics/shadow6.png').convert_alpha()
    shadowImage7 = pygame.image.load('graphics/shadow7.png').convert_alpha()
    shadowImage8 = pygame.image.load('graphics/shadow8.png').convert_alpha()
    shadowImage9 = pygame.image.load('graphics/shadow9.png').convert_alpha()
    shadowImage = [5,shadowImage1,shadowImage2,shadowImage3,shadowImage4,shadowImage5,shadowImage6,shadowImage7,shadowImage8,shadowImage9]
    return shadowImage

def ghostGraphics():
    ghostImage1 = pygame.image.load('graphics/ghost1.png').convert_alpha()
    ghostImage2 = pygame.image.load('graphics/ghost2.png').convert_alpha()
    ghostImage3 = pygame.image.load('graphics/ghost3.png').convert_alpha()
    ghostImage4 = pygame.image.load('graphics/ghost4.png').convert_alpha()
    ghostImage5 = pygame.image.load('graphics/ghost5.png').convert_alpha()
    ghostImage6 = pygame.image.load('graphics/ghost6.png').convert_alpha()
    ghostImage7 = pygame.image.load('graphics/ghost7.png').convert_alpha()
    ghostImage8 = pygame.image.load('graphics/ghost8.png').convert_alpha()
    ghostImage9 = pygame.image.load('graphics/ghost9.png').convert_alpha()
    ghostImage = [5,ghostImage1,ghostImage2,ghostImage3,ghostImage4,ghostImage5,ghostImage6,ghostImage7,ghostImage8,ghostImage9]
    return ghostImage

def previewImage():
    previewImage1 = pygame.image.load('graphics/track1.png').convert_alpha()
    previewImage2 = pygame.image.load('graphics/track2.png').convert_alpha()
    previewImage3 = pygame.image.load('graphics/track3.png').convert_alpha()
    previewImage4 = pygame.image.load('graphics/track4.png').convert_alpha()
    previewImage5 = pygame.image.load('graphics/track5.png').convert_alpha()
    previewImage6 = pygame.image.load('graphics/track6.png').convert_alpha()
    previewImage7 = pygame.image.load('graphics/track7.png').convert_alpha()
    previewImage8 = pygame.image.load('graphics/track8.png').convert_alpha()
    previewImage9 = pygame.image.load('graphics/track9.png').convert_alpha()
    previewImage = [1,previewImage1,previewImage2,previewImage3,previewImage4,previewImage5,previewImage6,previewImage7,previewImage8,previewImage9]
    return previewImage

def bikeStats(bikeSelect):
    pygame.draw.rect(windowSurface, BLACK,(600,240, 45,-62),1)
    pygame.draw.rect(windowSurface, BLACK,(650,240, 45,-62),1)
    pygame.draw.rect(windowSurface, BLACK,(700,240, 45,-62),1)
    pygame.draw.rect(windowSurface, BLACK,(750,240, 45,-62),1)
    pygame.draw.rect(windowSurface, LBLUE,(601,239, 43,-bikeSelect[bikeSelect[0]][2]*5))
    pygame.draw.rect(windowSurface, RED,(651,239, 43,-bikeSelect[bikeSelect[0]][3]*3))
    pygame.draw.rect(windowSurface, BLUE,(701,239, 43,-bikeSelect[bikeSelect[0]][0]*2.5))
    pygame.draw.rect(windowSurface, BGREEN,(751,239, 43,-bikeSelect[bikeSelect[0]][7]/2))
    accelText = smallFont.render('Accel', True, WHITE,)
    brakeText = smallFont.render('Brake', True, WHITE,)
    speedText = smallFont.render('Speed', True, WHITE,)
    boostText = smallFont.render('Boost', True, WHITE,)
    windowSurface.blit(accelText, (604,228))
    windowSurface.blit(brakeText, (651,228))
    windowSurface.blit(speedText, (701,228))
    windowSurface.blit(boostText, (751,228))

def settingsScreen():
    moveUp = False
    moveDown = False
    moveLeft = False
    moveRight = False
    global WINDOWWIDTH
    global WINDOWHEIGHT
    global sound
    WINDOWWIDTH = width[show[1]]
    WINDOWHEIGHT = height[show[1]]
    while settings[7]:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                    # change the keyboard variables
                    if event.key == K_UP or event.key == ord('w'):#Curser Up
                        moveDown = False
                        moveUp = True
                    if event.key == K_DOWN or event.key == ord('s'):#Curser Down
                        moveUp = False
                        moveDown = True
                    if event.key == K_RIGHT:#Select current option
                        if curser[1]==190:
                            detail[0] +=1
                            if detail[0] >3:
                                detail[0] = 1
                        if curser[1]==290:
                            show[1] +=1
                            if show[1] >5:
                                show[1] = 0
                            WINDOWWIDTH = width[show[1]]
                            WINDOWHEIGHT = height[show[1]]
                    if event.key == K_LEFT:#Select current option
                        if curser[1]==190:
                            detail[0] -=1
                            if detail[0] <1:
                                detail[0] = 3
                        if curser[1]==290:
                            show[1] -=1
                            if show[1] <0:
                                show[1] = 5
                            WINDOWWIDTH = width[show[1]]
                            WINDOWHEIGHT = height[show[1]]
                    if event.key == K_RETURN or event.key == K_SPACE:#
                        if curser[1] == 140:
                            if sound:
                                sound = False
                                settings[5] = 'Sound Off'
                            else:
                                sound = True
                                settings[5] = 'Sound On'
                        if curser[1] == 240:
                            if fps[0] == 1:
                                fps[0] = 0
                            else:
                                fps[0] = 1
                        if curser[1] == 290:
                            setDisplay(WINDOWWIDTH,WINDOWHEIGHT)
                        if curser[1] == 340:
                            if show[0]==0:
                                show[0]=FULLSCREEN
                                screen = pygame.display.get_surface()
                                tmp = screen.convert()
                                WINDOWWIDTH,WINDOWHEIGHT = screen.get_width(),screen.get_height()
                            else:
                                show[0]=0
                            setDisplay(WINDOWWIDTH,WINDOWHEIGHT)
                        if detail[0] == 1:
                            detail[1] = 100000
                        elif detail[0] == 2:
                            detail[1] = 1
                            detail[2] = 0
                        elif detail[0] == 3:
                            detail[1] = 0
                            detail[2] = 0
                        if curser[1] == 390:
                            settings[7]=False
                            menu()

            # move the Curser
        if moveDown and curser[1] < 350:
                curser[1] += MOVESPEED
                moveDown = False
        if moveUp and curser[1] > 150:
                curser[1] -= MOVESPEED
                moveUp = False

        drawBack()
        moveTrack()
        moveScenary()
        drawBanner(gripImage)

        if curser[1]==140:
                curser[2]=140
                option[7]='Press Enter to Enable / Disable Sound'
        if curser[1]==190:
                curser[2]=len(settings[1]*17)
                option[7]='Press Left / Right to change track detail'
        if curser[1]==240:
                curser[2]=145
                option[7]='Press Enter to enable FPS display'
        if curser[1]==290:
                curser[2]=len(settings[1]*17)+len(str(width[show[1]])*17)+len(str(height[show[1]])*17)
                option[7]='Press Left / Right to adjust size - Enter Select'
        if curser[1]==340:
                curser[2]=235
                option[7]='Press Enter to enable fullscreen'
        if curser[1]==390:
                curser[2]=70
                option[7]='Exit Settings'

        # blit the options onto the screen
        text1s = guessFont.render(settings[1] + ' - ' + str(detail[0]), True, BLACK,)
        text1 = guessFont.render(settings[1] + ' - ' + str(detail[0]), True, WHITE,)
        text2s = guessFont.render(settings[2], True, BLACK,)
        text2 = guessFont.render(settings[2], True, WHITE,)
        text3s = guessFont.render(settings[3] + ' - ' + str(WINDOWWIDTH) + ' x ' + str(WINDOWHEIGHT), True, BLACK,)
        text3 = guessFont.render(settings[3] + ' - ' + str(WINDOWWIDTH) + ' x ' + str(WINDOWHEIGHT), True, WHITE,)
        text4s = guessFont.render(settings[4], True, BLACK,)
        text4 = guessFont.render(settings[4], True, WHITE,)
        text5s = guessFont.render(settings[6], True, BLACK,)
        text5 = guessFont.render(settings[6], True, WHITE,)
        text6s = guessFont.render(settings[5], True, BLACK,)
        text6 = guessFont.render(settings[5], True, WHITE,)
        text7s = basicFont.render(option[7], True, BLACK,)
        text7 = basicFont.render(option[7], True, WHITE,)

        windowSurface.blit(text6s, (50,150))
        windowSurface.blit(text6, (52,152))
        windowSurface.blit(text1s, (50,200))
        windowSurface.blit(text1, (52,202))
        windowSurface.blit(text2s, (50,250))
        windowSurface.blit(text2, (52,252))
        windowSurface.blit(text3s, (50,300))
        windowSurface.blit(text3, (52,302))
        windowSurface.blit(text4s, (50,350))
        windowSurface.blit(text4, (52,352))
        windowSurface.blit(text5s, (50,400))
        windowSurface.blit(text5, (51,402))
        windowSurface.blit(text7s, (50,450))
        windowSurface.blit(text7, (51,451))

        # draw the curser onto the surface
        pygame.draw.rect(windowSurface, BLACK, (curser[0],curser[1],curser[2],curser[3]),1)

        backgroundAnim()
        framerate()
        pygame.display.update()

def about():
    while option[8]>=0:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_SPACE:#Return to main menu
                    option[8]=0

        drawBack()
        moveTrack()
        moveScenary()
        drawBanner(gripImage)
        text1s = guessFont.render('W = Accelerate - S = Brake', True, BLACK,)
        text1 = guessFont.render('W = Accelerate - S = Brake', True, WHITE,)
        text2s = guessFont.render('Left & Right Arrow keys = Steering', True, BLACK,)
        text2 = guessFont.render('Left & Right Arrow keys = Steering', True, WHITE,)
        text3s = guessFont.render('Up Arrow key = Boost', True, BLACK,)
        text3 = guessFont.render('Up Arrow key = Boost', True, WHITE,)
        text4s = guessFont.render('Try to beat the lap record without cutting corners!' , True, BLACK,)
        text4 = guessFont.render('Try to beat the lap record without cutting corners!', True, WHITE,)
        text5s = guessFont.render('0.5 seconds on the grass invalidates the lap', True, BLACK,)
        text5 = guessFont.render('0.5 seconds on the grass invalidates the lap', True, WHITE,)
        text6s = guessFont.render('Make sure you cross the white sector timing lines', True, BLACK,)
        text6 = guessFont.render('Make sure you cross the white sector timing lines', True, WHITE,)
        text7s = guessFont.render('You have ten laps to beat the time!', True, BLACK,)
        text7 = guessFont.render('You have ten laps to beat the time!', True, WHITE,)
        windowSurface.blit(text1s, (30,150))
        windowSurface.blit(text1, (32,152))
        windowSurface.blit(text2s, (30,200))
        windowSurface.blit(text2, (32,202))
        windowSurface.blit(text3s, (30,250))
        windowSurface.blit(text3, (32,252))
        windowSurface.blit(text4s, (30,300))
        windowSurface.blit(text4, (32,302))
        windowSurface.blit(text5s, (30,350))
        windowSurface.blit(text5, (32,352))
        windowSurface.blit(text6s, (30,400))
        windowSurface.blit(text6, (32,402))
        windowSurface.blit(text7s, (30,450))
        windowSurface.blit(text7, (32,452))
        backgroundAnim()
        option[8]-=1
        timer=int(option[8]/40)
        text8s = guessFont.render(str(timer), True, BLACK,)
        text8 = guessFont.render(str(timer), True, WHITE,)
        windowSurface.blit(text8s, (769,9))
        windowSurface.blit(text8, (770,10))
        framerate()
        pygame.display.update()

def displayLaptimes():
    while option[8]>0:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_SPACE:#Return to main menu
                    scrollLimits(drawTrack)
                    option[8]=0

        if lapTimes[0] >1:
                if ghostCounter[5]+1 < timer[2]:
                    whereGhost = playerSettings[0],playerSettings[1]
                    ghostRotatedImage, grotRect, goldCenter = rotation(playerImage,ghostLapRecord[ghostCounter[5]][2], whereGhost,ghostLapRecord[ghostCounter[5]][3])
                    whereShadow = playerSettings[0]-10, playerSettings[1]-5
                    shadowRotatedImage, srotRect, soldCenter = rotation(shadowImage,ghostLapRecord[ghostCounter[5]][2], whereShadow,ghostLapRecord[ghostCounter[5]][3])
                    ghostCounter[5] +=1
                    position[4] = position[0]
                    position[5] = position[1]
                    position[0]=ghostLapRecord[ghostCounter[5]][0]
                    position[1]=ghostLapRecord[ghostCounter[5]][1]
                    position[2] += position[0]-position[4]
                    position[3] += position[1]-position[5]
                    drawBack()
                    moveTrack()

                    for skid in skids:
                    # draw line for skids
                        skidmarks(skid,DGREY)

                    for skid in boost:
                    # draw line for skids
                        skidmarks(skid,DGREY)

                    for dirt in dirty:
                    # draw line on grass for dirt tracks
                        skidmarks(dirt,BROWN)

                    windowSurface.blit(shadowRotatedImage,srotRect)
                    windowSurface.blit(ghostRotatedImage,grotRect)
                    moveScenary()
                else:
                    ghostCounter[5]=1

        headf = normalFont.render(str('Lap Time'), True, WHITE,)
        head1 = normalFont.render(str('Sector 1'), True, WHITE,)
        head2 = normalFont.render(str('Sector 2'), True, WHITE,)
        head3 = normalFont.render(str('Sector 3'), True, WHITE,)
        recordf = guessFont.render("%.2f" %(int(lapRecord[0])/60), True, newLapRecord[1],)
        record1 = guessFont.render("%.2f" %(int(lapRecord[1])/60), True, newLapRecord[1],)
        record2 = guessFont.render("%.2f" %(int(lapRecord[2])/60), True, newLapRecord[1],)
        record3 = guessFont.render("%.2f" %(int(lapRecord[3])/60), True, newLapRecord[1],)
        lap1f = guessFont.render("%.2f" %((lapTimes[2][0]/60)), True, lapTimes[2][6],)
        lap11 = guessFont.render("%.2f" %((lapTimes[2][1]/60)), True, lapTimes[2][7],)
        lap12 = guessFont.render("%.2f" %((lapTimes[2][2]/60)), True, lapTimes[2][8],)
        lap13 = guessFont.render("%.2f" %((lapTimes[2][0]-(lapTimes[2][1]+lapTimes[2][2]))/60), True, lapTimes[2][9],)
        lap2f = guessFont.render("%.2f" %((lapTimes[3][0]/60)), True, lapTimes[3][6],)
        lap21 = guessFont.render("%.2f" %((lapTimes[3][1]/60)), True, lapTimes[3][7],)
        lap22 = guessFont.render("%.2f" %((lapTimes[3][2]/60)), True, lapTimes[3][8],)
        lap23 = guessFont.render("%.2f" %((lapTimes[3][0]-(lapTimes[3][1]+lapTimes[3][2]))/60), True, lapTimes[3][9],)
        lap3f = guessFont.render("%.2f" %((lapTimes[4][0]/60)), True, lapTimes[4][6],)
        lap31 = guessFont.render("%.2f" %((lapTimes[4][1]/60)), True, lapTimes[4][7],)
        lap32 = guessFont.render("%.2f" %((lapTimes[4][2]/60)), True, lapTimes[4][8],)
        lap33 = guessFont.render("%.2f" %((lapTimes[4][0]-(lapTimes[4][1]+lapTimes[4][2]))/60), True, lapTimes[4][9],)
        lap4f = guessFont.render("%.2f" %((lapTimes[5][0]/60)), True, lapTimes[5][6],)
        lap41 = guessFont.render("%.2f" %((lapTimes[5][1]/60)), True, lapTimes[5][7],)
        lap42 = guessFont.render("%.2f" %((lapTimes[5][2]/60)), True, lapTimes[4][8],)
        lap43 = guessFont.render("%.2f" %((lapTimes[5][0]-(lapTimes[5][1]+lapTimes[5][2]))/60), True, lapTimes[4][9],)
        lap5f = guessFont.render("%.2f" %((lapTimes[6][0]/60)), True, lapTimes[6][6],)
        lap51 = guessFont.render("%.2f" %((lapTimes[6][1]/60)), True, lapTimes[6][7],)
        lap52 = guessFont.render("%.2f" %((lapTimes[6][2]/60)), True, lapTimes[6][8],)
        lap53 = guessFont.render("%.2f" %((lapTimes[6][0]-(lapTimes[6][1]+lapTimes[6][2]))/60), True, lapTimes[6][9],)
        lap6f = guessFont.render("%.2f" %((lapTimes[7][0]/60)), True, lapTimes[7][6],)
        lap61 = guessFont.render("%.2f" %((lapTimes[7][1]/60)), True, lapTimes[7][7],)
        lap62 = guessFont.render("%.2f" %((lapTimes[7][2]/60)), True, lapTimes[7][8],)
        lap63 = guessFont.render("%.2f" %((lapTimes[7][0]-(lapTimes[7][1]+lapTimes[7][2]))/60), True, lapTimes[7][9],)
        lap7f = guessFont.render("%.2f" %((lapTimes[8][0]/60)), True, lapTimes[8][6],)
        lap71 = guessFont.render("%.2f" %((lapTimes[8][1]/60)), True, lapTimes[8][7],)
        lap72 = guessFont.render("%.2f" %((lapTimes[8][2]/60)), True, lapTimes[8][8],)
        lap73 = guessFont.render("%.2f" %((lapTimes[8][0]-(lapTimes[8][1]+lapTimes[8][2]))/60), True, lapTimes[8][9],)
        lap8f = guessFont.render("%.2f" %((lapTimes[9][0]/60)), True, lapTimes[9][6],)
        lap81 = guessFont.render("%.2f" %((lapTimes[9][1]/60)), True, lapTimes[9][7],)
        lap82 = guessFont.render("%.2f" %((lapTimes[9][2]/60)), True, lapTimes[9][8],)
        lap83 = guessFont.render("%.2f" %((lapTimes[9][0]-(lapTimes[9][1]+lapTimes[9][2]))/60), True, lapTimes[9][9],)
        lap9f = guessFont.render("%.2f" %((lapTimes[10][0]/60)), True, lapTimes[10][6],)
        lap91 = guessFont.render("%.2f" %((lapTimes[10][1]/60)), True, lapTimes[10][7],)
        lap92 = guessFont.render("%.2f" %((lapTimes[10][2]/60)), True, lapTimes[10][8],)
        lap93 = guessFont.render("%.2f" %((lapTimes[10][0]-(lapTimes[10][1]+lapTimes[10][2]))/60), True, lapTimes[10][9],)
        lap10f = guessFont.render("%.2f" %((lapTimes[11][0]/60)), True, lapTimes[11][6],)
        lap101 = guessFont.render("%.2f" %((lapTimes[11][1]/60)), True, lapTimes[11][7],)
        lap102 = guessFont.render("%.2f" %((lapTimes[11][2]/60)), True, lapTimes[11][8],)
        lap103 = guessFont.render("%.2f" %((lapTimes[11][0]-(lapTimes[11][1]+lapTimes[11][2]))/60), True, lapTimes[11][9],)
        if newLapRecord[0]:
            recordt = normalFont.render('Congratulations! You beat the lap record by ' + "%.2f" %((originalLapRecord-timer[2])/60) + ' seconds', True, newLapRecord[1],)
        else:
            recordt = normalFont.render('Unlucky! You missed the lap record by ' + "%.2f" %((timer[2]-originalLapRecord)/60) + ' seconds', True, newLapRecord[1],)
        topfive =normalFont.render(newLapRecord[2], True, newLapRecord[1],)
        pygame.draw.rect(windowSurface, WHITE, (45,165,360,35),1)
        windowSurface.blit(headf, (30,140))
        windowSurface.blit(head1, (130,140))
        windowSurface.blit(head2, (230,140))
        windowSurface.blit(head3, (330,140))
        windowSurface.blit(recordf, (50,170))
        windowSurface.blit(record1, (150,170))
        windowSurface.blit(record2, (250,170))
        windowSurface.blit(record3, (350,170))
        windowSurface.blit(lap1f, (50,200))
        windowSurface.blit(lap11, (150,200))
        windowSurface.blit(lap12, (250,200))
        windowSurface.blit(lap13, (350,200))
        windowSurface.blit(lap2f, (50,220))
        windowSurface.blit(lap21, (150,220))
        windowSurface.blit(lap22, (250,220))
        windowSurface.blit(lap23, (350,220))
        windowSurface.blit(lap3f, (50,240))
        windowSurface.blit(lap31, (150,240))
        windowSurface.blit(lap32, (250,240))
        windowSurface.blit(lap33, (350,240))
        windowSurface.blit(lap4f, (50,260))
        windowSurface.blit(lap41, (150,260))
        windowSurface.blit(lap42, (250,260))
        windowSurface.blit(lap43, (350,260))
        windowSurface.blit(lap5f, (50,280))
        windowSurface.blit(lap51, (150,280))
        windowSurface.blit(lap52, (250,280))
        windowSurface.blit(lap53, (350,280))
        windowSurface.blit(lap6f, (50,300))
        windowSurface.blit(lap61, (150,300))
        windowSurface.blit(lap62, (250,300))
        windowSurface.blit(lap63, (350,300))
        windowSurface.blit(lap7f, (50,320))
        windowSurface.blit(lap71, (150,320))
        windowSurface.blit(lap72, (250,320))
        windowSurface.blit(lap73, (350,320))
        windowSurface.blit(lap8f, (50,340))
        windowSurface.blit(lap81, (150,340))
        windowSurface.blit(lap82, (250,340))
        windowSurface.blit(lap83, (350,340))
        windowSurface.blit(lap9f, (50,360))
        windowSurface.blit(lap91, (150,360))
        windowSurface.blit(lap92, (250,360))
        windowSurface.blit(lap93, (350,360))
        windowSurface.blit(lap10f, (50,380))
        windowSurface.blit(lap101, (150,380))
        windowSurface.blit(lap102, (250,380))
        windowSurface.blit(lap103, (350,380))
        windowSurface.blit(recordt, (50,420))
        windowSurface.blit(topfive, (50,460))
        framerate()
        pygame.display.update()
    menu()

def moveTrack():
    if drawTrack[0] == 1:
        windowSurface.blit(trackImage62,(position[0]-1000,position[1]-115))
        windowSurface.blit(trackImage6,(position[0]-700,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]-400,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]-100,position[1]-100))
        windowSurface.blit(trackImage6,(position[0],position[1]-100))
        windowSurface.blit(trackImage64,(position[0]+300,position[1]-100))
        windowSurface.blit(trackImage41,(position[0]+600,position[1]-100))
        windowSurface.blit(trackImage31,(position[0]+600,position[1]+300))
        windowSurface.blit(trackImage63,(position[0]+300,position[1]+385))
        windowSurface.blit(trackImage6,(position[0],position[1]+400))
        windowSurface.blit(trackImage6,(position[0]-300,position[1]+400))
        windowSurface.blit(trackImage61,(position[0]-600,position[1]+400))
        windowSurface.blit(trackImage12,(position[0]-1100,position[1]+400))
        windowSurface.blit(trackImage22,(position[0]-1100,position[1]+900))
        windowSurface.blit(trackImage62,(position[0]-600,position[1]+1085))
        windowSurface.blit(trackImage6,(position[0]-300,position[1]+1100))
        windowSurface.blit(trackImage6,(position[0],position[1]+1100))
        windowSurface.blit(trackImage6,(position[0]+300,position[1]+1100))
        windowSurface.blit(trackImage6,(position[0]+600,position[1]+1100))
        windowSurface.blit(trackImage63,(position[0]+900,position[1]+1085))
        windowSurface.blit(trackImage34,(position[0]+1200,position[1]+700))
        windowSurface.blit(trackImage53,(position[0]+1585,position[1]+400))
        windowSurface.blit(trackImage54,(position[0]+1585,position[1]+100))
        windowSurface.blit(trackImage41,(position[0]+1500,position[1]-300))
        windowSurface.blit(trackImage21,(position[0]+1100,position[1]-400))
        windowSurface.blit(trackImage44,(position[0]+700,position[1]-1100))
        windowSurface.blit(trackImage11,(position[0]+300,position[1]-1100))
        windowSurface.blit(trackImage31,(position[0]+200,position[1]-700))
        windowSurface.blit(trackImage63,(position[0]-100,position[1]-615))
        windowSurface.blit(trackImage62,(position[0]-100,position[1]-615))
        windowSurface.blit(trackImage22,(position[0]-600,position[1]-800))
        windowSurface.blit(trackImage41,(position[0]-700,position[1]-1200))
        windowSurface.blit(trackImage64,(position[0]-1000,position[1]-1200))
        windowSurface.blit(trackImage61,(position[0]-1000,position[1]-1200))
        windowSurface.blit(trackImage14,(position[0]-1700,position[1]-1200))
        windowSurface.blit(trackImage24,(position[0]-1700,position[1]-500))
        # Timing Lines
        finishLine = pygame.draw.rect(windowSurface, WHITE,(position[0]+50,position[1]-100, 1,300))
        section1 = pygame.draw.rect(windowSurface, WHITE,(position[0],position[1]+1100, 1,300))
        section2 = pygame.draw.rect(windowSurface, WHITE,(position[0]-700,position[1]-1200, 1,300))

    if drawTrack[0] == 2:
        windowSurface.blit(trackImage64,(position[0]-100,position[1]-100))
        windowSurface.blit(trackImage41,(position[0]+200,position[1]-100))
        windowSurface.blit(trackImage32,(position[0]+100,position[1]+300))
        windowSurface.blit(trackImage11,(position[0]-300,position[1]+500))
        windowSurface.blit(trackImage22,(position[0]-300,position[1]+900))
        windowSurface.blit(trackImage62,(position[0]+200,position[1]+1085))
        windowSurface.blit(trackImage63,(position[0]+500,position[1]+1085))
        windowSurface.blit(trackImage31,(position[0]+800,position[1]+1000))
        windowSurface.blit(trackImage53,(position[0]+885,position[1]+700))
        windowSurface.blit(trackImage5,(position[0]+900,position[1]+400))
        windowSurface.blit(trackImage5,(position[0]+900,position[1]+100))
        windowSurface.blit(trackImage54,(position[0]+885,position[1]-200))
        windowSurface.blit(trackImage42,(position[0]+700,position[1]-700))
        windowSurface.blit(trackImage21,(position[0]+300,position[1]-800))
        windowSurface.blit(trackImage42,(position[0]+100,position[1]-1300))
        windowSurface.blit(trackImage11,(position[0]-300,position[1]-1300))
        windowSurface.blit(trackImage32,(position[0]-500,position[1]-900))
        windowSurface.blit(trackImage63,(position[0]-800,position[1]-715))
        windowSurface.blit(trackImage6,(position[0]-1100,position[1]-700))
        windowSurface.blit(trackImage61,(position[0]-1400,position[1]-700))
        windowSurface.blit(trackImage11,(position[0]-1800,position[1]-700))
        windowSurface.blit(trackImage51,(position[0]-1800,position[1]-300))
        windowSurface.blit(trackImage52,(position[0]-1800,position[1]))
        windowSurface.blit(trackImage22,(position[0]-1800,position[1]+300))
        windowSurface.blit(trackImage62,(position[0]-1300,position[1]+485))
        windowSurface.blit(trackImage31,(position[0]-1000,position[1]+400))
        windowSurface.blit(trackImage12,(position[0]-900,position[1]-100))
        windowSurface.blit(trackImage61,(position[0]-400,position[1]-100))

        # Timing Lines
        finishLine = pygame.draw.rect(windowSurface, WHITE,(position[0]+50,position[1]-100, 1,300))
        section1 = pygame.draw.rect(windowSurface, WHITE,(position[0]+400,position[1]+1100, 1,300))
        section2 = pygame.draw.rect(windowSurface, WHITE,(position[0]+100,position[1]-1300, 1,300))

    if drawTrack[0] == 3:
        # Track Circs
        windowSurface.blit(trackImage61,(position[0]-900,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]-600,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]-300,position[1]-100))
        windowSurface.blit(trackImage6,(position[0],position[1]-100))
        windowSurface.blit(trackImage64,(position[0]+200,position[1]-100))
        windowSurface.blit(trackImage41,(position[0]+500,position[1]-100))
        windowSurface.blit(trackImage31,(position[0]+500,position[1]+300))
        windowSurface.blit(trackImage11,(position[0]+100,position[1]+400))
        windowSurface.blit(trackImage21,(position[0]+100,position[1]+800))
        windowSurface.blit(trackImage62,(position[0]+500,position[1]+885))
        windowSurface.blit(trackImage31,(position[0]+800,position[1]+800))
        windowSurface.blit(trackImage11,(position[0]+900,position[1]+400))
        windowSurface.blit(trackImage41,(position[0]+1300,position[1]+400))
        windowSurface.blit(trackImage54,(position[0]+1385,position[1]+800))
        windowSurface.blit(trackImage53,(position[0]+1385,position[1]+900))
        windowSurface.blit(trackImage34,(position[0]+1000,position[1]+1200))
        windowSurface.blit(trackImage63,(position[0]+700,position[1]+1585))
        windowSurface.blit(trackImage62,(position[0]+400,position[1]+1585))
        windowSurface.blit(trackImage21,(position[0],position[1]+1500))
        windowSurface.blit(trackImage41,(position[0]-100,position[1]+1100))
        windowSurface.blit(trackImage11,(position[0]-500,position[1]+1100))
        windowSurface.blit(trackImage31,(position[0]-600,position[1]+1500))
        windowSurface.blit(trackImage22,(position[0]-1100,position[1]+1400))
        windowSurface.blit(trackImage12,(position[0]-1100,position[1]+900))
        windowSurface.blit(trackImage31,(position[0]-600,position[1]+800))
        windowSurface.blit(trackImage41,(position[0]-600,position[1]+400))
        windowSurface.blit(trackImage64,(position[0]-900,position[1]+400))
        windowSurface.blit(trackImage62,(position[0]-900,position[1]+385))
        windowSurface.blit(trackImage21,(position[0]-1300,position[1]+300))
        windowSurface.blit(trackImage11,(position[0]-1300,position[1]-100))

        # Timing Lines
        finishLine = pygame.draw.rect(windowSurface, WHITE,(position[0]+50,position[1]-100, 1,300))
        section1 = pygame.draw.rect(windowSurface, WHITE,(position[0]+900,position[1]+1600, 1,300))
        section2 = pygame.draw.rect(windowSurface, WHITE,(position[0]-600,position[1]+900, 1,300))

    if drawTrack[0] == 4:
        windowSurface.blit(trackImage61,(position[0]-100,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]+100,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]+400,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]+700,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]+1000,position[1]-100))
        windowSurface.blit(trackImage64,(position[0]+1200,position[1]-100))
        windowSurface.blit(trackImage41,(position[0]+1500,position[1]-100))
        windowSurface.blit(trackImage22,(position[0]+1600,position[1]+300))
        windowSurface.blit(trackImage32,(position[0]+2100,position[1]+300))
        windowSurface.blit(trackImage11,(position[0]+2300,position[1]-100))
        windowSurface.blit(trackImage43,(position[0]+2700,position[1]-100))
        windowSurface.blit(trackImage54,(position[0]+2985,position[1]+500))
        windowSurface.blit(trackImage33,(position[0]+2700,position[1]+800))
        windowSurface.blit(trackImage63,(position[0]+2400,position[1]+1085))
        windowSurface.blit(trackImage6,(position[0]+2100,position[1]+1100))
        windowSurface.blit(trackImage62,(position[0]+1800,position[1]+1085))
        windowSurface.blit(trackImage22,(position[0]+1300,position[1]+900))
        windowSurface.blit(trackImage42,(position[0]+1100,position[1]+400))
        windowSurface.blit(trackImage11,(position[0]+700,position[1]+400))
        windowSurface.blit(trackImage51,(position[0]+700,position[1]+800))
        windowSurface.blit(trackImage22,(position[0]+700,position[1]+1100))
        windowSurface.blit(trackImage41,(position[0]+1200,position[1]+1300))
        windowSurface.blit(trackImage33,(position[0]+1000,position[1]+1700))
        windowSurface.blit(trackImage21,(position[0]+600,position[1]+1900))
        windowSurface.blit(trackImage41,(position[0]+500,position[1]+1500))
        windowSurface.blit(trackImage21,(position[0]+100,position[1]+1400))
        windowSurface.blit(trackImage52,(position[0]+100,position[1]+1100))
        windowSurface.blit(trackImage41,(position[0],position[1]+700))
        windowSurface.blit(trackImage23,(position[0]-600,position[1]+400))
        windowSurface.blit(trackImage12,(position[0]-600,position[1]-100))

        # Timing Lines
        finishLine = pygame.draw.rect(windowSurface, WHITE,(position[0]+50,position[1]-100, 1,300))
        section1 = pygame.draw.rect(windowSurface, WHITE,(position[0]+3000,position[1]+600, 300,1))
        section2 = pygame.draw.rect(windowSurface, WHITE,(position[0]+700,position[1]+900, 300,1))

    if drawTrack[0] == 5:
        windowSurface.blit(trackImage11,(position[0]-1300,position[1]-100))
        windowSurface.blit(trackImage61,(position[0]-900,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]-600,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]-300,position[1]-100))
        windowSurface.blit(trackImage6,(position[0],position[1]-100))
        windowSurface.blit(trackImage6,(position[0]+300,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]+600,position[1]-100))
        windowSurface.blit(trackImage64,(position[0]+900,position[1]-100))
        windowSurface.blit(trackImage44,(position[0]+1200,position[1]-100))
        windowSurface.blit(trackImage54,(position[0]+1585,position[1]+600))
        windowSurface.blit(trackImage31,(position[0]+1500,position[1]+900))
        windowSurface.blit(trackImage21,(position[0]+1100,position[1]+900))
        windowSurface.blit(trackImage41,(position[0]+1000,position[1]+500))
        windowSurface.blit(trackImage64,(position[0]+700,position[1]+500))
        windowSurface.blit(trackImage61,(position[0]+400,position[1]+500))
        windowSurface.blit(trackImage11,(position[0],position[1]+500))
        windowSurface.blit(trackImage21,(position[0],position[1]+900))
        windowSurface.blit(trackImage41,(position[0]+400,position[1]+1000))
        windowSurface.blit(trackImage54,(position[0]+485,position[1]+1400))
        windowSurface.blit(trackImage33,(position[0]+200,position[1]+1700))
        windowSurface.blit(trackImage63,(position[0]-100,position[1]+1985))
        windowSurface.blit(trackImage6,(position[0]-300,position[1]+2000))
        windowSurface.blit(trackImage62,(position[0]-600,position[1]+1985))
        windowSurface.blit(trackImage21,(position[0]-1000,position[1]+1900))
        windowSurface.blit(trackImage11,(position[0]-1000,position[1]+1500))
        windowSurface.blit(trackImage31,(position[0]-600,position[1]+1400))
        windowSurface.blit(trackImage53,(position[0]-515,position[1]+1100))
        windowSurface.blit(trackImage54,(position[0]-515,position[1]+800))
        windowSurface.blit(trackImage41,(position[0]-600,position[1]+400))
        windowSurface.blit(trackImage64,(position[0]-900,position[1]+400))
        windowSurface.blit(trackImage62,(position[0]-900,position[1]+385))
        windowSurface.blit(trackImage21,(position[0]-1300,position[1]+300))
        windowSurface.blit(trackImage11,(position[0]-1300,position[1]-100))

        # Timing Lines
        finishLine = pygame.draw.rect(windowSurface, WHITE,(position[0]+50,position[1]-100, 1,300))
        section1 = pygame.draw.rect(windowSurface, WHITE,(position[0]+1500,position[1]+1000, 1,300))
        section2 = pygame.draw.rect(windowSurface, WHITE,(position[0]-500,position[1]+2000, 1,300))

    if drawTrack[0] == 6:
        windowSurface.blit(trackImage12,(position[0]-1800,position[1]-100))
        windowSurface.blit(trackImage61,(position[0]-1300,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]-1200,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]-900,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]-600,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]-300,position[1]-100))
        windowSurface.blit(trackImage6,(position[0],position[1]-100))
        windowSurface.blit(trackImage6,(position[0]+300,position[1]-100))
        windowSurface.blit(trackImage64,(position[0]+600,position[1]-100))
        windowSurface.blit(trackImage42,(position[0]+900,position[1]-100))
        windowSurface.blit(trackImage54,(position[0]+1085,position[1]+400))
        windowSurface.blit(trackImage5,(position[0]+1100,position[1]+700))
        windowSurface.blit(trackImage5,(position[0]+1100,position[1]+1000))
        windowSurface.blit(trackImage5,(position[0]+1100,position[1]+1300))
        windowSurface.blit(trackImage5,(position[0]+1100,position[1]+1600))
        windowSurface.blit(trackImage53,(position[0]+1085,position[1]+1900))
        windowSurface.blit(trackImage34,(position[0]+700,position[1]+2200))
        windowSurface.blit(trackImage22,(position[0]+200,position[1]+2400))
        windowSurface.blit(trackImage52,(position[0]+200,position[1]+2100))
        windowSurface.blit(trackImage5,(position[0]+200,position[1]+1800))
        windowSurface.blit(trackImage54,(position[0]+185,position[1]+1500))
        windowSurface.blit(trackImage44,(position[0]-200,position[1]+800))
        windowSurface.blit(trackImage64,(position[0]-500,position[1]+800))
        windowSurface.blit(trackImage6,(position[0]-800,position[1]+800))
        windowSurface.blit(trackImage62,(position[0]-1100,position[1]+785))
        windowSurface.blit(trackImage24,(position[0]-1800,position[1]+400))

        # Timing Lines
        finishLine = pygame.draw.rect(windowSurface, WHITE,(position[0]+50,position[1]-100, 1,300))
        section1 = pygame.draw.rect(windowSurface, WHITE,(position[0]+700,position[1]+2600, 1,300))
        section2 = pygame.draw.rect(windowSurface, WHITE,(position[0]-1000,position[1]+800, 1,300))

    if drawTrack[0] == 7:
        windowSurface.blit(trackImage11,(position[0]-700,position[1]-100))
        windowSurface.blit(trackImage61,(position[0]-300,position[1]-100))
        windowSurface.blit(trackImage64,(position[0],position[1]-100))
        windowSurface.blit(trackImage41,(position[0]+300,position[1]-100))
        windowSurface.blit(trackImage32,(position[0]+200,position[1]+300))
        windowSurface.blit(trackImage11,(position[0]-200,position[1]+500))
        windowSurface.blit(trackImage23,(position[0]-200,position[1]+900))
        windowSurface.blit(trackImage34,(position[0]+400,position[1]+800))
        windowSurface.blit(trackImage53,(position[0]+785,position[1]+500))
        windowSurface.blit(trackImage51,(position[0]+800,position[1]+400))
        windowSurface.blit(trackImage14,(position[0]+800,position[1]-300))
        windowSurface.blit(trackImage34,(position[0]+1500,position[1]-700))
        windowSurface.blit(trackImage44,(position[0]+1500,position[1]-1400))
        windowSurface.blit(trackImage13,(position[0]+900,position[1]-1400))
        windowSurface.blit(trackImage32,(position[0]+700,position[1]-800))
        windowSurface.blit(trackImage21,(position[0]+300,position[1]-700))
        windowSurface.blit(trackImage43,(position[0],position[1]-1300))
        windowSurface.blit(trackImage14,(position[0]-700,position[1]-1300))
        windowSurface.blit(trackImage34,(position[0]-1100,position[1]-600))
        windowSurface.blit(trackImage11,(position[0]-1500,position[1]-200))
        windowSurface.blit(trackImage23,(position[0]-1500,position[1]+200))
        windowSurface.blit(trackImage32,(position[0]-900,position[1]+300))
        windowSurface.blit(trackImage11,(position[0]-700,position[1]-100))

        # Timing Lines
        finishLine = pygame.draw.rect(windowSurface, WHITE,(position[0]+50,position[1]-100, 1,300))
        section1 = pygame.draw.rect(windowSurface, WHITE,(position[0]+400,position[1]+1200, 1,300))
        section2 = pygame.draw.rect(windowSurface, WHITE,(position[0]+700,position[1]-600, 1,300))

    if drawTrack[0] == 8:
        windowSurface.blit(trackImage14,(position[0]-1200,position[1]-100))
        windowSurface.blit(trackImage61,(position[0]-500,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]-200,position[1]-100))
        windowSurface.blit(trackImage63,(position[0]+100,position[1]-115))
        windowSurface.blit(trackImage31,(position[0]+400,position[1]-200))
        windowSurface.blit(trackImage14,(position[0]+500,position[1]-900))
        windowSurface.blit(trackImage44,(position[0]+1200,position[1]-900))
        windowSurface.blit(trackImage34,(position[0]+1200,position[1]-200))
        windowSurface.blit(trackImage11,(position[0]+800,position[1]+200))
        windowSurface.blit(trackImage51,(position[0]+800,position[1]+600))
        windowSurface.blit(trackImage52,(position[0]+800,position[1]+600))
        windowSurface.blit(trackImage21,(position[0]+800,position[1]+900))
        windowSurface.blit(trackImage32,(position[0]+1200,position[1]+800))
        windowSurface.blit(trackImage11,(position[0]+1400,position[1]+400))
        windowSurface.blit(trackImage61,(position[0]+1800,position[1]+400))
        windowSurface.blit(trackImage6,(position[0]+2100,position[1]+400))
        windowSurface.blit(trackImage63,(position[0]+2400,position[1]+385))
        windowSurface.blit(trackImage33,(position[0]+2700,position[1]+100))
        windowSurface.blit(trackImage11,(position[0]+3000,position[1]-300))
        windowSurface.blit(trackImage44,(position[0]+3400,position[1]-300))
        windowSurface.blit(trackImage34,(position[0]+3400,position[1]+400))
        windowSurface.blit(trackImage14,(position[0]+2700,position[1]+800))
        windowSurface.blit(trackImage33,(position[0]+2400,position[1]+1500))
        windowSurface.blit(trackImage63,(position[0]+2100,position[1]+1785))
        windowSurface.blit(trackImage6,(position[0]+1800,position[1]+1800))
        windowSurface.blit(trackImage6,(position[0]+1500,position[1]+1800))
        windowSurface.blit(trackImage6,(position[0]+1200,position[1]+1800))
        windowSurface.blit(trackImage62,(position[0]+900,position[1]+1785))
        windowSurface.blit(trackImage21,(position[0]+500,position[1]+1700))
        windowSurface.blit(trackImage41,(position[0]+400,position[1]+1300))
        windowSurface.blit(trackImage64,(position[0]+100,position[1]+1300))
        windowSurface.blit(trackImage6,(position[0]-200,position[1]+1300))
        windowSurface.blit(trackImage62,(position[0]-500,position[1]+1285))
        windowSurface.blit(trackImage24,(position[0]-1200,position[1]+900))
        windowSurface.blit(trackImage52,(position[0]-1200,position[1]+600))
        windowSurface.blit(trackImage51,(position[0]-1200,position[1]+600))

        # Timing Lines
        finishLine = pygame.draw.rect(windowSurface, WHITE,(position[0]+50,position[1]-100, 1,300))
        section1 = pygame.draw.rect(windowSurface, WHITE,(position[0]+800,position[1]+700, 300,1))
        section2 = pygame.draw.rect(windowSurface, WHITE,(position[0]+1700,position[1]+1800, 1,300))

    if drawTrack[0] == 9:
        windowSurface.blit(trackImage11,(position[0]-800,position[1]-100))
        windowSurface.blit(trackImage61,(position[0]-400,position[1]-100))
        windowSurface.blit(trackImage6,(position[0]-100,position[1]-100))
        windowSurface.blit(trackImage63,(position[0]+200,position[1]-115))
        windowSurface.blit(trackImage31,(position[0]+500,position[1]-200))
        windowSurface.blit(trackImage11,(position[0]+600,position[1]-600))
        windowSurface.blit(trackImage44,(position[0]+1000,position[1]-600))
        windowSurface.blit(trackImage54,(position[0]+1385,position[1]+100))
        windowSurface.blit(trackImage53,(position[0]+1385,position[1]+100))
        windowSurface.blit(trackImage34,(position[0]+1000,position[1]+400))
        windowSurface.blit(trackImage21,(position[0]+600,position[1]+700))
        windowSurface.blit(trackImage41,(position[0]+500,position[1]+300))
        windowSurface.blit(trackImage13,(position[0]-100,position[1]+300))
        windowSurface.blit(trackImage23,(position[0]-100,position[1]+900))
        windowSurface.blit(trackImage42,(position[0]+500,position[1]+1200))
        windowSurface.blit(trackImage54,(position[0]+685,position[1]+1700))
        windowSurface.blit(trackImage52,(position[0]+700,position[1]+1700))
        windowSurface.blit(trackImage22,(position[0]+700,position[1]+2000))
        windowSurface.blit(trackImage41,(position[0]+1200,position[1]+2200))
        windowSurface.blit(trackImage32,(position[0]+1100,position[1]+2600))
        windowSurface.blit(trackImage63,(position[0]+800,position[1]+2785))
        windowSurface.blit(trackImage6,(position[0]+500,position[1]+2800))
        windowSurface.blit(trackImage62,(position[0]+200,position[1]+2785))
        windowSurface.blit(trackImage24,(position[0]-500,position[1]+2400))
        windowSurface.blit(trackImage52,(position[0]-500,position[1]+2100))
        windowSurface.blit(trackImage5,(position[0]-500,position[1]+1800))
        windowSurface.blit(trackImage54,(position[0]-515,position[1]+1600))
        windowSurface.blit(trackImage42,(position[0]-700,position[1]+1100))
        windowSurface.blit(trackImage23,(position[0]-1300,position[1]+800))
        windowSurface.blit(trackImage11,(position[0]-1300,position[1]+400))
        windowSurface.blit(trackImage31,(position[0]-900,position[1]+300))
        # Timing Lines
        finishLine = pygame.draw.rect(windowSurface, WHITE,(position[0]+50,position[1]-100, 1,300))
        section1 = pygame.draw.rect(windowSurface, WHITE,(position[0]+1400,position[1]+200, 300,1))
        section2 = pygame.draw.rect(windowSurface, WHITE,(position[0]+1300,position[1]+2600, 300,1))
    return finishLine, section1, section2

def moveScenary():
    if drawTrack[0] == 1:
        if detail[0] == 3:
            windowSurface.blit(scenaryImage1,(position[0]+1250,position[1]+420))
            windowSurface.blit(scenaryImage1,(position[0]+1260,position[1]+280))
            windowSurface.blit(scenaryImage1,(position[0]+1245,position[1]+180))
            windowSurface.blit(scenaryImage1,(position[0]+1250,position[1]))
            windowSurface.blit(scenaryImage1,(position[0]+1800,position[1]+450))
            windowSurface.blit(scenaryImage1,(position[0]+1810,position[1]+300))
            windowSurface.blit(scenaryImage1,(position[0]+1780,position[1]+180))
            windowSurface.blit(scenaryImage1,(position[0]+1800,position[1]))
            windowSurface.blit(scenaryImage1,(position[0]+1790,position[1]-130))

def drawBack():
    if detail[0] == 3:
        if position[2] >= 200:
            position[2] -=200
        if position[2] <= -200:
            position[2] += 200
        if position[3] >= 200:
            position[3] -= 200
        if position[3] <= -200:
            position[3] += 200
        windowSurface.blit(overheadImage,(position[2]+1200,position[3]-200))
        windowSurface.blit(overheadImage,(position[2]+1000,position[3]-200))
        windowSurface.blit(overheadImage,(position[2]+800,position[3]-200))
        windowSurface.blit(overheadImage,(position[2]+600,position[3]-200))
        windowSurface.blit(overheadImage,(position[2]+400,position[3]-200))
        windowSurface.blit(overheadImage,(position[2]+200,position[3]-200))
        windowSurface.blit(overheadImage,(position[2],position[3]-200))
        windowSurface.blit(overheadImage,(position[2]-200,position[3]-200))
        windowSurface.blit(overheadImage,(position[2]+1200,position[3]))
        windowSurface.blit(overheadImage,(position[2]+1000,position[3]))
        windowSurface.blit(overheadImage,(position[2]+800,position[3]))
        windowSurface.blit(overheadImage,(position[2]+600,position[3]))
        windowSurface.blit(overheadImage,(position[2]+400,position[3]))
        windowSurface.blit(overheadImage,(position[2]+200,position[3]))
        windowSurface.blit(overheadImage,(position[2],position[3]))
        windowSurface.blit(overheadImage,(position[2]-200,position[3]))
        windowSurface.blit(overheadImage,(position[2]+1200,position[3]+200))
        windowSurface.blit(overheadImage,(position[2]+1000,position[3]+200))
        windowSurface.blit(overheadImage,(position[2]+800,position[3]+200))
        windowSurface.blit(overheadImage,(position[2]+600,position[3]+200))
        windowSurface.blit(overheadImage,(position[2]+400,position[3]+200))
        windowSurface.blit(overheadImage,(position[2]+200,position[3]+200))
        windowSurface.blit(overheadImage,(position[2],position[3]+200))
        windowSurface.blit(overheadImage,(position[2]-200,position[3]+200))
        windowSurface.blit(overheadImage,(position[2]+1200,position[3]+400))
        windowSurface.blit(overheadImage,(position[2]+1000,position[3]+400))
        windowSurface.blit(overheadImage,(position[2]+800,position[3]+400))
        windowSurface.blit(overheadImage,(position[2]+600,position[3]+400))
        windowSurface.blit(overheadImage,(position[2]+400,position[3]+400))
        windowSurface.blit(overheadImage,(position[2]+200,position[3]+400))
        windowSurface.blit(overheadImage,(position[2],position[3]+400))
        windowSurface.blit(overheadImage,(position[2]-200,position[3]+400))
        windowSurface.blit(overheadImage,(position[2]+1200,position[3]+600))
        windowSurface.blit(overheadImage,(position[2]+1000,position[3]+600))
        windowSurface.blit(overheadImage,(position[2]+800,position[3]+600))
        windowSurface.blit(overheadImage,(position[2]+600,position[3]+600))
        windowSurface.blit(overheadImage,(position[2]+400,position[3]+600))
        windowSurface.blit(overheadImage,(position[2]+200,position[3]+600))
        windowSurface.blit(overheadImage,(position[2],position[3]+600))
        windowSurface.blit(overheadImage,(position[2]-200,position[3]+600))
        if WINDOWHEIGHT > 600:
            windowSurface.blit(overheadImage,(position[2]+1200,position[3]+800))
            windowSurface.blit(overheadImage,(position[2]+1000,position[3]+800))
            windowSurface.blit(overheadImage,(position[2]+800,position[3]+800))
            windowSurface.blit(overheadImage,(position[2]+600,position[3]+800))
            windowSurface.blit(overheadImage,(position[2]+400,position[3]+800))
            windowSurface.blit(overheadImage,(position[2]+200,position[3]+800))
            windowSurface.blit(overheadImage,(position[2],position[3]+800))
            windowSurface.blit(overheadImage,(position[2]-200,position[3]+800))
        if WINDOWHEIGHT > 800:
            windowSurface.blit(overheadImage,(position[2]+1200,position[3]+1000))
            windowSurface.blit(overheadImage,(position[2]+1000,position[3]+1000))
            windowSurface.blit(overheadImage,(position[2]+800,position[3]+1000))
            windowSurface.blit(overheadImage,(position[2]+600,position[3]+1000))
            windowSurface.blit(overheadImage,(position[2]+400,position[3]+1000))
            windowSurface.blit(overheadImage,(position[2]+200,position[3]+1000))
            windowSurface.blit(overheadImage,(position[2],position[3]+1000))
            windowSurface.blit(overheadImage,(position[2]-200,position[3]+1000))
        if WINDOWWIDTH > 1000:
            windowSurface.blit(overheadImage,(position[2]+1400,position[3]-200))
            windowSurface.blit(overheadImage,(position[2]+1400,position[3]))
            windowSurface.blit(overheadImage,(position[2]+1400,position[3]+200))
            windowSurface.blit(overheadImage,(position[2]+1400,position[3]+400))
            windowSurface.blit(overheadImage,(position[2]+1400,position[3]+600))
            windowSurface.blit(overheadImage,(position[2]+1400,position[3]+800))
            windowSurface.blit(overheadImage,(position[2]+1400,position[3]+1000))
    else:
        windowSurface.fill(GREEN)

def rotation(image,imageNo,where,degree):
    # Calculate rotated graphics & centre position
    surf =  pygame.Surface((100,50))
    rotatedImage = pygame.transform.rotate(image[imageNo],degree)
    blittedRect = windowSurface.blit(surf, where)
    oldCenter = blittedRect.center
    rotatedSurf =  pygame.transform.rotate(surf, degree)
    rotRect = rotatedSurf.get_rect()
    rotRect.center = oldCenter
    return rotatedImage, rotRect, oldCenter

def skidmarks(skid,colour):
    global position
    originalH = (position[0]-skid[2])+WINDOWWIDTH/2
    originalV = (position[1]-skid[3])+(WINDOWHEIGHT/2)+18
    newH = (position[0]-skid[0])+WINDOWWIDTH/2
    newV = (position[1]-skid[1])+(WINDOWHEIGHT/2)+18
    if originalH >= -50 and originalH <= WINDOWWIDTH+50 and originalV >= -50 and originalV<= WINDOWHEIGHT+50:
        pygame.draw.line(windowSurface, colour,(originalH,originalV),(newH,newV),4)

def recordSkid(skidCount,resolution,location,wheels):
    if skidCount < 1:
        oldRearPosition[0] = rearWheel[0]
        oldRearPosition[1] = rearWheel[1]
        if wheels == 2:
            oldFrontPosition[0] = frontWheel[0]
            oldFrontPosition[1] = frontWheel[1]
        skidCount = resolution
        return skidCount
    elif skidCount > 1:
        skidCount -= 1
        return skidCount
    else:
        skidRear = [rearWheel[0],rearWheel[1],oldRearPosition[0],oldRearPosition[1]]
        location.append(skidRear)
        oldRearPosition[0] = rearWheel[0]
        oldRearPosition[1] = rearWheel[1]
        if wheels == 2:
            skidFront = [frontWheel[0],frontWheel[1],oldFrontPosition[0],oldFrontPosition[1]]
            location.append(skidFront)
            oldFrontPosition[0] = frontWheel[0]
            oldFrontPosition[1] = frontWheel[1]
        skidCount = resolution
        return skidCount

def playSound():
    if accelerating[0]:
        revChannel.play(revSound[revSound[0]])
    else:
        freewheelSound[0] = revSound[0]
        revChannel.play(freewheelSound[freewheelSound[0]])


def TestPy2exe():
    print( "Py2exe Success" )

# run the game loop
setDisplay(WINDOWWIDTH,WINDOWHEIGHT)
lapRecord, lapRecord2, lapRecord3, lapRecord4,lapRecord5 = loadRecords(drawTrack)
shadowImage = shadowGraphics()
ghostImage = ghostGraphics()
previewImage = previewImage()
menu()

#TestPy2exe()

while option[6]==2:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # change the keyboard variables
            if event.key == K_LEFT or event.key == ord('a'):
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
            if event.key == ord('w'):
                moveDown = False
                moveUp = True
            if event.key == ord('s'):
                moveDown = True
            if event.key == K_UP :
                if kers[2] > 0:
                    kers[0] = True
                else:
                    kers[0] = False

            if event.key == K_9: #Show FPS
                if fps[0] == 1:
                    fps = [0,60,10,60,0]
                else:
                    fps[0] = 1
            if event.key == K_EQUALS: #Increase max FPS
                fps[1] += 5
            if event.key == K_MINUS: #Decrease max FPS
                fps[1] -= 5
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                moveUp = False
                movespeed = [0,0,2,0]
                option[6]=0
                position,limit = scrollLimits(drawTrack)
                menu()
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
            if event.key == ord('w'):
                moveUp = False
            if event.key == ord('s'):
                moveDown = False
            if event.key == K_UP:
                kers[0] = False

    bikeSettings = bikeSelect[bikeSelect[0]]

    # Get rotated graphics
    where = playerSettings[0], playerSettings[1]
    playerRotatedImage, rotRect, oldCenter = rotation(playerImage,playerImage[0], where,degree)
    whereShadow = playerSettings[0]-10, playerSettings[1]-5
    shadowRotatedImage, srotRect, soldCenter = rotation(shadowImage,playerImage[0], whereShadow,degree)

    # draw the ghostblock onto the surface
    if lapTimes[0] >1:
        if ghostCounter[5]+1 < timer[1]:
            if ghostCounter[5]+1 < timer[2]:
                whereGhost = (playerSettings[0]+ghostCounter[1]),int(playerSettings[1]+ghostCounter[2])
                ghostRotatedImage, grotRect, goldCenter = rotation(ghostImage,ghostLapRecord[ghostCounter[5]][2], whereGhost,ghostLapRecord[ghostCounter[5]][3])


    # draw the track background onto the surface
    drawBack()

    # draw the track onto the surface
    finishLine, section1, section2 = moveTrack()

    # Check the background colour
    colour = windowSurface.get_at((oldCenter))# centre colour
    if colour[0] >= 88 and colour[0] <= 91 or colour[0] == 165 or colour[0] == 255:
        dirtPosition = 0
    else:
        movespeed[2] = 3
        if playerImage[0]<3:
            playerImage[0] +=1
        if playerImage[0]>7:
            playerImage[0] -= 1
        if movespeed[0] >4:
            bikeSettings[1] -= bikeSettings[3]*2
            cheatCheck[4]+=1
        if movespeed[0] >1:
            dirtPosition = recordSkid(dirtPosition,6,dirty,2)
        revSound[0] = 1
        if sound:
            playSound()

    for skid in skids:
    # draw lines for braking skids
        skidmarks(skid,DGREY)

    for skid in boost:
    # draw line for boosting skids
        skidmarks(skid,DGREY)

    for dirt in dirty:
    # draw line on grass for dirt tracks
        skidmarks(dirt,BROWN)

    # Calculate whether the ghost should be shown / position
    if lapTimes[0] >1:
        if ghostCounter[5]+1 < timer[1]:
            if ghostCounter[5]+1 < timer[2]:
                ghostCounter[5] +=1
                ghostCounter[1]=position[0]-ghostLapRecord[ghostCounter[5]][0]
                ghostCounter[2]=position[1]-ghostLapRecord[ghostCounter[5]][1]
                if (WINDOWWIDTH/2)+ghostCounter[1] >0:
                    if (WINDOWHEIGHT/2)+ghostCounter[2] >0:
                        windowSurface.blit(ghostRotatedImage,grotRect)

    # draw the player onto the surface
    windowSurface.blit(shadowRotatedImage,srotRect)
    windowSurface.blit(playerRotatedImage,rotRect)

    # draw the scenary onto the surface
    moveScenary()

    # Calculate player direction rotation
    degree = -5 * playerSettings[2]
    radians = -degree * (3.142/180)

    if skiding[0] == False:
        moveDegree = degree
        moveRadians = radians
        movespeed[2] = 2
        playerSettings[3] = playerSettings[2]
    else:
        moveDegree = -5 * playerSettings[3]
        moveRadians = -moveDegree * (3.142/180)

    position[0]-=(movespeed[0]*((math.cos(moveRadians))))
    position[1]-=(movespeed[0]*((math.sin(moveRadians))))
    frontWheel[0]=position[0]-(30*((math.cos(radians))))
    frontWheel[1]=position[1]-(30*((math.sin(radians))))
    rearWheel[0]=position[0]+(30*(math.cos(radians)))
    rearWheel[1]=position[1]+(30*(math.sin(radians)))

    position[2]-=(movespeed[0]*((math.cos(moveRadians))))
    position[3]-=(movespeed[0]*((math.sin(moveRadians))))

    if moveLeft:    # Turn Left
        if movespeed[0] > 0:
            bikeSettings[6]-=1
            if bikeSettings[6]==0:
                playerSettings[2] -= 1
                bikeSettings[6] = movespeed[2]
                if playerImage[0] > 1:
                    playerImage[0] -=1
                if playerSettings[2] < 0:
                    playerSettings[2]=71
        if skiding[0]:
            kers[4]-=1
            if kers[4]==0:
                playerSettings[3] -= 1
                kers[4] = movespeed[2]+1
                if playerSettings[3]<0:
                    playerSettings[3]=71

    if moveRight:
        if movespeed[0] > 0:
            bikeSettings[6]-=1
            if bikeSettings[6]==0:
                playerSettings[2] += 1
                bikeSettings[6] = movespeed[2]
                if playerImage[0] < 9:
                    playerImage[0] +=1
                if playerSettings[2]>71:
                    playerSettings[2]=0

        if skiding[0]:
            kers[4]-=1
            if kers[4]==0:
                playerSettings[3] += 1
                kers[4] = movespeed[2]+1
                if playerSettings[3]>71:
                    playerSettings[3]=0

    if moveRight == False and moveLeft == False:
        if playerImage[0]<5:
            playerImage[0] +=1
        elif playerImage[0]>5:
            playerImage[0] -= 1
        if kers[0]: # Straighten whilst boosting & not turning
            if playerSettings[2] < 15 and playerSettings[3] > 60:
                playerSettings[3] += 1
                playerSettings[2] -= 1
            elif playerSettings[3] < 15 and playerSettings[2] > 60:
                playerSettings[2] += 1
                playerSettings[3] -= 1
            elif playerSettings[2] > playerSettings [3]:
                playerSettings[3] += 1
                playerSettings[2] -= 1
            elif playerSettings[2] < playerSettings [3]:
                playerSettings[3] -= 1
                playerSettings[2] += 1
            if playerSettings[2] < 0:
                playerSettings[2] = 71
            elif playerSettings[2] > 71:
                playerSettings[2] = 0
            if playerSettings[3] < 0:
                playerSettings[3] = 71
            elif playerSettings[3] > 71:
                playerSettings[3] = 0

    # check if the player has crossed the section 1 line.
    if rotRect.colliderect(section1):
        if cheatCheck[2] == False:
            cheatCheck[0] = 1
            timer[3] = timer[0]
            timer[4] = 0
            timer[5] = 0
            timer[6] = int(timer[3]) - int(lapRecord[1])
            cheatCheck[2] = True
            cheatCheck[6] = '         '
            displayTimeDif = 50
            if timer[3] <= int(lapRecord[1]):
                lap[7] = BGREEN
            else:
                lap[7] = WHITE
    else:
        cheatCheck[2] = False

    # check if the player has crossed the section 2 line.
    if rotRect.colliderect(section2):
        if cheatCheck[3] == False:
            cheatCheck[0] += 10
            timer[4] = timer[0]-timer[3]
            timer[6] = (int(timer[4]) - int(lapRecord[2])) + (int(timer[3]) - int(lapRecord[1]))
            cheatCheck[3] = True
            displayTimeDif = 50
            if timer[4] <= int(lapRecord[2]):
                lap[8] = BGREEN
            else:
                lap[8] = WHITE
    else:
        cheatCheck[3] = False

    # check if the player has crossed the finish line.
    if rotRect.colliderect(finishLine):
        if lapTimes[0] >=11:
                lapTimeFile = open(drawTrack[drawTrack[0]],'r+')
                lapTimeFile.write(str(lapRecord[0]) + " " + str(lapRecord[1]) + " " + str(lapRecord[2]) + " " + str(lapRecord[3]) + " " + str(lapRecord[4]) + "  \n")
                lapTimeFile.write(str(lapRecord2[0]) + " " + str(lapRecord2[1]) + " " + str(lapRecord2[2]) + " " + str(lapRecord2[3]) + " " + str(lapRecord2[4]) + "  \n")
                lapTimeFile.write(str(lapRecord3[0]) + " " + str(lapRecord3[1]) + " " + str(lapRecord3[2]) + " " + str(lapRecord3[3]) + " " + str(lapRecord3[4]) + "  \n")
                lapTimeFile.write(str(lapRecord4[0]) + " " + str(lapRecord4[1]) + " " + str(lapRecord4[2]) + " " + str(lapRecord4[3]) + " " + str(lapRecord4[4]) + "  \n")
                lapTimeFile.write(str(lapRecord5[0]) + " " + str(lapRecord5[1]) + " " + str(lapRecord5[2]) + " " + str(lapRecord5[3]) + " " + str(lapRecord5[4]) + "  \n")
                lapTimeFile.close()
                gameOver = True

        timer[7] = True
        ghostCounter[0] = True
        if cheatCheck[1] == False:
            if cheatCheck[4] <=cheatCheck[5]:
                cheatCheck[0] +=100
                cheatCheck[6] = '         '
            else:
                cheatCheck[6] = 'Invalid Lap - '
            timer[6]=int(timer[0])-int(lapRecord[0])
            if cheatCheck[0]==111:
                cheatCheck[0]=0
                timer[5]=timer[0]-(timer[3]+timer[4])
                if timer[0] < timer[2] and timer[0] > 0:
                    timer[2] = timer[0]
                    ghostLapRecord = ghostLap
                if timer[0] < int(lapRecord5[0]) and timer[0] > 0:
                    if timer[0] < int(lapRecord4[0]):
                        lapRecord5[0] = lapRecord4[0]
                        lapRecord5[1] = lapRecord4[1]
                        lapRecord5[2] = lapRecord4[2]
                        lapRecord5[3] = lapRecord4[3]
                        lapRecord5[4] = lapRecord4[4]
                        if timer[0] < int(lapRecord3[0]):
                            lapRecord4[0] = lapRecord3[0]
                            lapRecord4[1] = lapRecord3[1]
                            lapRecord4[2] = lapRecord3[2]
                            lapRecord4[3] = lapRecord3[3]
                            lapRecord4[4] = lapRecord3[4]
                            if timer[0] < int(lapRecord2[0]):
                                lapRecord3[0] = lapRecord2[0]
                                lapRecord3[1] = lapRecord2[1]
                                lapRecord3[2] = lapRecord2[2]
                                lapRecord3[3] = lapRecord2[3]
                                lapRecord3[4] = lapRecord2[4]
                                if timer[0] < int(lapRecord[0]):
                                    lapRecord2[0] = lapRecord[0]
                                    lapRecord2[1] = lapRecord[1]
                                    lapRecord2[2] = lapRecord[2]
                                    lapRecord2[3] = lapRecord[3]
                                    lapRecord2[4] = lapRecord[4]
                                    lapRecord[0]=timer[0]
                                    lapRecord[1]=timer[3]
                                    lapRecord[2]=timer[4]
                                    lapRecord[3]=timer[5]
                                    lapRecord[4]=bikeSelect[0]
                                    newLapRecord = [True,BGREEN,'Your quickest lap ranked 1st!',1]
                                else:
                                    lapRecord2[0]=timer[0]
                                    lapRecord2[1]=timer[3]
                                    lapRecord2[2]=timer[4]
                                    lapRecord2[3]=timer[5]
                                    lapRecord2[4]=bikeSelect[0]
                                    if newLapRecord[3] > 2:
                                        newLapRecord[2] = 'Your quickest lap ranked 2nd'
                                        newLapRecord[3] = 2
                            else:
                                lapRecord3[0]=timer[0]
                                lapRecord3[1]=timer[3]
                                lapRecord3[2]=timer[4]
                                lapRecord3[3]=timer[5]
                                lapRecord3[4]=bikeSelect[0]
                                if newLapRecord[3] > 3:
                                    newLapRecord[2] = 'Your quickest lap ranked 3rd'
                                    newLapRecord[3] = 3
                        else:
                            lapRecord4[0]=timer[0]
                            lapRecord4[1]=timer[3]
                            lapRecord4[2]=timer[4]
                            lapRecord4[3]=timer[5]
                            lapRecord4[4]=bikeSelect[0]
                            if newLapRecord[3] > 4:
                                newLapRecord[2] = 'Your quickest lap ranked 4th'
                                newLapRecord[3] = 4
                    else:
                        lapRecord5[0]=timer[0]
                        lapRecord5[1]=timer[3]
                        lapRecord5[2]=timer[4]
                        lapRecord5[3]=timer[5]
                        lapRecord5[4]=bikeSelect[0]
                        if newLapRecord[3] > 5:
                            newLapRecord[2] = 'Your quickest lap ranked 5th'
                            newLapRecord[3] = 5

                timer[1] = timer[0]
                lap[5]='Valid'
                if timer[0] <= int(lapRecord[0]):
                    lap[6] = BGREEN
                else:
                    lap[6] = WHITE
            else:
                lap[5]='Invalid'
                lap[6]=LGREY
            if timer[0]-(timer[3]+timer[4]) <= int(lapRecord[3]):
                lap[9] = BGREEN
            else:
                lap[9] = WHITE
            lap[0]=timer[0]
            lap[1]=timer[3]
            lap[2]=timer[4]
            lap[3]=timer[5]
            lap[4]=bikeSelect[0]
            lapTimes.append(lap)
            lap = [0,0,0,0,0,0,WHITE,WHITE,WHITE,WHITE]
            timer[0]=0
            ghostCounter[5]=0
            ghostLap = []
            kers[2] = bikeSettings[7]
            cheatCheck[4]=0
            lapTimes[0]+=1
            if 10-lapTimes[0] >1:
                timer[8]=str(10-lapTimes[0]) + ' Laps Remaining'
            elif 10-lapTimes[0] ==1:
                timer[8]=str(10-lapTimes[0]) + ' Lap Remaining'
            else:
                timer[8]='On your Last Lap!'
            cheatCheck[1] = True
            displayTimeDif = 50
            cheatCheck[7] = WHITE
    else:
        cheatCheck[1]=False
        if timer[7]:
            timer[0]+=1
        if gameOver:
            moveUp = False
            kers[0] = False
            movespeed = [0,0,2,0]
            option[6]=0
            moveLeft = False
            moveRight = False
            gameOver = False
            option[8]=600
            soundTimer[0]=50
            displayLaptimes()
            position[0] = WINDOWWIDTH/2
            position[1] = WINDOWHEIGHT/2


    # move the player
    if moveDown:    # Braking
        bikeSettings[1] -= bikeSettings[3]
        accelerating[0] = False
        if movespeed[0] > 14:
            skiding[0]=True
            if sound:
                slideSound.play()
            if dirtPosition == 0:
                skiding[1] = recordSkid(skiding[1],4,skids,2)
        elif skiding[1] > 0:
            skiding[1] -= 1
        else:
            skiding[0] = False
            slideSound.stop()
    else:
        skiding[0] = False
        skiding[1] = 0
        slideSound.stop()

    if moveUp:    # Accelerate
        bikeSettings[1] += bikeSettings[2]
        accelerating[0] = True
    else:
        bikeSettings[1] -= bikeSettings[4]
        accelerating[0] = False

    if kers[0] == True: # Boost System
        movespeed[1] = bikeSettings[0]+kers[1]
        bikeSettings[1] += (bikeSettings[2]+kers[1])
        if kers[2]>0:
            kers[0]=True
            kers[2] -=1
            if movespeed[0] < movespeed[1]:
                skiding[0] = True
                if dirtPosition == 0:
                    kers[3] = recordSkid(kers[3],4,boost,1)
                    if sound:
                        wheelspinSound.play()
            else:
                kers[3] = 0
                wheelspinSound.stop()
        else:
            kers[0]=False
            kers[3]=0
            wheelspinSound.stop()
    else:
        movespeed[1] = bikeSettings[0]
        kers[3] = 0
        wheelspinSound.stop()

    if bikeSettings[1] >= bikeSettings[5] and movespeed[0] < movespeed[1]:# Change up gear
        movespeed[0] +=1
        bikeSettings[1] = 0
    elif bikeSettings[1] >= bikeSettings[5] and movespeed[0] >= movespeed[1]:# Accelerate Limiter
        bikeSettings[1] = bikeSettings[5]
    elif bikeSettings[1] < 0 and movespeed[0] == 0: # Braking limiter
        bikeSettings[1]=0
        movespeed[0]=0
    elif bikeSettings[1] <0:# Change down gears
        movespeed[0] -=1
        bikeSettings[1]=bikeSettings[5]

    if movespeed[0] > movespeed[1]:
        bikeSettings[1] -= bikeSettings[3]

    #Has Speed Changed?
    if movespeed[0] > 0:
        if changeSound != revSound[0]:
            if sound:
                playSound()

        changeSound = revSound[0]

    if movespeed[0] > 0:
        if accelerating[0] != accelerating[1]:
            if sound:
                playSound()

        accelerating[1] = accelerating[0]

    if movespeed[0] == bikeSettings[0] + kers[1] and bikeSettings[1] == bikeSettings[5]:
        if sound:
            revChannel.play(freewheelSound[3])
    elif movespeed[0] > bikeSettings[0]:
            revSound[0] =5

    if movespeed[0] == bikeSettings[0] and bikeSettings[1] == bikeSettings[5]:
        if sound:
            revChannel.play(freewheelSound[4])
    elif movespeed[0] > bikeSettings[0] // 1.5:
        revSound[0] =4
    elif movespeed[0] > bikeSettings[0] // 2:
        revSound[0] =3
        soundTimer[1] = 100
    elif movespeed[0] > bikeSettings[0] // 4:
        revSound[0] =2
    elif movespeed[0] > 0:
        revSound[0] =1
    else:
        if soundTimer[0] == 0:
            if sound:
                revChannel.play(tickoverSound)
        else:
            soundTimer[0] -= 1

    # Record ghost lap info
    if ghostCounter[0]:
        ghostPosition[0]=position[0]
        ghostPosition[1]=position[1]
        ghostPosition[2]=playerImage[0]
        ghostPosition[3]=degree
        ghostLap.append(ghostPosition)
        ghostPosition=[0,0,0,0,0]

    # draw the HUD onto screen
    if detail[0] > 1:
        pygame.draw.rect(windowSurface, BLACK,(WINDOWWIDTH-100,WINDOWHEIGHT-50, 50,((-bikeSettings[0]-1)*bikeSettings[5]/6)),2)
        pygame.draw.rect(windowSurface, BLACK,(WINDOWWIDTH-100,WINDOWHEIGHT-50-((bikeSettings[0]+1)*bikeSettings[5]/6)-2, 50,-kers[1]*10),2)
        pygame.draw.rect(windowSurface, BLUE,(WINDOWWIDTH-98,(WINDOWHEIGHT-50), 47,(-movespeed[0]*bikeSettings[5]-bikeSettings[1])/6))
        pygame.draw.rect(windowSurface, BLACK,(WINDOWWIDTH-100,WINDOWHEIGHT/10*2, 50,bikeSettings[7]+4),2)
        pygame.draw.rect(windowSurface, BGREEN,(WINDOWWIDTH-98,(WINDOWHEIGHT/10*2)+bikeSettings[7]+2, 47,-kers[2]))
        speedText = smallFont.render('Speed', True, WHITE,)
        boostText = smallFont.render('Boost', True, WHITE,)
        windowSurface.blit(speedText, (WINDOWWIDTH-96,WINDOWHEIGHT-64))
        windowSurface.blit(boostText, (WINDOWWIDTH-96,(WINDOWHEIGHT/10*2)+2))

    if detail[0] > 2:
        timeConversion = ["%.2f" %(timer[2]/60),int(lapRecord[0])/60,timer[2]/60]
        if timer[2] == 10000:
            timeConversion[0] = ' - '
        if newLapRecord[3] == 6:
            posText = 'Unranked'
        elif newLapRecord[3] == 5:
            posText = '5th'
        elif newLapRecord[3] == 4:
            posText = '4th'
        elif newLapRecord[3] == 3:
            posText = '3rd'
        elif newLapRecord[3] == 2:
            posText = '2nd'
        else:
            posText = '1st'

        best = normalFont.render('Best Lap - ' + posText, True, WHITE,)
        best1 = normalFont.render(timeConversion[0], True, WHITE,)
        best2 = normalFont.render("%.2f" %(timeConversion[1]), True, WHITE,)
        windowSurface.blit(best, (35,20))
        windowSurface.blit(best1, (35,40))
        windowSurface.blit(best2, (125,40))
        last = normalFont.render('Last Lap ' + "%.2f" %(round(timer[1]/60,2)), True, WHITE,)
        windowSurface.blit(last, (WINDOWWIDTH/2-50,20))
        remaining = normalFont.render(timer[8], True, WHITE,)
        windowSurface.blit(remaining, (WINDOWWIDTH/2-65,40))
        current = normalFont.render('Current Lap ' + "%.2f" %(round(timer[0]/60,2)), True, cheatCheck[7],)
        windowSurface.blit(current, (WINDOWWIDTH-200,20))
        section1 = smallFont.render('Section 1 ' + "%.2f" %(round(timer[3]/60,2)) + ' (' + "%.2f" %(round(int(lapRecord[1])/60,2)) + ')', True, WHITE,)
        windowSurface.blit(section1, (WINDOWWIDTH-160,40))
        section2 = smallFont.render('Section 2 ' + "%.2f" %(round(timer[4]/60,2)) + ' (' + "%.2f" %(round(int(lapRecord[2])/60,2))+ ')', True, WHITE,)
        windowSurface.blit(section2, (WINDOWWIDTH-160,50))
        section3 = smallFont.render('Section 3 ' + "%.2f" %(round(timer[5]/60,2)) + ' (' + "%.2f" %(round(int(lapRecord[3])/60,2)) + ')', True, WHITE,)
        windowSurface.blit(section3, (WINDOWWIDTH-160,60))

    if displayTimeDif > 0:
        if cheatCheck[4]>cheatCheck[5]:
            cheatCheck[6] = 'Invalid Lap - '
            cheatCheck[7] = RED
        if timer[6] > 0:
            dif = smallFont.render(cheatCheck[6] + "%.2f" %(round(timer[6]/60,2)), True, RED,)
            displayTimeDif -= 1
        else:
            dif = smallFont.render(cheatCheck[6] + "%.2f" %(round(timer[6]/60,2)), True, BGREEN,)
            displayTimeDif -= 1
        windowSurface.blit(dif, (WINDOWWIDTH/2-50,WINDOWHEIGHT/2-30))

    # draw the window onto the screen
    framerate()
    pygame.display.update()
