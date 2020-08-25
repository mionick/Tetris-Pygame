##CONSTANTS
import pygame
from enum import Enum


class GameState(Enum):
    MENU = 0
    PLAYING = 1
    PLAYAGAIN = 2
    PAUSED = 3
    EXIT = 4


BOARD_BOARDER = 10
BLOCKSIZE = 30
WIDTH = 10
HEIGHT = 22
P_WIDTH = (WIDTH+12)*BLOCKSIZE
P_HEIGHT = (HEIGHT+2)*BLOCKSIZE

fuschia = (128, 0, 128)
shadowColor = 40

color = [ fuschia, #(0,0,0),
          (0,0,255),
          (0,255,0),
          (0,255,255),
          (255,0,0),
          (255,0,255),
          (255,255,0),
          (255,255,255)]


blocks = []

for i in range(8):
    blocks.append(pygame.Surface((BLOCKSIZE, BLOCKSIZE)))
    blocks[i].fill(color[i])
    pygame.draw.rect(blocks[i], (0,0,0),(0,0,BLOCKSIZE, BLOCKSIZE), 2)# self.width = 2
pygame.draw.rect(blocks[0], (30,30,30),(0,0,BLOCKSIZE, BLOCKSIZE), 1)# self.width = 2
# blocks[0] is background block
# blocks[8] is shadow for drop block
# 9 is used when dont want to maintain colors of placed pieces
blocks.append(pygame.Surface((BLOCKSIZE, BLOCKSIZE)))
blocks[8].fill((shadowColor, shadowColor, shadowColor))
blocks.append(pygame.Surface((BLOCKSIZE, BLOCKSIZE)))
blocks[9].fill((0, 0, 0))
blocks.append(pygame.Surface((BLOCKSIZE, BLOCKSIZE), pygame.SRCALPHA))
blocks[10].fill((0, 0, 0, 128))
blocks.append(pygame.Surface((BLOCKSIZE, BLOCKSIZE), pygame.SRCALPHA))
blocks[11].fill((255, 255, 255, 90))
pygame.draw.rect(blocks[8], (30,30,30),(0,0,BLOCKSIZE, BLOCKSIZE), 1)

anchors = [(1, 1), (1, 0), (0, 1), (1, 1)]
lineanchors = [(0, 2), (1, 0), (0, 1), (2, 0)]


#MENU STUFF
button_width = 250
button_height = 50
