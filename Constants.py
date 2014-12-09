##CONSTANTS
import pygame
color = [ (0,0,0),
          (0,0,255),
          (0,255,0),
          (0,255,255),
          (255,0,0),
          (255,0,255),
          (255,255,0),
          (255,255,255)]

BLOCKSIZE = 25

blocks = []

for i in range(8):
    blocks.append(pygame.Surface((BLOCKSIZE, BLOCKSIZE)))
    blocks[i].fill(color[i])
    pygame.draw.rect(blocks[i], (0,0,0),(0,0,BLOCKSIZE, BLOCKSIZE), 2)#self.width = 2
pygame.draw.rect(blocks[0], (30,30,30),(0,0,BLOCKSIZE, BLOCKSIZE), 1)#self.width = 2
#blocks[0] is background block
#blocks[8] is shadow for drop block
blocks.append(pygame.Surface((BLOCKSIZE, BLOCKSIZE)))
blocks[8].fill((12, 12, 12))
pygame.draw.rect(blocks[8], (30,30,30),(0,0,BLOCKSIZE, BLOCKSIZE), 1)

anchors = [(1, 1), (1, 0), (0, 1), (1, 1)]
lineanchors = [(0, 2), (1, 0), (0, 1), (2, 0)]
