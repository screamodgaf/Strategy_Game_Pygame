import pygame

class Mover(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.oTop = self.top
        self.oBottom = self.bottom
        self.oRight = self.right
        self.oLeft = self.left
    def move(self, x , y ):
        self.x += x
        self.y += y
    def updateOldPos(self):
        self.oTop = self.top
        self.oBottom = self.bottom
        self.oRight = self.right
        self.oLeft = self.left
    def checkCollisions(self, listOfObjects, nodeWithPlayer):
        for c in listOfObjects:
            print("----------------")
            if c is nodeWithPlayer:
                continue
            if self.colliderect(c) == False:
                print("self.colliderect(c) == False:")
                continue
            if self.colliderect(c) == True and c.checkIfObstackle() == False:
                print("self.colliderect(c) == TRUE:")
                continue
            '''  
            TODO
            if c.checkIfObstackle() == False:
                print("c.checkIfObstackle() == False")
                continue
            '''
            #print("collision")
            #print(self.top, " ", self.oTop)
            print("myBottom: ", self.bottom, " wallTop: ", c.top)
            print("myoBottom: ", self.oBottom, " wallTop: ", c.oTop)

            if self.bottom < c.top or self.top > c.bottom or self.left > c.right or self.right < c.left:
                print("return")
                continue

            if self.bottom >= c.top and self.oBottom <= c.oTop:
                self.bottom = c.top - 0.1
                print("bottom")
            if self.top <= c.bottom and self.oTop >= c.oBottom:
                self.top = c.bottom +0.1
                print("top")

            if self.right >= c.left and self.oRight <= c.oLeft:
                self.right = c.left -0.1
                print("right")
            if self.left <= c.right and self.oLeft >= c.oRight:
                self.left = c.right + 0.1
                print("left")
            print("None")
