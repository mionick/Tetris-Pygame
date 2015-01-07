import pygame
from Constants import *
from button import Button


items = []
items.append(Button(button_width, button_height, "Classic", GameState.PLAYING))
items.append(Button(button_width, button_height, "Four-Way"))
items.append(Button(button_width, button_height, "Highscores"))
items.append(Button(button_width, button_height, "Exit", GameState.EXIT))

space = 10

num_items = len(items)
cursor_pos = 0

cursor_image = pygame.Surface((button_width+10, button_height+10), pygame.SRCALPHA)
cursor_color = 255, 255, 255

color1 = (200, 255, 200)
color2 = (0, 255, 0)

time = 0
direction = 1

flashing_period = 800.0

def update_cursor(color):
    pygame.draw.line(cursor_image, color, (0, 0), (0, button_height/2+5), 15)
    pygame.draw.line(cursor_image, color, (0, 0), (button_width/2+5, 0), 15)
    pygame.draw.line(cursor_image, color, (button_width+10, button_height/2+5), (button_width+10, button_height+10), 15)
    pygame.draw.line(cursor_image, color, (button_width/2+5, button_height+10), (button_width+10, button_height+10), 15)

def cursor_pos_down():
    global cursor_pos
    cursor_pos = (cursor_pos + 1) % num_items

def cursor_pos_up():
    global cursor_pos
    cursor_pos = (cursor_pos - 1) % num_items

def lerp(milliseconds):
    global time
    global direction
    global cursor_color
    time += direction*milliseconds
    if time > flashing_period:
        direction = -1
        time = flashing_period
    elif time < 0:
        direction = 1
        time = 0
    cursor_color = ((color1[0]*time/flashing_period + (1-time/flashing_period)*color2[0]), (color1[1]*time/flashing_period + (1-time/flashing_period)*color2[1]), (color1[2]*time/flashing_period + (1-time/flashing_period)*color2[2]))


def update(milliseconds):
    lerp(milliseconds)
    update_cursor(cursor_color)
    

def render(screen, x=0, y=0):
    for i in range(num_items):
        screen.blit(items[i].surface, (x, y+i*(button_height+space)))
    update_cursor(cursor_color)
    screen.blit(cursor_image, (x-5, y+cursor_pos*(button_height+space)-5))


    
    
        







