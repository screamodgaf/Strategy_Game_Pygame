# Import the pygame module
import pygame
import sys
import math
from node import Node
from pathFinding import PathFinding
from world import World

def createControlableObject():
    # Create a rectangle object
    rect = pygame.Rect(100, 300, 30, 30)
    return rect

def checkKeyEvents(player):
    # Get the state of the keyboard keys
    keys = pygame.key.get_pressed()
    # Check if the left arrow key is pressed
    if keys[pygame.K_LEFT]:
        # Move the rectangle to the left
        player.move_ip(-5, 0)
    # Check if the right arrow key is pressed
    if keys[pygame.K_RIGHT]:
        # Move the rectangle to the right
        player.move_ip(5, 0)
    # Check if the up arrow key is pressed
    if keys[pygame.K_UP]:
        # Move the rectangle up
        player.move_ip(0, -5)
    # Check if the down arrow key is pressed
    if keys[pygame.K_DOWN]:
        # Move the rectangle down
        player.move_ip(0, 5)

def fps_counter(screen, system_font):
    fps = str(int(clock.get_fps()))
    fps_text = system_font.render(fps, 1, pygame.Color("WHITE"))
    screen.blit(fps_text, (0, 0))  # Adjust the position as needed

def getSystemFont():
    font_name = "Arial"
    system_font_size = 18
    system_font = pygame.font.SysFont(font_name, system_font_size)
    return system_font

def createObjectsToDraw():
    rect = pygame.Rect(600, 300, 100, 50)
    listOfObjectsToDraw = []
    listOfObjectsToDraw.append(rect)
    return listOfObjectsToDraw

def drawObjects(listOfObjectsToDraw):
    for rect in listOfObjectsToDraw:
        pygame.draw.rect(screen, (255,10,10), rect)

def drawControlableObject(player):
    pygame.draw.rect(screen, (255,255,0), player)

def determineWorldPos(player, worldNodesList, FIELD_SIZE):
    x = int(player.x/FIELD_SIZE)
    y = int(player.y/FIELD_SIZE)
    nodeWithPlayer = worldNodesList[x + y * MATRIX_WIDTH]
    #i want to check if the player collides only with its neighbours nodes, not all as its not efficient:
    upDownLeftRightNeighbours = nodeWithPlayer.getNeighbourList()
    diagonalNeighbours = nodeWithPlayer.getDiagonalNeighbourList()

    allNeighbours = upDownLeftRightNeighbours + diagonalNeighbours
    closeWalls = []
 
    #i also have to check the nodeWithPlayer, as when i move right, the upper-left corner of player enters another node, bypassing the nearest neighbour:
    allNeighbours.append(nodeWithPlayer)
    for i in allNeighbours:
        if i.getType() == "wall":
            if player.colliderect(i):
                i.setColour((0, 200, 0))
                print("collides")
        else:
            print(" ")

# Initialize pygame
pygame.init()
# Create a display surface
screen = pygame.display.set_mode((800, 600))
# Set the caption of the window
pygame.display.set_caption("Game")
# Create a clock object
clock = pygame.time.Clock()

#Create objects to draw:
listOfObjectsToDraw = createObjectsToDraw()
#create human controlled object with keyboard:
player = createControlableObject()

# Create a color object
color = pygame.Color(255, 0, 0)

MATRIX_HEIGHT = 12
MATRIX_WIDTH = 16
FIELD_SIZE = 50
world = World(screen, MATRIX_HEIGHT, MATRIX_WIDTH,FIELD_SIZE)
worldNodesList = world.associateMatrixToDrawableRects()

determineWorldPos(player, worldNodesList, FIELD_SIZE)

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
    checkKeyEvents(player)
    # Fill the screen with black
    screen.fill((0, 0, 0))

    determineWorldPos(player, worldNodesList, FIELD_SIZE)

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
