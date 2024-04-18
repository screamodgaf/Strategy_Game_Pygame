import pygame
import random
from node import Node

class World():
    def __init__(self, screen, MATRIX_HEIGHT, MATRIX_WIDTH,FIELD_SIZE):
        self.MATRIX_HEIGHT = MATRIX_HEIGHT
        self.MATRIX_WIDTH = MATRIX_WIDTH
        self.FIELD_SIZE = FIELD_SIZE
        self.matrix =[]
        self.screen = screen

        self.createMatrix()
        self.makeRandomObstackles()

    def createMatrix(self):
        '''
        #Create matrix
        matrix = [0,1,0,0,0,0,0,0,
                  0,1,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,
                  1,1,1,1,1,1,1,0,
                  0,0,0,0,0,0,1,0,
                  0,0,0,0,0,0,1,0]

        MATRIX_HEIGHT = 6
        MATRIX_WIDTH = 8
        FIELD_SIZE = 30
        '''
        self.matrix = [0] * self.MATRIX_HEIGHT * self.MATRIX_WIDTH

    def associateMatrixToDrawableRects(self):
        worldNodesList = []
        WHITE = (255,255,255)
        BLACK = (0,0,0)

        for y in range(self.MATRIX_HEIGHT):
            for x in range(self.MATRIX_WIDTH):
                node = Node(x * self.FIELD_SIZE, y * self.FIELD_SIZE, self.FIELD_SIZE,
                                self.FIELD_SIZE)  # instead: rect = pygame.Rect(posX, posY, FIELD_SIZE, FIELD_SIZE)
                # if its 1 in matrix, set the associated node as an unpenetrable obstackle:
                if self.matrix[x + y * self.MATRIX_WIDTH] == 1:
                    node.setAsObstackle()
                    node.setType("wall")
                    node.setColour(BLACK)
                else:
                    node.setType("land")
                    node.setColour(WHITE)
                worldNodesList.append(node)

        return worldNodesList

    def makeRandomObstackles(self):
        for _ in range(200):
            x = random.randint(1, self.MATRIX_WIDTH - 1)
            y = random.randint(1, self.MATRIX_HEIGHT - 1)
            self.matrix[x + y * self.MATRIX_WIDTH] = 1

    def drawMatrix(self, worldNodesList):
        for y in range(self.MATRIX_HEIGHT):
            for x in range(self.MATRIX_WIDTH):
                if self.matrix[x + y * self.MATRIX_WIDTH] == 0:
                    color = worldNodesList[x + y * self.MATRIX_WIDTH].getColour()
                    worldNodesList[x + y * self.MATRIX_WIDTH].draw(self.screen,
                                                                        self.FIELD_SIZE, color)
                elif self.matrix[x + y * self.MATRIX_WIDTH] == 1:
                    color = worldNodesList[x + y * self.MATRIX_WIDTH].getColour()
                    worldNodesList[x + y * self.MATRIX_WIDTH].draw(self.screen,
                                                                        self.FIELD_SIZE, color)
