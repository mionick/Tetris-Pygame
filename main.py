import sys, os
from enum import Enum
from Board import Board
import pygame
import InputHandler
from Constants import *
from UserProfiles import load_profile, buttons

#Initializing================================================
load_profile("colin")

pygame.init()



#CONSTANTS===================================================
WIDTH = 10
HEIGHT = 22
class GameState(Enum):
    start = 0
    playing = 1
    playagain = 2
    paused = 3


#GLOBAL VARIABLES============================================

screen = pygame.display.set_mode(((WIDTH+7)*BLOCKSIZE, (HEIGHT+2)*BLOCKSIZE))
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

font15 = pygame.font.SysFont("monospace", 15)
font20 = pygame.font.SysFont("monospace", 20)
font50 = pygame.font.SysFont("monospace", 50)

# render text
fps_image = font15.render(str(FPS), 1, (255,255,255))



#input array
#[LEFT, RIGHT, ROTATE_C, ROTATE_CC, DOWN, DROP, ACCEPT, STORE, PAUSE]
userInput = [0,0,0,0,0,0,0,0]
InputHandler.userInput = userInput

pygame.time.set_timer(pygame.USEREVENT, 10)

#PLAYING THINGS=============================================
current_state = GameState.playing
switched = False


sinceYUpdate = 0

#PLAYAGAIN THINGS===========================================
playagain_text = font15.render("Play again? (Y/N)", 1, (255,255,255))
paused_text = font20.render("PAUSED", 1, (255,255,255))


#FUNCTION DEFINITIONS=======================================
def GetEvents():
    global running

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key in buttons[0]:
                running = False # user pressed ESC
            if event.key in buttons[1]:#LEFT
                userInput[0] = 1
            if event.key in buttons[2]:#RIGHT
                userInput[1] = 1
            if event.key in buttons[3]:#ROTATE_C
                userInput[2] = 1
            if event.key in buttons[4]:#ROTATE_CC
                userInput[2] = -1
            if event.key in buttons[5]:#DOWN
                userInput[3] = 1
            if event.key in buttons[6]:#DROP
                userInput[4] = 1
            if event.key in buttons[7]:#ACCEPT
                userInput[5] = 1
            if event.key in buttons[8]:#SWITCHPIECE
                userInput[6] = 1
            if event.key in buttons[9]:#PAUSE
                userInput[7] = 1
                
        if event.type == pygame.KEYUP:
            if event.key in buttons[0]:
                running = False # user pressed ESC
            if event.key in buttons[1]:#LEFT
                userInput[0] = 0
            if event.key in buttons[2]:#RIGHT
                userInput[1] = 0
            if event.key in buttons[3]:#ROTATE_C
                userInput[2] = 0
            if event.key in buttons[4]:#ROTATE_CC
                userInput[2] = 0
            if event.key in buttons[5]:#DOWN
                userInput[3] = 0
            if event.key in buttons[6]:#DROP
                userInput[4] = 0
            if event.key in buttons[7]:#ACCEPT
                userInput[5] = 0
            if event.key in buttons[8]:#SWITCHPIECE
                userInput[6] = 0
            if event.key in buttons[9]:#PAUSE
                userInput[7] = 0
            
#END Get Events

#RENDER FUNCTION + VARIABLES
points_image = font20.render("Score:" + str(board.points), 1, (255, 255, 255))
level_image1 = font20.render("Level:", 1, (255, 255, 255))
level_image2 = font50.render(str(board.level), 1, (255, 255, 255))
lines_image = font20.render("lines: " + str(board.lines_total), 1, (255, 255, 255))
storage_image = font20.render("Stored:", 1, (255, 255, 255))

def render_screen():
    board.render(screen, 6, 1)
    level_image2 = font50.render(str(board.level), 1, (255, 255, 255))
    points_image = font20.render("Score:" + str(board.points), 1, (255, 255, 255))
    lines_image = font20.render("lines: " + str(board.lines_total), 1, (255, 255, 255))
    
    screen.blit(level_image1, (BLOCKSIZE, BLOCKSIZE))
    screen.blit(level_image2, (BLOCKSIZE, 2*BLOCKSIZE))
    screen.blit(points_image, (BLOCKSIZE, 4*BLOCKSIZE))
    screen.blit(lines_image, (BLOCKSIZE, 5*BLOCKSIZE))

    screen.blit(storage_image, (BLOCKSIZE, 19*BLOCKSIZE)) 
    if board.stored != None:
        board.stored.render(screen, 1-board.stored.x, 20-board.stored.y)
    
    


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
        fps_image = font15.render(str(actualFPS), 1, (255,255,255))
    
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
            continue
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
        if (InputHandler.rotate_button != 0):
            board.actRotate(InputHandler.rotate_button)
        if (InputHandler.pause_button):
            current_state = GameState.paused
            
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
        render_screen()
    elif current_state == GameState.playagain:
        render_screen()
        screen.blit(playagain_text, (10,9*BLOCKSIZE))
    elif current_state == GameState.paused:
        render_screen()
        screen.blit(paused_text, (10,9*BLOCKSIZE))
        

        
    screen.blit(fps_image, (10, 10))
    pygame.display.flip()
#END MAIN LOOP (running)

pygame.quit()
sys.exit()


