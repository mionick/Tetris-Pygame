import pygame
pygame.font.init()


font40 = pygame.font.SysFont("monospace", 40)
font50 = pygame.font.SysFont("monospace", 50)

#size in pixels


class Button():
    def __init__(self, width, height, label, attribute = None, thickness = 5):
        self.surface = pygame.Surface((width, height))
        self.surface.fill((10, 10, 10))
        pygame.draw.rect(self.surface, (30, 30, 30), (0,0,width, height), thickness)
        self.width = width
        self.height = height

        text = font40.render(label, 1, (255, 255, 255))
        
        self.surface.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

        self.attribute = attribute
        

