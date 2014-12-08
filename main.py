import sys, os
from enum import Enum
from GameObjects import *
from pygame import *
import InputHandler

pygame.init()
pygame.key.set_repeat(50, 50)

##Board will be 10 wide by 24 high.
##each block will be 15*15 pixels for now.

#CONSTANTS===================================================
WIDTH = 10
HEIGHT = 22
class GameState(Enum):
    start = 0
    playing = 1
    playagain = 2
    paused = 3


#GLOBAL VARIABLES============================================

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
titlefont = pygame.font.SysFont("monospace", 20)
linefont = pygame.font.SysFont("monospace", 50)

# render text
label = myfont.render(str(FPS), 1, (255,255,255))



#input array
#[LEFT, RIGHT, UP, DOWN, SPACE, Y, RSHIFT, LSHIFT]
userInput = [0,0,0,0,0,0,0,0]
InputHandler.userInput = userInput

pygame.time.set_timer(pygame.USEREVENT, 10)

#PLAYING THINGS=============================================
current_state = GameState.playing
switched = False


sinceYUpdate = 0

#PLAYAGAIN THINGS===========================================
playagaintext = myfont.render("Play again? (Y/N)", 1, (255,255,255))
pausedtext = titlefont.render("PAUSED", 1, (255,255,255))


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
            if event.key == pygame.K_LSHIFT:
                userInput[7] = 1
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                userInput[0] = 0
            if event.key == pygame.K_RIGHT:
                userInput[1] = 0
            if event.key == pygame.K_UP:
                userInput[2] = 0
            if event.key == pygame.K_DOWN:
                userInput[3] = 0
            if event.key == pygame.K_SPACE:
                userInput[4] = 0
            if event.key == pygame.K_y:
                userInput[5] = 0
            if event.key == pygame.K_RSHIFT:
                userInput[6] = 0
            if event.key == pygame.K_LSHIFT:
                userInput[7] = 0
            
#END Get Events 


#MAIN LOOP======================================================
while running:
    milliseconds = clock.tick(FPS+1)
    seconds = milliseconds / 1000.0 #seconds since last frame
    sinceYUpdate += seconds

    
    GetEvents()
    InputHandler.update()
    
    #frame business
    frames+=1
    if (pygame.time.get_ticks() - startTime >= 1000):
        actualFPS = frames
        frames=0
        startTime = pygame.time.get_ticks()
        label = myfont.render(str(actualFPS), 1, (255,255,255))
    
    if (current_state == GameState.playing):

    #UPDATE===============================================

    #PLAYING STATE====================================
    
        if board.active == None:
            board.create()
            switched = False
            sinceYUpdate = 0

        ##Switching with Stored
        if (InputHandler.store_button and not switched):
            board.store()
            switched = True
        #Drop piece by one
        if (sinceYUpdate >= 1.0/board.fall_rate):
            board.actIncY()
            sinceYUpdate = 0
        #Or move left/right
        if (InputHandler.right_button or InputHandler.left_button):
            board.actMoveX(InputHandler.right_button - InputHandler.left_button)
        #Drop piece
        if (InputHandler.drop_button):
            board.actDrop()
        #Moving down
        if (InputHandler.down_button):
            board.actIncY()
        #Rotate Piece
        if (InputHandler.rotate_button):
            board.actRotate()
        if (InputHandler.pause_button):
            current_state = GameState.paused
            
        board.update()
        if board.gameOver:
            current_state = GameState.playagain
            
    elif (current_state == GameState.playagain):#END OF PLAYING STATE
        if InputHandler.accept_button:
            current_state = GameState.playing
            board.clear()
    elif (current_state == GameState.paused):
        if InputHandler.pause_button:
            current_state= GameState.playing
        
    #RENDER===============================================
    screen.fill((0,0,0))
    if current_state == GameState.playing:
        board.render(screen, 3, 1)
    elif current_state == GameState.playagain:
        board.render(screen, 3, 1)
        screen.blit(playagaintext, (10,9*BLOCKSIZE))
    elif current_state == GameState.paused:
        board.render(screen, 3, 1)
        screen.blit(pausedtext, (10,9*BLOCKSIZE))
        

        
    screen.blit(label, (10, 10))
    pygame.display.flip()
#END MAIN LOOP (running)

pygame.quit()
sys.exit()


