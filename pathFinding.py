import math
class PathFinding():
    def __init__(self, screen, startNode, goalNode, MATRIX_HEIGHT, MATRIX_WIDTH, FIELD_SIZE, worldRectsList):
        self.screen = screen
        self.startNode = startNode
        self.goalNode = goalNode
        self.worldRectsList = worldRectsList
        self.MATRIX_HEIGHT = MATRIX_HEIGHT
        self.MATRIX_WIDTH = MATRIX_WIDTH
        self.FIELD_SIZE = FIELD_SIZE

        self.nodesToBeEvaluated = []
        self.nodesEvaluated = []
        self.pathList = []
        self.allPaths = []
        # so to display the final, search that doesnt with reaching the goal:
        self.searchFinished = [False]
        self.goalReached = [False]

        self.currentNode = [startNode]
        self.previousNode = [startNode]

        # make sure the start and the goal nodes are not obstackles, otherwise they d never be checked and this goal wouldnt be reached:
        self.startNode.setAsObstackle(False)
        self.goalNode.setAsObstackle(False)
        #run methods:

        # add starting node to nodesToBeEvaluated:
        self.nodesToBeEvaluated.append(startNode)
        # make every mode in the matrix (worldRectsList) know its neighbours (fill neighbours list in every node)
        self.determineNeighboursOfAllNodes()


    def determineNeighboursOfAllNodes(self):
        print("determineNeighboursOfAllNodes")
        for i in range(len(self.worldRectsList)):
            self.worldRectsList[i].determineNeighboursOfNode(self.worldRectsList,
                                                             self.MATRIX_HEIGHT, self.MATRIX_WIDTH)
            self.worldRectsList[i].determineDiagonalNeighboursOfNode(self.worldRectsList,
                                                             self.MATRIX_HEIGHT, self.MATRIX_WIDTH)
    def calculateHeuristics(self, p1, p2):
        #euclidean distance - distance between current node and the end:
        dist = math.sqrt(  math.pow((p2.x/self.FIELD_SIZE - p1.x/self.FIELD_SIZE), 2)
                         + math.pow((p2.y/self.FIELD_SIZE - p1.y/self.FIELD_SIZE), 2)  )
        #print("heuristics: ", dist)
        p1.setDist(dist)
        '''  
        #Manhatan distance: the distance between two points measured along axes at right angles. In a plane with p1 at (x1, y1) and p2 at (x2, y2), it is |x1 - x2| + |y1 - y2|. Lm distance:
        dist = abs(p1.x/100 - p2.x/100) + abs(p1.y/100 - p2.y/100)
        p1.setDist(dist)
        print("Manhatan: ", dist)
        '''
        return dist

    def drawStartAndGoalNodes(self):
        PINK = (255,150,200)
        for i in range(len(self.worldRectsList)):
            if self.worldRectsList[i] == self.startNode or self.worldRectsList[i] == self.goalNode:
                self.worldRectsList[i].draw(self.screen, self.FIELD_SIZE, PINK)

    def drawNodesToBeEvaluated(self):
        #draw the nodes from nodesToBeEvaluated list:
        YELLOW = (255,255,0)
        for i in range(len(self.nodesToBeEvaluated)):
            self.nodesToBeEvaluated[i].draw(self.screen, self.FIELD_SIZE, YELLOW)

    def drawNodesEvaluated(self):
        #draw the nodes from nodesEvaluated list:
        RED = (255,0,0)
        for i in range(len(self.nodesEvaluated)):
            self.nodesEvaluated[i].draw(self.screen, self.FIELD_SIZE, RED)


    def drawPath(self, pathList):
        #draw the nodes from nodesEvaluated list:
        GREEN = (0, 228, 0)
        BLUE = (0,0,255)
        color = GREEN
        if self.searchFinished[0] == True and self.goalReached[0] == False:
            color = BLUE
        if self.searchFinished[0] == True and self.goalReached[0] == True:
            color = GREEN
            print("GREEN")
        for i in range(len(pathList)):
            pathList[i].draw(self.screen, self.FIELD_SIZE, color)

    def estimateActualPath(self, currentNode, pathList):
        if currentNode == 0:
            return
        tempNode =  currentNode
        pathList.append(tempNode)
        # this while loop condition goes all the way back to the startNode:
        while tempNode.getPrevious() != None:
            pathList.append(tempNode.getPrevious()) #adds backwards
            # if previous mode was found, check now its own previous node by setting it do "tempNode" which existence is the while loop condition:
            tempNode = tempNode.getPrevious()
        return pathList

    def findBestUnreachable(self):
        lowestDist = 999
        bestIndex = 0

        for index, path in enumerate(self.allPaths):
            temp = path[0].getDist()
            #print("dist: ", temp)
            if temp < lowestDist:
                lowestDist = temp
                bestIndex = index
        #print("lowest distance: ", lowestDist , " bestIndex: " ,bestIndex, " predicteddist: ", self.allPaths[bestIndex][0].getDist())

        #drawPath(screen, FIELD_SIZE, allPaths[bestIndex], searchFinished, goalReached)
        return self.allPaths[bestIndex]

    def pathFinding(self):
        lowestFNodeIndex = 0
        #currentNode = 0 #this line turns mutable class object Node into int, which is immutable, thus i had to pass it as list[] previousNode
        if len(self.nodesToBeEvaluated) >0:
            for i in range(len(self.nodesToBeEvaluated)):
                #if there is a node better suiting the easiest path - go there setting it as current:
                if self.nodesToBeEvaluated[i].getF() < self.nodesToBeEvaluated[lowestFNodeIndex].getF():
                    lowestFNodeIndex = i
                    self.currentNode = self.nodesToBeEvaluated[lowestFNodeIndex]
                    self.previousNode[0] = self.currentNode
        else:
            #print("Goal unreachable!!!")
            self.searchFinished[0] = True
            self.goalReached[0] = False
            return self.previousNode[0]
        # current node is the node in the nodesToBeEvaluated list having the LOWEST fScore:
        self.currentNode = self.nodesToBeEvaluated[lowestFNodeIndex]

        if self.currentNode == self.goalNode:
            print("We reached the goal!")
            self.searchFinished[0] = True
            self.goalReached[0] = True
            #drawPath(screen, FIELD_SIZE, pathList, searchFinished, goalReached)
            # we must return currentNode, cause in the main loop there
            return self.currentNode

        self.nodesToBeEvaluated.remove(self.currentNode)
        #nodesEvaluated consist of currents (red), but not all corrents create the path:
        self.nodesEvaluated.append(self.currentNode)
        #check every single neighbour of the current node for g value:
        neighboursOfCurrent = self.currentNode.getNeighbourList()
        for i in range(len(neighboursOfCurrent)):
            neighbour = neighboursOfCurrent[i]
            #check if a neighbour was already evaluated (meaning is present in nodesEvaluated):
            if (neighbour.checkIfObstackle() == False) and (neighbour not in self.nodesEvaluated):
                #and if it was not evaluated, get its g and add 1 to it, as every neighbour of current node will have higher g (current.g + 1):
                tempG = self.currentNode.getG() +1 + self.calculateHeuristics(neighbour, self.goalNode)
                #check, if the neighbour with a lower tempG was already found in nodesToBeEvaluated (meaning there is a better way to get there):

                if neighbour in self.nodesToBeEvaluated:
                    #so if the neighbour was already evaluated and its g is smaller than tempG, set its g to tempG:
                    if neighbour.getG() > tempG:
                        neighbour.setG(tempG)

                #and if the neighbour is not in nodesToBeEvaluated, set its g to the current's g +1 (currentNode.getG() +1):
                else:
                    neighbour.setG(tempG)
                    self.nodesToBeEvaluated.append(neighbour)
                    #setting heuristics (educated guess how long will it take to get to the end) for the neighbour:
                    neighbour.setH(self.calculateHeuristics(neighbour, self.goalNode))
                    neighbour.setF( neighbour.getG() + neighbour.getH() )
                    #get the previous node (where it came from), for finding the best path:
                    #so we seek for the best neighbour, and set current node as the predecesor of the neighbour
                    neighbour.setPrevious(self.currentNode)
        return self.currentNode

    def run(self):
        pathList = []
        currentNode = self.pathFinding()

        # draw A* algorithm at work:
        pathList = self.estimateActualPath(currentNode, pathList)

        # draw the nodes from nodesEvaluated list:
        self.drawNodesEvaluated()  # RED
        # draw the nodes from nodesToBeEvaluated list:
        self.drawNodesToBeEvaluated()  # YELLOW

        self.drawStartAndGoalNodes()

        if self.searchFinished[0] == False:
            # it draws only when the algorithm is not done. The file path drawing is called in a different line
            self.drawPath(pathList)
            self.allPaths.append(pathList)

        # when the goal is unreachable, get the path leading to the closest node to the goal:
        if self.searchFinished[0] == True and self.goalReached[0] == False:
            bestPath = self.findBestUnreachable()
            self.drawPath(bestPath)

        if self.searchFinished[0] == True and self.goalReached[0] == True:
            self.drawPath(pathList)

