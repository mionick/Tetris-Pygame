import pygame
pygame.font.init()
import random

random.seed()

##CONSTANTS
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


class Board():
    board = []
    gameOver = False
    active = None
    shadow = None
    stored = None
    lines_total = 0
    linefont = pygame.font.SysFont("monospace", 50)
    line_image = None

    ##BOARD METHODS==================================================================
    
    def __init__(self, width, height):
        Board.board = [[0]*width for i in range(height)]
        self.width = width
        self.height = height
        Board.line_image = Board.linefont.render(str(Board.lines_total),1, (255,255,255))


    def clear(self):
        Board.board = [[0]*self.width for i in range(self.height)]
        Board.active = None
        Board.stored = None
        Board.gameOver = False

    def render(self, screen, offX, offY):
        for i in range(len(Board.board)):       #For each row
            for j in range(len(Board.board[i])):#For each cell in that row
                block = blocks[Board.board[i][j]]
                screen.blit(block, ((j + offX)*BLOCKSIZE, (i + offY)*BLOCKSIZE))
        if Board.active != None:
            Board.shadow.render(screen, offX, offY)
            Board.active.render(screen, offX, offY)
        if Board.stored != None:
            Board.stored.render(screen, -Board.stored.x, -Board.stored.y)

        #Render Num of lines on screen:
        screen.blit(Board.line_image, (BLOCKSIZE/2, 12*BLOCKSIZE))

        
        
    def update(self):
        #clears Lines
        count = 0
        for i in Board.board:
            if all(i):
                Board.board.remove(i)
                count+=1
        for i in range(count):
            Board.board.insert(0, [0]*self.width)
        Board.lines_total += count
        if count > 0:
            Board.line_image = Board.linefont.render(str(Board.lines_total),1, (255,255,255))

    def collideBorderX(self, tet=None):
        #returns 1 for left, 2 for right, 0 for neither
        #Defaults to using active
        if tet == None:
            tet = Board.active
            
        side = 0
        if tet.x < 0:
            side = 1
        if tet.x + tet.width > self.width:
            side = 2
        return side


    def collideY(self, tet=None):
        #Check if shape has fallen on the bottom of the board
        if tet == None:
            tet = Board.active
            
        #did active hit the bottom of the board?
        collide = False
        if tet.y > self.height-tet.height:
            collide = True
            
        #did it hit another piece on board?
        #Check current position
        else:
            for i in range(len(tet.shape)): #Each line of shape
                for j in range(len(tet.shape[i])):     #Each 1 or zero in shape
                    if (tet.shape[i][j] != 0)  and (self.board[tet.y+i][tet.x+j] != 0):
                        collide = True
        if (collide and (tet.y <= 0)):
            Board.gameOver = True
        return collide

    def collideX(self, tet = None):
        #check if collision 
        if tet == None:
            tet = Board.active
        collide = False
        
        #Check current position
        for i in range(len(tet.shape)): #Each line of shape
            for j in range(len(tet.shape[i])):     #Each 1 or zero in shape
                if (tet.shape[i][j] != 0)  and (self.board[tet.y+i][tet.x+j] != 0):
                    collide = True

        return collide

    def absorb(self, tet = None):
    ##will make the tet part of the board and destroy the current active
        if tet == None:
            tet = Board.active
        if tet == None:
            return
        posx = tet.x
        posy = tet.y
        for i in range(len(tet.shape)): #Each line of shape
            for j in range(len(tet.shape[i])):     #Each 1 or zero in shape
                if tet.shape[i][j]==1:
                    Board.board[posy+i][posx+j] = tet.kind

        Board.active = None
     
    ##ACTIVE TET METHODS=============================================        
    def clearActive(self):
        Board.active = None
        
    def create(self, kind = None):
        Board.active = Tetromino(3, 0, None)
        self.shadowUpdate()
        

    def actIncY(self):
        if Board.active == None:
            return
        Board.active.y += 1
        if(self.collideY()):
            Board.active.y -= 1
            self.absorb()

    def actDecY(self):
        if Board.active == None:
            return
        Board.active.y -= 1
        
    def actMoveX(self, x):
        if Board.active == None:
            return
        Board.active.update(x, 0)
        if (self.collideBorderX() or self.collideX()):
            Board.active.update(-x, 0)
        self.shadowUpdate()


    def Drop(self, tet):
        while(not self.collideY(tet)):
            tet.addY(1)
        tet.addY(-1)
        
    def shadowUpdate(self):
        Board.shadow = Board.active.clone()
        Board.shadow.kind = 8
        self.Drop(Board.shadow)

    def actDrop(self):
        if Board.active == None:
            return
        while(not self.collideY()):
            Board.active.y += 1
        Board.active.y -= 1
        self.absorb()

    def actRotate(self):
        if Board.active == None:
            return
        success = True
        edge = False
        tempPiece = Board.active.clone()
        tempPiece.rotate()
            
        side = self.collideBorderX(tempPiece)
        if side == 0:
            pass
        elif side == 1:
            tempPiece.x = 0
        elif side == 2:
            tempPiece.x = self.width - tempPiece.width

        if tempPiece.y > self.height - tempPiece.height:
            tempPiece.setY(self.height - tempPiece.height)
        if (self.collideX(tempPiece)):
            success = False
        
        if (success):
            Board.active = tempPiece.clone()
        del tempPiece

        self.shadowUpdate()

    def store(self):
        Board.active, Board.stored = Board.stored, Board.active
        if Board.active == None:
            self.create()
        Board.active.setPos(3, 0)
        self.shadowUpdate()
        
        
        
    
                
        
        

    
        
        

        
        

        
        
        

    
    
    
        
