# Import the pygame module
import pygame
import sys
import math
from node import Node
from pathFinding import PathFinding
from world import World
from mover import Mover
def createControlableObject():
    # Create a rectangle object
    mover = Mover(100, 300, 48, 48)
    return mover

def checkWorldBountaries(player, FIELD_SIZE, MATRIX_WIDTH, MATRIX_HEIGHT):
    if player.x + player.width >=   MATRIX_WIDTH *FIELD_SIZE:
        player.x = MATRIX_WIDTH *FIELD_SIZE - player.width-1
    elif player.x  <  0:
        player.x = 0
    elif player.y + player.height >  MATRIX_HEIGHT * FIELD_SIZE:
        player.y = MATRIX_HEIGHT * FIELD_SIZE - player.height-1
    elif player.y <  0:
        player.y = 0

def checkMatrixBountaries(matrixX, matrixY, MATRIX_WIDTH, worldNodesList):
    if matrixX + matrixY * MATRIX_WIDTH >= len(worldNodesList) or matrixX + matrixY * MATRIX_WIDTH <0:
        return True
def checkKeyEvents(player, worldNodesList, FIELD_SIZE, MATRIX_WIDTH):
    speed = 5
    # Get the state of the keyboard keys
    keys = pygame.key.get_pressed()
    # Check if the left arrow key is pressed
    pw = player.width
    if keys[pygame.K_LEFT]:
        # Move the rectangle to the left
        if determineIfPlayerCanMove(player, -speed, 0,
                                    worldNodesList, FIELD_SIZE, MATRIX_WIDTH, MATRIX_HEIGHT) == False:
            player.move(-speed, 0)
    # Check if the right arrow key is pressed
    elif keys[pygame.K_RIGHT]:
        # Move the rectangle to the right
        if determineIfPlayerCanMove(player, speed+pw, 0,
                                    worldNodesList, FIELD_SIZE, MATRIX_WIDTH, MATRIX_HEIGHT) == False:
            player.move(speed, 0)
    # Check if the up arrow key is pressed
    if keys[pygame.K_UP]:
        # Move the rectangle up
        if determineIfPlayerCanMove(player, 0, -speed,
                                    worldNodesList, FIELD_SIZE, MATRIX_WIDTH, MATRIX_HEIGHT) == False:
            player.move(0, -speed)
    # Check if the down arrow key is pressed
    elif keys[pygame.K_DOWN]:
        # Move the rectangle down
        if determineIfPlayerCanMove(player, 0, speed+pw,
                                    worldNodesList, FIELD_SIZE, MATRIX_WIDTH, MATRIX_HEIGHT) == False:
            player.move(0, speed)

    checkWorldBountaries(player, FIELD_SIZE, MATRIX_WIDTH, MATRIX_HEIGHT)

def fps_counter(screen, system_font):
    fps = str(int(clock.get_fps()))
    fps_text = system_font.render(fps, 1, pygame.Color("WHITE"))
    screen.blit(fps_text, (0, 0))  # Adjust the position as needed

def getSystemFont():
    font_name = "Arial"
    system_font_size = 18
    system_font = pygame.font.SysFont(font_name, system_font_size)
    return system_font

'''  
def createObjectsToDraw():
    rect = pygame.Rect(600, 300, 100, 50)
    listOfObjectsToDraw = []
    listOfObjectsToDraw.append(rect)
    return listOfObjectsToDraw
'''

def drawObjects(listOfObjectsToDraw):
    for rect in listOfObjectsToDraw:
        pygame.draw.rect(screen, (255,10,10), rect)

def drawControlableObject(player):
    pygame.draw.rect(screen, (255,255,0), player)

def determinePlayersNode(player, worldNodesList, FIELD_SIZE):
    #this method 1. find the node in the world, where the player is placed
    # 2. determines all neighbours of the node, where the player is, and returns the array:

    x = int(player.x/FIELD_SIZE)
    y = int(player.y/FIELD_SIZE)
    nodeWithPlayer = worldNodesList[x + y * MATRIX_WIDTH]
    return nodeWithPlayer

