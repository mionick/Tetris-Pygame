#Maps from logical buttons to pygame inputs
import pygame
buttons = []
def load_profile(profile = None):
    global buttons
    if profile == "colin":
        buttons.append(set([pygame.K_ESCAPE]))  #CLOSE
        buttons.append(set([pygame.K_LEFT]))    #LEFT
        buttons.append(set([pygame.K_RIGHT]))   #RIGHT
        buttons.append(set([pygame.K_UP, pygame.K_x]))      #ROTATE
        buttons.append(set([pygame.K_z]))      #ROTATE_CC
        buttons.append(set([pygame.K_DOWN]))    #DOWN
        buttons.append(set([pygame.K_SPACE]))   #DROP
        buttons.append(set([pygame.K_y, pygame.K_RETURN]))       #ACCEPT
        buttons.append(set([pygame.K_RSHIFT]))  #STORE
        buttons.append(set([pygame.K_LSHIFT]))  #PAUSE
        buttons.append(set([pygame.K_n, pygame.K_BACKSPACE]))  #Reject
    else:
        buttons.append(set([pygame.K_ESCAPE]))  #CLOSE
        buttons.append(set([pygame.K_LEFT]))    #LEFT
        buttons.append(set([pygame.K_RIGHT]))   #RIGHT
        buttons.append(set([pygame.K_UP, pygame.K_x]))      #ROTATE
        buttons.append(set([pygame.K_z]))      #ROTATE_CC
        buttons.append(set([pygame.K_DOWN]))    #DOWN
        buttons.append(set([pygame.K_SPACE]))   #DROP
        buttons.append(set([pygame.K_y, pygame.K_RETURN]))       #ACCEPT
        buttons.append(set([pygame.K_RSHIFT, pygame.K_c]))  #STORE
        buttons.append(set([pygame.K_LSHIFT]))  #PAUSE
        buttons.append(set([pygame.K_n, pygame.K_BACKSPACE]))  #Reject
    
    
