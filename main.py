import sys, os
from GameObjects import *
from pygame import *

pygame.init()
pygame.key.set_repeat(50, 50)

##Board will be 10 wide by 24 high.
##each block will be 15*15 pixels for now.

#CONSTANTS===================================================
WIDTH = 10
HEIGHT = 22


#GLOBAL VARIABLES============================================
dropPS = 5

screen = pygame.display.set_mode(((WIDTH+3)*BLOCKSIZE, (HEIGHT+2)*BLOCKSIZE))
#ball = pygame.image.load(os.path.join(os.path.curdir, "assets", "ball.gif"))

#SPRITES=====================================================

board = Board(WIDTH, HEIGHT)

#monitor the frame rate=====================
clock = pygame.time.Clock()
running = True
FPS = 60
actualFPS = 60
frames = 0
startTime = pygame.time.get_ticks()

myfont = pygame.font.SysFont("monospace", 15)

# render text
label = myfont.render(str(FPS), 1, (255,255,255))



#input array
#[LEFT, RIGHT, UP, DOWN]
userInput = [0,0,0,0,0,0,0]

pygame.time.set_timer(pygame.USEREVENT, 10)

#PLAYING THINGS=============================================
sinceRotateUpdate = 0
sinceDropUpdate = 0
sinceYUpdate = 0
sinceCollisionUpdate = 0
rotateUpdateRate = 6
dropUpdateRate = 6
yUpdateRate = 2
##CHANGE COLLISION UPDATE RATE
collisionUpdateRate = max(rotateUpdateRate, dropUpdateRate, yUpdateRate)
playing = True
active = None
stored = None
switched = False
#PLAYAGAIN THINGS===========================================
playagaintext = myfont.render("Play again? (Y/N))", 1, (255,255,255))


#FUNCTION DEFINITIONS=======================================
def GetEvents():
    global running

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False # user pressed ESC
            if event.key == pygame.K_LEFT:
                userInput[0] = 1
            if event.key == pygame.K_RIGHT:
                userInput[1] = 1
            if event.key == pygame.K_UP:
                userInput[2] = 1
            if event.key == pygame.K_DOWN:
                userInput[3] = 1
            if event.key == pygame.K_SPACE:
                userInput[4] = 1
            if event.key == pygame.K_y:
                userInput[5] = 1
            if event.key == pygame.K_RSHIFT:
                userInput[6] = 1
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                userInput[0] = 0
            if event.key == pygame.K_RIGHT:
                userInput[1] = 0
            if event.key == pygame.K_DOWN:
                userInput[3] = 0
#END Get Events 


#MAIN LOOP======================================================
while running:
    milliseconds = clock.tick(FPS+1)
    seconds = milliseconds / 1000.0 #seconds since last frame

    
    GetEvents()
    
    #frame business
    frames+=1
    if (pygame.time.get_ticks() - startTime >= 1000):
        actualFPS = frames
        frames=0
        startTime = pygame.time.get_ticks()
        label = myfont.render(str(actualFPS), 1, (255,255,255))
    
    if(playing):
        sinceDropUpdate += seconds
        sinceYUpdate += seconds
        sinceRotateUpdate += seconds
        sinceCollisionUpdate += seconds
    #UPDATE===============================================

    #PLAYING STATE====================================
    
        if board.active == None:
            board.create()
            userInput[6] = 0 ##RSHIFT
            switched = False
        #Drop piece by one
        if (sinceYUpdate > (1.0/yUpdateRate)):
            board.actIncY()
            sinceYUpdate = 0
        #Or move left/right
        elif (userInput[0] or userInput[1]):#sinceXUpdate > (1.0/xUpdateRate)):
            board.actMoveX(userInput[1]-userInput[0])
            userInput[0] = 0
            userInput[1] = 0
        #Drop Piece LOGIC IS FLAWED. THIS INPUT THING SUCKS timing
        if (sinceDropUpdate < (1.0/dropUpdateRate)):
            userInput[4] = 0
        if (userInput[4] == 1):
            board.actDrop()
            userInput[4] = 0
            sinceDropUpdate = 0
        #Moving down
        if userInput[3]:
            board.actIncY()
            userInput[3] = 0
        #Rotate Piece
        if (sinceRotateUpdate > 1.0/rotateUpdateRate):
            if userInput[2]:
                board.actRotate()
                userInput[2] = 0
            sinceRotateUpdate = 0

        ##Switching with Stored Logic is missing
        if (userInput[6]):
            board.store()
            switched = True
            userInput[6] = 0
            
        board.update()
        if board.gameOver:
            playing = False
            playagain = True
            userInput[5] = 0
    elif playagain:#END OF PLAYING STATE
        if userInput[5]:
            playing = True
            playagian = False
            stored = None
            board.clear()
            userInput[5]=0
            userInput[4]=0
    else:
        pass
    #RENDER===============================================
    screen.fill((0,0,0))
    if playing:
        board.render(screen, 3, 1)
    elif playagain:
        screen.blit(playagaintext, (10,9*BLOCKSIZE))
        

        
    screen.blit(label, (10, 10))
    pygame.display.flip()
#END MAIN LOOP (running)

pygame.quit()
sys.exit()