def determineIfPlayerCanMove(player, moveX, moveY, worldNodesList, FIELD_SIZE, MATRIX_WIDTH, MATRIX_HEIGHT):
    posX = player.x + moveX
    posY = player.y + moveY
    matrixX = int(posX/FIELD_SIZE)
    matrixY = int(posY/FIELD_SIZE)
    if checkMatrixBountaries(matrixX, matrixY, MATRIX_WIDTH, worldNodesList):
        return True
    nodePredictedAfterAddingMovement = worldNodesList[matrixX + matrixY * MATRIX_WIDTH ]
    if nodePredictedAfterAddingMovement.checkIfObstackle():
        print("Obstacle!!!!!!!!!!!!!")
        return True
    if moveY < 0: #movement up  (0, -5)
        posX = player.x + player.width
        posY = player.y + moveY
        matrixX = int(posX / FIELD_SIZE)
        matrixY = int(posY / FIELD_SIZE)
        if checkMatrixBountaries(matrixX, matrixY, MATRIX_WIDTH, worldNodesList):
            return True
        nodePredictedAfterAddingMovement = worldNodesList[matrixX + matrixY * MATRIX_WIDTH]
        if nodePredictedAfterAddingMovement.checkIfObstackle():
            print("Obstacle!!!!!!!!!!!!!")
            return True

    elif moveY > 0: #movement down (0,5)
        posX = player.x + player.width
        posY = player.y + moveY
        matrixX = int(posX / FIELD_SIZE)
        matrixY = int(posY / FIELD_SIZE)
        if checkMatrixBountaries(matrixX, matrixY, MATRIX_WIDTH, worldNodesList):
            return True
        nodePredictedAfterAddingMovement = worldNodesList[matrixX + matrixY * MATRIX_WIDTH]
        if nodePredictedAfterAddingMovement.checkIfObstackle():
            print("Obstacle!!!!!!!!!!!!!")
            return True

    if moveX < 0: #movement left (-5,0)
        posX = player.x + moveX
        posY = player.y + player.height
        matrixX = int(posX / FIELD_SIZE)
        matrixY = int(posY / FIELD_SIZE)
        if checkMatrixBountaries(matrixX, matrixY, MATRIX_WIDTH, worldNodesList):
            return True
        nodePredictedAfterAddingMovement = worldNodesList[matrixX + matrixY * MATRIX_WIDTH]
        if nodePredictedAfterAddingMovement.checkIfObstackle():
            print("Obstacle!!!!!!!!!!!!!")
            return True

    elif moveX > 0: #movement right (5,0)
        posX = player.x + moveX
        posY = player.y + player.height
        matrixX = int(posX / FIELD_SIZE)
        matrixY = int(posY / FIELD_SIZE)
        if checkMatrixBountaries(matrixX, matrixY, MATRIX_WIDTH, worldNodesList) == True:
            return True
        nodePredictedAfterAddingMovement = worldNodesList[matrixX + matrixY * MATRIX_WIDTH]
        if nodePredictedAfterAddingMovement.checkIfObstackle():
            print("Obstacle!!!!!!!!!!!!!")
            return True
    return False

#for now not used - might be useful when checking collisions with movable objects which are in certain nodes:
def determinePlayerNodeNeighbours(nodeWithPlayer):
    #i want to check if the player collides only with its neighbours nodes, not all as its not efficient:
    upDownLeftRightNeighbours = nodeWithPlayer.getNeighbourList()
    diagonalNeighbours = nodeWithPlayer.getDiagonalNeighbourList()

    allNeighbours = upDownLeftRightNeighbours + diagonalNeighbours
    closeWalls = []
 
    #i also have to check the nodeWithPlayer, as when i move right, the upper-left corner of player enters another node, bypassing the nearest neighbour:
    allNeighbours.append(nodeWithPlayer)
    '''  
    for i in allNeighbours:
        if i.getType() == "wall":
            if player.colliderect(i):
                i.setColour((0, 200, 0))
                #print("collides")
        else:
            print(" ")
    '''
    return allNeighbours
# Initialize pygame
pygame.init()
# Create a display surface
screen = pygame.display.set_mode((800, 600))
# Set the caption of the window
pygame.display.set_caption("Game")
# Create a clock object
clock = pygame.time.Clock()

#Create objects to draw:
#listOfObjectsToDraw = createObjectsToDraw()

#create human controlled object with keyboard:
player = createControlableObject()

# Create a color object
color = pygame.Color(255, 0, 0)

MATRIX_HEIGHT = 12
MATRIX_WIDTH = 16
FIELD_SIZE = 50
world = World(screen, MATRIX_HEIGHT, MATRIX_WIDTH,FIELD_SIZE)
worldNodesList = world.associateMatrixToDrawableRects()




#set start and end nodes for pathfinding:
startNode = worldNodesList[0 + 0 * MATRIX_WIDTH]
#goalNode = worldRectsList[7 + 5 * MATRIX_WIDTH]
goalNode = worldNodesList[(MATRIX_WIDTH-1) + (MATRIX_HEIGHT-1) * MATRIX_WIDTH]
#find closest path between 2 nodes:
pathFinding = PathFinding(screen, startNode, goalNode, MATRIX_HEIGHT, MATRIX_WIDTH, FIELD_SIZE, worldNodesList)

system_font = getSystemFont()
#test
#test  = worldRectsList[7 + 0 * MATRIX_WIDTH]
#nodesEvaluated.append(test)

# Create a variable for controlling the game loop
running = True
# Start the game loop
while running:
    # Handle the events
    for event in pygame.event.get():
        # Check if the user clicked the close button
        if event.type == pygame.QUIT:
            # Exit the loop
            running = False
            sys.exit()

    nodeWithPlayer = determinePlayersNode(player, worldNodesList, FIELD_SIZE)
    playerNeighboursList = determinePlayerNodeNeighbours(nodeWithPlayer)


    checkKeyEvents(player, worldNodesList, FIELD_SIZE, MATRIX_WIDTH)
    checkWorldBountaries(player, FIELD_SIZE, MATRIX_WIDTH, MATRIX_HEIGHT)
    '''  
    player.checkCollisions(playerNeighboursList, nodeWithPlayer)
    player.updateOldPos()
    # so to set old position:
    for i in playerNeighboursList:
        i.updateOldPos()
    '''

    # Fill the screen with black
    screen.fill((0, 0, 0))



    #draw nodes on the screen according to the natrix:
    world.drawMatrix(worldNodesList)

    pathFinding.run()

    #drawObjects(listOfObjectsToDraw)
    drawControlableObject(player)
    fps_counter(screen, system_font)
    # Update the display
    pygame.display.update()
    # Control the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
