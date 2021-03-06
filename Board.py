import pygame

import Constants
from Constants import *
from Tetromino import *
from collections import deque
import RandomGenerator
from enum import Enum


class AnimationState(Enum):
    CLEARING_LINES = 1


class Board:
    board = []
    gameOver = False
    active = None
    shadow = None
    stored = None
    current_animation_state = None
    fall_rate = 2.0
    touch_count = 0.0

    line_clear_flash_length = 50
    line_clear_anim_flash_count = 2
    line_clear_anim_current_flash_count = 0
    line_clear_anim_start_time = 0

    lines_total = 0
    level = 1
    next_level = 5
    combo_length = 0
    points = 0

    next_pieces = deque()
    pieces = []

    for i in range(1, 8):
        pieces.append(Tetromino(0, 0, i))

    ##BOARD METHODS==================================================================

    def __init__(self, width, height):
        self.inAnimation = False
        Board.board = [[0] * width for i in range(height)]
        self.width = width
        self.height = height
        for i in range(7):
            self.next_pieces.append(RandomGenerator.get_next())

        self.opacity_screen10 = pygame.Surface(((width) * BLOCKSIZE, (height) * BLOCKSIZE), pygame.SRCALPHA)
        # self.opacity_screen10.fill((0,0,0,40))

    def clear(self):
        Board.board = [[0] * self.width for i in range(self.height)]
        Board.active = None
        Board.stored = None
        Board.gameOver = False
        Board.fall_rate = 2.0
        Board.lines_total = 0
        Board.level = 1
        Board.next_level = 5
        Board.touch_count = 0

        Board.combo_length = 0
        Board.points = 0

        RandomGenerator.reseed()
        self.next_pieces.clear()
        for i in range(7):
            self.next_pieces.append(RandomGenerator.get_next())

    def render(self, screen, offX, offY):

        pygame.draw.rect(screen,
                         (255,255, 255),
                         (offX * BLOCKSIZE - BOARD_BOARDER, offY * BLOCKSIZE - BOARD_BOARDER,
                          BLOCKSIZE * Constants.WIDTH + BOARD_BOARDER * 2, BLOCKSIZE * Constants.HEIGHT + BOARD_BOARDER * 2))  # self.width = 2

        for i in range(len(Board.board)):  # For each row
            for j in range(len(Board.board[i])):  # For each cell in that row
                block = blocks[Board.board[i][j]] if Board.board[i][j] == 0 else blocks[9]
                screen.blit(block, ((j + offX) * BLOCKSIZE, (i + offY) * BLOCKSIZE))

        if self.current_animation_state is AnimationState.CLEARING_LINES:
            if self.line_clear_anim_start_time == 0:
                self.line_clear_anim_start_time = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.line_clear_anim_start_time > self.line_clear_flash_length:
                self.line_clear_anim_current_flash_count += 1
                self.line_clear_anim_start_time = pygame.time.get_ticks()
            if self.line_clear_anim_current_flash_count > self.line_clear_anim_flash_count:
                self.endLineClearAnimation()
            else:
                for i in self.to_be_removed:
                    for j in range(len(Board.board[i])):  # For each cell in that row
                        block = blocks[11] if self.line_clear_anim_current_flash_count % 2 == 0 else blocks[9]
                        screen.blit(block, ((j + offX) * BLOCKSIZE, (i + offY) * BLOCKSIZE))

        screen.blit(self.opacity_screen10, (offX * BLOCKSIZE, offY * BLOCKSIZE))

        if Board.active is not None:
            Board.shadow.render(screen, offX, offY)
            Board.active.render(screen, offX, offY, 1.0 - (Board.touch_count / Board.fall_rate))

    def render_next(self, screen, offX, offY):
        for i in range(5):
            self.pieces[self.next_pieces[i] - 1].render(screen, offX, offY + 3 * i)

    to_be_removed = []

    def endLineClearAnimation(self):
        self.inAnimation = False
        self.current_animation_state = None
        self.line_clear_anim_current_flash_count = 0
        self.line_clear_anim_start_time = 0

        for i in self.to_be_removed:
            Board.board.pop(i)

        for i in range(len(self.to_be_removed)):
            Board.board.insert(0, [0] * self.width)

        self.to_be_removed = []

    def update(self):
        # clears Lines
        count = 0
        # clearing lines
        for i in reversed(range(len(Board.board))):
            if all(Board.board[i]):
                self.to_be_removed.append(i)
                count += 1
        if count > 0:
            self.inAnimation = True
            self.current_animation_state = AnimationState.CLEARING_LINES

        # update score
        self.score(count)
        # updating image data
        if count > 0:
            Board.fall_rate += count / 10.0
            if Board.lines_total >= Board.next_level:
                Board.level += 1
                Board.next_level += 5 * Board.level
                print("level: " + str(Board.level))
                print("lines: " + str(Board.lines_total))
                print("To next: " + str(Board.next_level))
                print("score: " + str(Board.points))

    def score(self, lines):
        new_points = 0
        if lines == 1:
            new_points += 100 * Board.level
            Board.lines_total += 1
        elif lines == 2:
            new_points += 300 * Board.level
            Board.lines_total += 3
        elif lines == 3:
            new_points += 500 * Board.level
            Board.lines_total += 5
        elif lines == 4:
            new_points += 800 * Board.level
            Board.lines_total += 8

        if lines == 0:
            Board.combo_length = 0
        else:
            Board.combo_length += 1
            new_points += Board.combo_length * 50 * Board.level
            print(new_points)
        Board.points += new_points
        return new_points

    def collideBorderX(self, tet=None):
        # returns 1 for left, 2 for right, 0 for neither
        # Defaults to using active
        if tet == None:
            tet = Board.active

        side = 0
        if tet.x < 0:
            side = 1
        if tet.x + tet.width > self.width:
            side = 2
        return side

    def collideY(self, tet=None):
        # Check if shape has fallen on the bottom of the board
        if tet == None:
            tet = Board.active

        # did active hit the bottom of the board?
        collide = False
        if tet.y > self.height - tet.height:
            collide = True

        # did it hit another piece on board?
        # Check current position
        else:
            for i in range(len(tet.shape)):  # Each line of shape
                for j in range(len(tet.shape[i])):  # Each 1 or zero in shape
                    if (tet.shape[i][j] != 0) and (self.board[tet.y + i][tet.x + j] != 0):
                        collide = True
        if (collide and (tet.y <= 0)):
            Board.gameOver = True
        return collide

    def collideX(self, tet=None):
        # check if collision
        if tet == None:
            tet = Board.active
        collide = False

        # Check current position
        for i in range(len(tet.shape)):  # Each line of shape
            for j in range(len(tet.shape[i])):  # Each 1 or zero in shape
                if (tet.shape[i][j] != 0) and (self.board[tet.y + i][tet.x + j] != 0):
                    collide = True

        return collide

    def absorb(self, tet=None):
        ##will make the tet part of the board and destroy the current active
        if tet == None:
            tet = Board.active
        if tet == None:
            return
        posx = tet.x
        posy = tet.y
        for i in range(len(tet.shape)):  # Each line of shape
            for j in range(len(tet.shape[i])):  # Each 1 or zero in shape
                if tet.shape[i][j] == 1:
                    Board.board[posy + i][posx + j] = tet.kind

        Board.active = None

        self.update()

    ##ACTIVE TET METHODS=============================================        
    def clearActive(self):
        Board.active = None

    def create(self):
        self.next_pieces.append(RandomGenerator.get_next())
        Board.active = Tetromino(3, 0, self.next_pieces.popleft())
        self.shadowUpdate()

    def actIncY(self):
        if Board.active == None:
            return
        Board.active.y += 1
        if (self.collideY()):
            self.actDecY()
            Board.touch_count += 1.0
        if (Board.touch_count > Board.fall_rate):
            self.absorb()
            Board.touch_count = 0.0
        self.shadowUpdate()

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
        while (not self.collideY(tet)):
            tet.addY(1)
        tet.addY(-1)

    def shadowUpdate(self):
        if Board.active is None:
            return
        Board.shadow = Board.active.clone()
        Board.shadow.kind = 8 # TODO: kind should be an enum
        self.Drop(Board.shadow)

    def actDrop(self):
        if Board.active is None:
            return
        while (not self.collideY()):
            Board.active.y += 1
        Board.active.y -= 1
        self.absorb()
        Board.touch_count = 0.0

    def actRotate(self, wise=1):
        if Board.active == None:
            return
        success = True
        tempPiece = Board.active.clone()
        if wise == 1:
            tempPiece.rotate()
        else:
            tempPiece.rotate_counter()

        side = self.collideBorderX(tempPiece)
        if side == 0:
            pass
        elif side == 1:
            tempPiece.x = 0
        elif side == 2:
            tempPiece.x = self.width - tempPiece.width

        if tempPiece.y > self.height - tempPiece.height:
            tempPiece.setY(self.height - tempPiece.height)
        if self.collideX(tempPiece):
            tempPiece.addY(-1)
        if self.collideX(tempPiece):
            success = False

        if success:
            Board.active = tempPiece.clone()
            Board.touch_count = 0
        del tempPiece

        self.shadowUpdate()

    def store(self):
        Board.active, Board.stored = Board.stored, Board.active
        if Board.active == None:
            self.create()
        Board.active.setPos(3, 0)
        self.shadowUpdate()
