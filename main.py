import sys, os
from Board import Board
import pygame
import InputHandler
from Constants import *
from UserProfiles import load_profile, buttons
import Menu

import win32api
import win32con
import win32gui

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('This is a log message.')

#Initializing================================================
load_profile()

pygame.init()

# Set window transparency color
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuschia), 100, win32con.LWA_COLORKEY)




#GLOBAL VARIABLES============================================

screen = pygame.display.set_mode(((WIDTH+12)*BLOCKSIZE, (HEIGHT+2)*BLOCKSIZE), pygame.SRCALPHA)

opacity_screen20 = pygame.Surface(((WIDTH+12)*BLOCKSIZE, (HEIGHT+2)*BLOCKSIZE), pygame.SRCALPHA)
#opacity_screen20.fill((0,0,0,100))
opacity_screen20.fill(fuschia)
#SPRITES=====================================================

board = Board(WIDTH, HEIGHT)

#monitor the frame rate=====================
clock = pygame.time.Clock()
running = True
FPS = 60
actualFPS = 60
anti_alias = 0
frames = 0
startTime = pygame.time.get_ticks()

font15 = pygame.font.SysFont("monospace", 15)
font20 = pygame.font.SysFont("monospace", 20)
font30 = pygame.font.SysFont("monospace", 30)
font50 = pygame.font.SysFont("monospace", 50)

# render text
fps_image = font15.render(str(FPS), anti_alias, (255,255,255))



#input array
#[LEFT, RIGHT, ROTATE_C, ROTATE_CC, DOWN, DROP, ACCEPT, STORE, PAUSE]
userInput = [0,0,0,0,0,0,0,0,0]
InputHandler.userInput = userInput

pygame.time.set_timer(pygame.USEREVENT, 10)

#PLAYING THINGS=============================================
current_state = GameState.MENU
switched = False


sinceYUpdate = 0

#PLAYAGAIN THINGS===========================================
playagain_text = font30.render("Play again? (Y/N)", 1, (255,255,255), (0,0,0))
paused_text = font20.render("PAUSED", 1, (255,255,255))


#FUNCTION DEFINITIONS=======================================
def GoToMenu():
    global current_state
    board.clear()
    current_state = GameState.MENU

def NewGame():
    global current_state
    board.clear()
    current_state = GameState.PLAYING

def GetEvents():
    global running

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key in buttons[0]:
                GoToMenu() # user pressed ESC
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
            if event.key in buttons[10]:#PAUSE
                userInput[8] = 1
                
        if event.type == pygame.KEYUP:
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
            if event.key in buttons[10]:#PAUSE
                userInput[8] = 0
            
#END Get Events

#RENDER FUNCTION + VARIABLES
points_image = font20.render("Score:" + str(board.points), anti_alias, (255, 255, 255))
level_image1 = font20.render("Level:", anti_alias, (255, 255, 255))
level_image2 = font50.render(str(board.level), anti_alias, (255, 255, 255))
lines_image = font20.render("lines: " + str(board.lines_total), anti_alias, (255, 255, 255))
storage_image = font20.render("Stored:", anti_alias, (255, 255, 255))
next_image = font20.render("Next:", anti_alias, (255, 255, 255))

def render_playing_screen():
    board.render(screen, 6, 1)
    level_image2 = font50.render(str(board.level), anti_alias, (255, 255, 255))
    points_image = font20.render("Score:" + str(board.points), anti_alias, (255, 255, 255))
    lines_image = font20.render("lines: " + str(board.lines_total), anti_alias, (255, 255, 255))
    
    screen.blit(level_image1, (BLOCKSIZE, BLOCKSIZE))
    screen.blit(level_image2, (BLOCKSIZE, 2*BLOCKSIZE))
    screen.blit(points_image, (BLOCKSIZE, 4*BLOCKSIZE))
    screen.blit(lines_image, (BLOCKSIZE, 5*BLOCKSIZE))
    screen.blit(next_image, (17*BLOCKSIZE, BLOCKSIZE))

    screen.blit(storage_image, (BLOCKSIZE, 19*BLOCKSIZE)) 
    if board.stored != None:
        board.stored.render(screen, 1-board.stored.x, 20-board.stored.y)
    board.render_next(screen, 17, 2)



beard_image = pygame.image.load(os.path.join(os.path.curdir, "assets", "Tetris.png"))#"beard.bmp"))
beard_image.convert()



def render_menu():
    screen.blit(beard_image, (P_WIDTH/2 - beard_image.get_width()/2,BLOCKSIZE))
    Menu.render(screen, P_WIDTH/2 - button_width/2, 300)

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
        fps_image = font15.render(str(actualFPS), anti_alias, (255,255,255))

    #UPDATE===============================================
    #MENU STATE======================================
    if (current_state == GameState.MENU):
        Menu.update(milliseconds)

        if (InputHandler.rotate_button != 0):
            Menu.cursor_pos_up()
        if (InputHandler.down_button):
            Menu.cursor_pos_down()
        if (InputHandler.accept_button or InputHandler.drop_button):
            current_state = Menu.items[Menu.cursor_pos].attribute

    elif (current_state == GameState.PLAYING):
    #PLAYING STATE====================================
    
        if board.active == None:
            board.create()
            switched = False
            sinceYUpdate = 0

        if not board.inAnimation:
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
            current_state = GameState.PAUSED
            
        if board.gameOver:
            current_state = GameState.PLAYAGAIN

    #PLAYAGAIN STATE=======================================
    elif (current_state == GameState.PLAYAGAIN):
        if InputHandler.accept_button:
            NewGame()
        if InputHandler.reject_button:
            GoToMenu()
    #PAUSED STATE=========================================
    elif (current_state == GameState.PAUSED):
        if InputHandler.pause_button:
            current_state= GameState.PLAYING
    #EXIT=================================================
    elif (current_state == GameState.EXIT):
        running = False
        
    #RENDER===============================================
    screen.fill(fuschia)
    if (current_state == GameState.MENU):
        render_menu()
    elif current_state == GameState.PLAYING:
        render_playing_screen()
    elif current_state == GameState.PLAYAGAIN:
        render_playing_screen()
        screen.blit(playagain_text, (10,9*BLOCKSIZE))
    elif current_state == GameState.PAUSED:
        render_playing_screen()
        screen.blit(paused_text, (10,9*BLOCKSIZE))

        

        
    screen.blit(fps_image, (10, 10))
    pygame.display.flip()
#END MAIN LOOP (running)

pygame.quit()
sys.exit()




#TODO
#Highscores
