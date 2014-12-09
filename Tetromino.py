#Tetromino
from Constants import *
import random
random.seed()

#Each tetromino will be specified by a matrix of ones and zeroes, representing it's shape.
class Tetromino():
##    x, y
##    kind
##    shape
##    width
##    height
##    anchor
##    color
##    orientation
    
    def __init__(self, x, y, kind=None):
        self.kind = random.randint(1, 7)
        if (kind != None):
            self.kind = kind
        
        if self.kind == 1:
            #Left L shape
            self.shape = [[1, 0, 0],
                     [1, 1, 1]]
            self.width = 3
            self.height = 2
            self.anchor = (1, 1)
        elif self.kind == 2:
            #Right L shape
            self.shape = [[0, 0, 1],
                     [1, 1, 1]]
            self.width = 3
            self.height = 2
            self.anchor = (1, 1)
        elif self.kind == 3:
            #Square
            self.shape = [[1, 1],
                     [1, 1]]
            self.width = 2
            self.height = 2
            self.anchor = (1, 1)#This actually makes it worse for the square. maybe don't use.
        elif self.kind == 4:
            #Line
            self.shape = [[1, 1, 1, 1]]
            self.width = 4
            self.height = 1
            self.anchor = (0, 0)#makes sense for line? probably won't use
        elif self.kind == 5:
            #s shape
            self.shape = [[0, 1, 1],
                     [1, 1, 0]]
            self.width = 3
            self.height = 2
            self.anchor = (1, 1)
        elif self.kind == 6:
            #z shape
            self.shape = [[1, 1, 0],
                     [0, 1, 1]]
            self.width = 3
            self.height = 2
            self.anchor = (1, 1)
        else:
            #T shape

            self.shape = [[0, 1, 0],
                     [1, 1, 1]]
            self.width = 3
            self.height = 2
            self.anchor = (1, 1)

        self.color = color[self.kind]
        self.orientation = 0

        self.x = x
        self.y = y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def addY(self, y):
        self.y += y

    def setPos(self, x, y):
        self.x = x
        self.y = y
        
    def rotate(self):
        self.width, self.height = self.height, self.width
        self.shape = list(zip(*self.shape[::-1]))
        nextanchor = anchors[(self.orientation+1) % 4]
        self.orientation = (self.orientation+1) % 4
        if(self.kind != 3 and self.kind != 4):
            self.x+=self.anchor[1]-nextanchor[1]
            self.y+=self.anchor[0]-nextanchor[0]
            self.anchor = nextanchor
        if(self.kind == 4):
            nextanchor = lineanchors[(self.orientation+1) % 4]
            self.x-=self.anchor[1]-nextanchor[1]
            self.y-=self.anchor[0]-nextanchor[0]
            self.anchor = nextanchor

    def clone(self):
        clone = Tetromino(self.x, self.y, self.kind)
        clone.shape = self.shape
        clone.width = self.width
        clone.height = self.height
        clone.anchor = self.anchor
        clone.orientation = self.orientation
        return clone


    def update(self, x, y=0):
        self.y +=y
        self.x +=x

    def render(self, screen, offX, offY):
        for i in range(len(self.shape)):       #For each row
            for j in range(len(self.shape[i])):#For each cell in that row
                if(self.shape[i][j] == 1):
                    screen.blit(blocks[self.kind], ((j+self.x +offX)*BLOCKSIZE, (i + self.y +offY)*BLOCKSIZE))

