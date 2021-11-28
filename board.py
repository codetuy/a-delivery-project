from random import randint

from node import *
from display import *
from button import Button

pygame.init()


class Board:
    def __init__(self, rows, cols):
        self.start = Node(None, None)
        self.goal = Node(None, None)
        self.current = Node(None, None)
        self.path = []
        self.matrix = []
        self.cols = cols
        self.rows = rows
        self.finish = False
        self.userSelect = None
        self.act = 'select'

        self.checkpoints = []
        self.checkpointsFound = []
        self.openSetsBox = [[self.start]]
        self.openSet = [self.start]
        self.closedSetBox = [[]]
        self.currentBox = 1
        self.paths = []

    def setBorder(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if j == 0 or i == 0 or j == self.cols - 1 or i == self.rows - 1:
                    self.matrix[i][j].wall = True

    def selectCheckpoints(self):
        cont = True
        self.userSelect = 'box'
        count = 0
        next_b = Button(GOLD, WIDTH - 100, HEIGHT - 30, 90, 20, text="Next")
        while cont:
            for e in pygame.event.get():
                mouseX, mouseY = pygame.mouse.get_pos()
                if e.type == pygame.MOUSEBUTTONDOWN and e.type != pygame.MOUSEBUTTONUP:
                    x = (mouseX - padding) // ppb
                    y = (mouseY - padding) // ppb
                    if 1 <= x < (self.cols - 1) and 1 <= y < (self.rows - 1):
                        self.checkpoints.append(Node(None, None))
                        self.checkpoints[count].x = x
                        self.checkpoints[count].y = y
                        self.matrix[y][x] = self.checkpoints[count]
                        self.openSetsBox.append([self.checkpoints[count]])
                        count += 1

                    if next_b.isOver((mouseX, mouseY)):
                        next_b.color = ORANGE
                        if count > 0:
                            self.checkpointsFound = [False for _ in range(len(self.checkpoints))]
                        else:
                            self.openSet = self.openSetsBox[0]
                        self.userSelect = None
                        cont = False
                    else:
                        next_b.color = GOLD

            display_l(self)
            next_b.draw(screen)
            pygame.display.update()

    def selectStartAndGoal(self):
        click = 0
        cont = True
        self.userSelect = 's'
        self.act = None
        while cont:
            for e in pygame.event.get():
                mouseX, mouseY = pygame.mouse.get_pos()
                x = (mouseX - padding) // ppb
                y = (mouseY - padding) // ppb
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if 1 <= x < (self.cols - 1) and 1 <= y < (self.rows - 1):
                        if click == 0:
                            self.start.x = x
                            self.start.y = y
                            self.matrix[y][x] = self.start
                            click += 1
                            self.userSelect = 'g'

                        else:
                            if self.start.x != x or self.start.y != y:
                                self.goal.x = x
                                self.goal.y = y
                                self.userSelect = None
                                self.matrix[y][x] = self.goal
                                cont = False
            display(self)

    def initChildren(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.matrix[row][col].createChildren(self)

    def loadBoard(self):
        for row in range(self.rows):
            self.matrix.append([])
            for col in range(self.cols):
                self.matrix[row].append(Node(row, col))

    def initialize(self):
        self.loadBoard()
        self.setBorder()
        self.initChildren()

    def userChoose(self):
        self.selectStartAndGoal()
        self.selectCheckpoints()
        self.start.wall = False
        self.goal.wall = False
        for i in range(len(self.checkpoints)):
            self.checkpoints[i].wall = False
        self.act = None

    def clear(self):
        for i in range(1, self.rows - 1):
            for j in range(1, self.cols - 1):
                self.matrix[i][j] = None
        self.checkpoints = []

    def restart(self):

        self.openSet = [self.start]
        self.openSetsBox = [[self.start]]
        self.closedSetBox = [[]]

        for i in range(len(self.checkpoints)):
            self.openSetsBox.append([self.checkpoints[i]])

        self.path = []
        self.paths = []
        self.finish = False
        self.currentBox = 1

class RandomBoard(Board):
    def __init__(self, rows, cols, probability):
        super().__init__(rows, cols)
        self.wallSpawnProbability = probability

    def generateObstacles(self):
        self.act = "generating"
        for row in range(self.rows):
            for col in range(self.cols):
                i = randint(0, 99)
                if -1 <= i <= self.wallSpawnProbability:
                    self.matrix[row][col].wall = True

    def userChoose(self):
        self.generateObstacles()
        self.selectStartAndGoal()
        self.selectCheckpoints()
        self.start.wall = False
        self.goal.wall = False

class ObstacleBoard(Board):
    def __init__(self, rows, cols):
        super().__init__(rows, cols)
        self.wallShape = 1

    def selectObstacles(self):
        cont = True
        self.userSelect = 'w'
        selection = False
        opta = Button(D_GREEN, WIDTH - 80, padding + 190, 20, 20, "1")
        optb = Button(D_GREEN, WIDTH - 80, padding + 220, 20, 20, "2")
        optc = Button(D_GREEN, WIDTH - 80, padding + 250, 20, 20, "3")
        optd = Button(D_GREEN, WIDTH - 80, padding + 280, 20, 20, "4")
        next_b = Button(GOLD, WIDTH - 100, HEIGHT - 30, 90, 20, text="Next")
        self.wallShape = 1
        while cont:
            for e in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if opta.isOver(pos):
                        self.wallShape = 1
                    elif optb.isOver(pos):
                        self.wallShape = 2
                    elif optc.isOver(pos):
                        self.wallShape = 3
                    elif optd.isOver(pos):
                        self.wallShape = 4

                if opta.isOver(pos):
                    opta.color = D_GREEN
                else:
                    opta.color = AQUA
                if optb.isOver(pos):
                    optb.color = D_GREEN
                else:
                    optb.color = AQUA
                if optc.isOver(pos):
                    optc.color = D_GREEN
                else:
                    optc.color = AQUA
                if optd.isOver(pos):
                    optd.color = D_GREEN
                else:
                    optd.color = AQUA

                if e.type == pygame.MOUSEBUTTONDOWN:
                    selection = True
                if e.type == pygame.MOUSEBUTTONUP:
                    selection = False
                if selection:
                    x = (pos[0] - padding) // ppb
                    y = (pos[1] - padding) // ppb
                    if 0 < x < self.cols and 0 < y < self.rows:
                        if self.wallShape == 1:
                            self.matrix[y][x].wall = True
                        elif self.wallShape == 2 and 2 <= y < self.rows - 2 and 2 <= x < self.cols - 2:
                            self.matrix[y + 1][x + 1].wall = True
                            self.matrix[y][x + 1].wall = True
                            self.matrix[y - 1][x + 1].wall = True
                            self.matrix[y + 1][x - 1].wall = True
                            self.matrix[y][x - 1].wall = True
                            self.matrix[y - 1][x - 1].wall = True
                            self.matrix[y + 1][x].wall = True
                            self.matrix[y - 1][x].wall = True
                        elif self.wallShape == 3 and 2 <= y < self.rows - 2:
                            self.matrix[y + 1][x].wall = True
                            self.matrix[y][x].wall = True
                            self.matrix[y - 1][x].wall = True
                        elif self.wallShape == 4 and 2 <= x < self.cols - 2:
                            self.matrix[y][x + 1].wall = True
                            self.matrix[y][x].wall = True
                            self.matrix[y][x - 1].wall = True

                if self.wallShape == 1:
                    opta.color = D_GREEN
                    optb.color = AQUA
                    optc.color = AQUA
                    optd.color = AQUA
                elif self.wallShape == 2 and 2 <= y < self.rows - 2 and 2 <= x < self.cols - 2:
                    opta.color = AQUA
                    optb.color = D_GREEN
                    optc.color = AQUA
                    optd.color = AQUA
                elif self.wallShape == 3 and 2 <= y < self.rows - 2:
                    opta.color = AQUA
                    optb.color = AQUA
                    optc.color = D_GREEN
                    optd.color = AQUA
                elif self.wallShape == 4 and 2 <= x < self.cols - 2:
                    opta.color = AQUA
                    optb.color = AQUA
                    optc.color = AQUA
                    optd.color = D_GREEN

                if e.type == pygame.MOUSEBUTTONDOWN:
                    if next_b.isOver(pos):
                        next_b.color = ORANGE
                        self.userSelect = None
                        cont = False
                    else:
                        next_b.color = GOLD

                display_l(self)
                opta.draw(screen)
                optb.draw(screen)
                optc.draw(screen)
                optd.draw(screen)
                next_b.draw(screen)
                pygame.display.update()

    def initialize(self):
        self.loadBoard()
        self.setBorder()

    def userChoose(self):
        self.selectStartAndGoal()
        self.selectCheckpoints()
        self.selectObstacles()
        self.initChildren()
        self.start.wall = False
        self.goal.wall = False
        for i in range(len(self.checkpoints)):
            self.checkpoints[i].wall = False

def set_remove(set, current):
    for i, o in enumerate(set):
        if o.x == current.x and o.y == current.y:
            del set[i]
            return
