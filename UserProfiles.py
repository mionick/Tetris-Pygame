#Maps from logical buttons to pygame inputs
import pygame
buttons = []
def load_profile(profile = None):
    global buttons
    if profile == "colin":
        buttons.append(set([pygame.K_ESCAPE]))  #CLOSE
        buttons.append(set([pygame.K_LEFT]))    #LEFT
        buttons.append(set([pygame.K_RIGHT]))   #RIGHT
        buttons.append(set([pygame.K_UP, pygame.K_z]))      #ROTATE
        buttons.append(set([pygame.K_DOWN]))    #DOWN
        buttons.append(set([pygame.K_SPACE]))   #DROP
        buttons.append(set([pygame.K_y]))       #ACCEPT
        buttons.append(set([pygame.K_RSHIFT]))  #STORE
        buttons.append(set([pygame.K_LSHIFT]))  #PAUSE
    else:
        buttons.append(set([pygame.K_ESCAPE]))  #CLOSE
        buttons.append(set([pygame.K_LEFT]))    #LEFT
        buttons.append(set([pygame.K_RIGHT]))   #RIGHT
        buttons.append(set([pygame.K_UP]))      #ROTATE
        buttons.append(set([pygame.K_DOWN]))    #DOWN
        buttons.append(set([pygame.K_SPACE]))   #DROP
        buttons.append(set([pygame.K_y]))       #ACCEPT
        buttons.append(set([pygame.K_RSHIFT]))  #STORE
        buttons.append(set([pygame.K_LSHIFT]))  #PAUSE
    
    
